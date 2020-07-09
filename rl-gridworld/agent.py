from grid import Grid, Action
import numpy as np

class Agent:
    def __init__(self, grid, explorationRate, learningRate=0.1):
        posX = np.random.randint(grid.width, size=1)[0]
        posY = np.random.randint(grid.height, size=1)[0]
        while not grid.isEmpty(posX, posY):
            posX = np.random.randint(grid.width, size=1)[0]
            posY = np.random.randint(grid.height, size=1)[0]
        self.position = (posX, posY)
        self.initialPosition = (posX, posY)        
        grid.setSquare(posX, posY, 'A')
        self.grid = grid
        self.moves = []
        self.explorationRate = explorationRate
        self.learningRate = learningRate
        self.stateValues = {}
        for i in range(grid.width):
            for j in range(grid.height):
                self.stateValues[(i, j)] = self.grid.giveReward((i, j))

    def getPosition(self):
        return self.position

    def moveTo(self, pos):
        self.grid.setSquare(*self.position, ' ')
        self.position = pos
        self.grid.setSquare(*pos, 'A')
        self.moves.append(pos)
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
                nextReward = self.stateValues[self.grid.getNextLegalPosition(self.getPosition(), a)]
                if (nextReward > maxReward):
                    maxReward = nextReward
                    action = a
            return action

    def play(self, rounds=200):
        for i in range(rounds):
            reward = self.grid.giveReward(self.getPosition())
            if (reward == 1):
                print(i, "GOAL!")
                self.stateValues[self.getPosition()] = reward
                for m in reversed(self.moves):
                    reward = self.stateValues[m] + self.learningRate * (reward - self.stateValues[m])
                    self.stateValues[m] = round(reward, 3)
                self.moveTo(self.initialPosition)
                self.moves = []
            else:
                action = self.chooseAction()
                nextPos = self.grid.getNextLegalPosition(self.getPosition(), action)
                print(i, 'moving from {} to {}'.format(self.getPosition(), nextPos))
                self.moves.append(nextPos)
                self.moveTo(nextPos)
