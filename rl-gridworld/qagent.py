from grid import Grid, Action
import numpy as np

class QAgent:
    def __init__(self, grid, explorationRate, learningRate=0.1, gamma=0.9):
        posX = np.random.randint(grid.width, size=1)[0]
        posY = np.random.randint(grid.height, size=1)[0]
        while not grid.isEmpty(posX, posY):
            posX = np.random.randint(grid.width, size=1)[0]
            posY = np.random.randint(grid.height, size=1)[0]
        self.position = (posX, posY)
        self.initialPosition = (posX, posY)        
        grid.setSquare(posX, posY, 'A')
        self.grid = grid
        self.states = []
        self.explorationRate = explorationRate
        self.learningRate = learningRate
        self.gamma = gamma
        self.qValues = {}
        for i in range(grid.width):
            for j in range(grid.height):
                self.qValues[(i, j)] = {}
                for a in Action:
                    self.qValues[(i, j)][a] = 0

    def takeAction(self, action):
        nextPos = self.grid.getNextLegalPosition(self.getPosition(), action)
        self.grid.setSquare(*self.position, ' ')
        self.position = nextPos
        self.grid.setSquare(*nextPos, 'A')
        # self.grid.draw()

    def chooseAction(self):
        if (np.random.uniform(0, 1) <= self.explorationRate):
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

    def play(self, rounds=200):
        for i in range(rounds):
            reward = self.grid.giveReward(self.getPosition())
            if (reward == 1):
                print(i, "GOAL!")
                for a in Action:
                    self.qValues[self.getPosition()][a] = reward
                for s in reversed(self.states):
                    currentQValue = self.qValues[s[0]][s[1]]
                    reward = currentQValue + self.learningRate * (self.gamma * reward - currentQValue)
                    self.stateValues[s[0]][s[1]] = round(reward, 3)
                self.position = self.initialPosition
                self.states = []
            else:
                action = self.chooseAction()
                self.states.append([self.getPosition(), action])
                print(i, 'current pos: {} action {}'.format(self.getPosition(), action))
                self.takeAction(action)
    
    def getPosition(self):
        return self.position

    def getQValues(self):
        return self.qValues