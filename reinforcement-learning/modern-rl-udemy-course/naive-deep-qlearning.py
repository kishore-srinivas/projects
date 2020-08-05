''' assignment for Section 3 of Deep QLearning in Pytorch course https://www.udemy.com/course/deep-q-learning-from-paper-to-code/ '''

import gym
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch as T
from util import plotLearningCurve

class DeepQNetwork(nn.Module):
    def __init__(self, inputDims, numActions, learningRate):
        super(DeepQNetwork, self).__init__()
        self.inputDims = inputDims
        self.numActions = numActions
        self.learningRate = learningRate

        self.layer1 = nn.Linear(*inputDims, 128)
        self.layer2 = nn.Linear(128, numActions)

        self.loss = nn.MSELoss()
        self.optimizer = optim.Adam(self.parameters(), lr=learningRate)
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, state):
        outputLayer1 = F.relu(self.layer1(state))
        actions = self.layer2(outputLayer1)
        return actions

class Agent():
    def __init__(self, inputDims, numActions, learningRate, gamma=0.99, epsilon=1.0, epsilonDecay=1e-5, minEpsilon=0.01):
        self.learningRate = learningRate
        self.inputDims = inputDims
        self.numActions = numActions
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilonDecay = epsilonDecay
        self.minEpsilon = minEpsilon

        self.actionSpace = [i for i in range(numActions)]
        self.QNetwork = DeepQNetwork(self.inputDims, self.numActions, self.learningRate)

    def chooseAction(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.actionSpace)

        state = T.tensor(state, dtype=T.float).to(self.QNetwork.device)
        actions = self.QNetwork.forward(state)
        bestAction = T.argmax(actions).item()
        return bestAction

    def decrementEpsilon(self):
        self.epsilon = max(self.minEpsilon, self.epsilon - self.epsilonDecay)

    def learn(self, state, action, reward, nextState):
        self.QNetwork.optimizer.zero_grad()
        states = T.tensor(state, dtype=T.float).to(self.QNetwork.device)
        actions = T.tensor(action).to(self.QNetwork.device)
        rewards = T.tensor(reward).to(self.QNetwork.device)
        nextStates = T.tensor(nextState, dtype=T.float).to(self.QNetwork.device)

        qPred = self.QNetwork.forward(states)[actions]
        qNext = self.QNetwork.forward(nextStates).max()
        qTarget = reward + self.gamma * qNext
        loss = self.QNetwork.loss(qTarget, qPred).to(self.QNetwork.device)
        loss.backward()
        self.QNetwork.optimizer.step()
        self.decrementEpsilon()

if __name__ == '__main__':
    env = gym.make('CartPole-v1')
    numGames = 10000
    scores = []
    epsilonHistory = []
    agent = Agent(inputDims=env.observation_space.shape, numActions=env.action_space.n, learningRate=1e-4)

    for i in range(numGames):
        score = 0
        done = False
        obs = env.reset()
        while not done:
            action = agent.chooseAction(obs)
            nextObs, reward, done, info = env.step(action)
            score += reward
            agent.learn(obs, action, reward, nextObs)
            obs = nextObs

        scores.append(score)
        epsilonHistory.append(agent.epsilon)
        if (i % 100 == 0):
            avgScore = np.mean(scores[-100:])
            print('game {:4d} | score {:.2f} | avg score {:.2f} | epsilon {:.2f}'.format(i, score, avgScore, agent.epsilon))

    filename = 'cartpole-naive-dqn.png'
    x = [i+1 for i in range(numGames)]
    plotLearningCurve(x, scores, epsilonHistory, filename)       