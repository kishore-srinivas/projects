from grid import Grid, Action
import numpy as np

class QAgent:
    def __init__(self, grid, explorationRate, learningRate=0.2, gamma=0.9):
        rowPos = np.random.randint(grid.getNumRows(), size=1)[0]
        colPos = np.random.randint(grid.getNumCols(), size=1)[0]
        while not grid.isEmpty((rowPos, colPos)):
            rowPos = np.random.randint(grid.getNumRows(), size=1)[0]
            colPos = np.random.randint(grid.getNumCols(), size=1)[0]
        self.position = (rowPos, colPos)
        self.initialPosition = (rowPos, colPos)        
        grid.setSquare(self.position, 'A')
        self.grid = grid
        self.states = []
        self.explorationRate = explorationRate
        self.learningRate = learningRate
        self.gamma = gamma
        self.qValues = {}
        for i in range(grid.getNumRows()):
            for j in range(grid.getNumCols()):
                self.qValues[(i, j)] = {}
                for a in Action:
                    self.qValues[(i, j)][a] = 0

    def takeAction(self, action):
        nextPos = self.grid.getNextLegalPosition(self.getPosition(), action)
        self.grid.setSquare(self.getPosition(), ' ')
        self.setPosition(nextPos)
        self.grid.setSquare(self.getPosition(), 'A')
        # self.grid.draw()

    def chooseAction(self, exp):
        if (np.random.uniform(0, 1) <= exp):
            num = np.random.randint(1, len(Action)+1, size=1)[0]
            return Action(num)
        else:
            maxReward = 0
            action = Action(1)
            for i in range(1, len(Action)+1):
                a = Action(i)
                nextReward = self.qValues[self.getPosition()][a]
                if (nextReward > maxReward):
                    maxReward = nextReward
                    action = a
            return action

    def play(self, rounds=50):
        lastPos = None
        lastAction = None
        curPos = self.getPosition()
        for i in range(rounds):
            reward = self.grid.giveReward(self.getPosition())
            if (reward == 1):
                print(i, "GOAL!")
                for a in Action:
                    self.qValues[self.getPosition()][a] = -reward
                for s in reversed(self.states):
                    currentQValue = self.qValues[s[0]][s[1]]
                    reward = currentQValue + self.learningRate * (self.gamma * reward - currentQValue)
                    self.qValues[s[0]][s[1]] = round(reward, 3)
                self.reset()
                # return
            else:
                action = self.chooseAction(exp=self.explorationRate)
                if (curPos == lastPos):
                    while (action == lastAction):
                        action = self.chooseAction(exp=self.explorationRate)
                self.states.append([self.getPosition(), action])
                print('{:2d} current pos: {} action {}'.format(i, self.getPosition(), action))
                lastPos = curPos
                self.takeAction(action)
                curPos = self.getPosition()
                lastAction = action
    
    def getPosition(self):
        return self.position

    def setPosition(self, pos):
        self.position = pos

    def getQValues(self):
        return self.qValues

    def reset(self):
        self.grid.reset()
        self.position = self.initialPosition
        self.states = []
        self.grid.setSquare(self.position, 'A')