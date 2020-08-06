import numpy as np
import torch as T
from dqn_section4 import DeepQNetwork
from memory_section4 import ReplayBuffer

class DQNAgent():
    def __init__(self, gamma, epsilon, learningRate, numActions, inputDims, memSize, batchSize, minEpsilon=0.01, epsilonDecay=5e-7, replace=1000, algo=None, envName=None, checkpointDir=''):
        self.gamma = gamma
        self.epsilon = epsilon
        self.learningRate = learningRate
        self.numActions = numActions
        self.inputDims = inputDims
        self.batchSize = batchSize
        self.minEpsilon = minEpsilon
        self.epsilonDecay = epsilonDecay
        self.replaceTargetCount = replace
        self.algo = algo
        self.envName = envName
        self.checkpointDir = checkpointDir
        self.actionSpace = [i for i in range(numActions)]
        self.learnStepCounter = 0
        self.memory = ReplayBuffer(memSize, inputDims, numActions)
        self.evalQ = DeepQNetwork(learningRate, numActions, inputDims=inputDims, fileName=envName+'_'+self.algo+'_q_eval', fileDir=checkpointDir)
        self.nextQ = DeepQNetwork(learningRate, numActions, inputDims=inputDims, fileName=envName+'_'+self.algo+'_q_next', fileDir=checkpointDir)

    def chooseAction(self, observation):
        if np.random.random() < self.epsilon:
            return np.random.choice(self.actionSpace)
        
        state = T.tensor([observation], dtype=T.float).to(self.evalQ.device)
        actions = self.evalQ.forward(state)
        action = T.argmax(actions).item()
        return action

    def storeTransition(self, state, action, reward, nextState, done):
        self.memory.storeTransition(state, action, reward, nextState, done)

    def sampleFromMemory(self):
        state, action, rewards, nextState, done = self.memory.sampleFromBuffer(self.batchSize)
        states = T.tensor(state).to(self.evalQ.device)
        actions = T.tensor(action).to(self.evalQ.device)
        rewards = T.tensor(reward).to(self.evalQ.device)
        nextStates = T.tensor(nextState).to(self.evalQ.device)
        dones = T.tensor(done).to(self.evalQ.device)
        return states, actions, rewards, nextStates, dones

    def replaceTargetNetwork(self):
        if self.learnStepCounter % self.replaceTargetCount == 0:
            self.nextQ.load_state_dict(self.evalQ.state_dict())

    def decrementEpsilon(self):
        self.epsilon = max(self.epsilon - self.epsilonDecay, self.minEpsilon)

    def saveModels(self):
        self.evalQ.save_checkpoint()
        self.nextQ.save_checkpoint()

    def loadModels(self):
        self.evalQ.load_checkpoint()
        self.nextQ.load_checkpoint()

    def learn(self):
        if self.memory.memCounter < self.batchSize:
            return

        self.evalQ.optimizer.zero_grad()
        self.replaceTargetNetwork()
        states, actions, rewards, nextStates, dones = self.sampleFromMemory()

        indices = np.arange(self.batchSize)
        qPred = self.evalQ.forward(states)[indices, actions]
        qNext = self.nextQ.forward(nextStates).max(dim=1)[0]
        qNext[dones] = 0.0
        qTarget = rewards + self.gamma * qNext

        loss = self.evalQ.loss(qTarget, qPred).to(self.evalQ.device)
        loss.backward()
        self.evalQ.optimizer.step()
        self.learnStepCounter += 1
        self.decrementEpsilon()