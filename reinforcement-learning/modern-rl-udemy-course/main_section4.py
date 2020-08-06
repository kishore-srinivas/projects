import numpy as np
from agent_section4 import DQNAgent
from util import makeEnv, plotLearningCurve

if __name__ == '__main__':
    env = makeEnv('PongNoFrameskip-v4')
    bestScore = -np.inf
    loadCheckpoint = False
    numGames = 500
    agent = DQNAgent(gamma=0.99, epsilon=1.0, learningRate=1e-4, inputDims=env.observation_space.shape, numActions=env.action_space.n, memSize=10000, batchSize=32, minEpsilon=0.1, replace=1000, epsilonDecay=1e-5, algo='DQNAgent', envName='PongNoFrameskip-v4')
    if loadCheckpoint:
        agent.loadModels()

    fileName = agent.algo + '_' + agent.envName + '_lr' + str(agent.learningRate) + '_' + str(numGames) + 'games'
    figureFile = filename + '.png'

    numSteps = 0
    scores, epsilonHistory, stepsHistory = [], [], []
    for i in range(numGames):
        done = False
        score = 0
        obs = env.reset()
        while not done:
            action = agent.chooseAction(obs)
            nextObs, reward, done, info = env.step(action)
            score += reward
            if not loadCheckpoint:
                agent.storeTransition(obs, action, reward, nextObs, int(done))
                agent.learn()
            obs = nextObs
            numSteps += 1
        scores.append(score)
        stepsHistory.append(numSteps)

        avgScore = np.mean(scores[-100:])
        print('game {:4d} | avg score {:.2f} | best score {:.2f} | epsilon {:.2f} | steps {}'.format(i, avgScore, bestScore, agent.epsilon, numSteps))
        if avgScore > bestScore:
            if not loadCheckpoint:
                agent.saveModels()
            bestScore = avgScore
        epsilonHistory.append(agent.epsilon)

    plotLearningCurve(stepsHistory, scores, epsilonHistory, figureFile)
