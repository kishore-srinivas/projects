import numpy as np
import random
from enum import Enum

class Action(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

class Grid: 
    def __init__(self, width, height, deterministic=False, numWalls=1):
        if (numWalls >= width * height - 1):
            numWalls = 1
        self.grid = []
        for i in range(height):
            row = []
            for j in range(width):
                row.append(' ')
            self.grid.append(row)
        self.height = height
        self.width = width
        self.goal = [0, width-1]
        self.grid[self.goal[0]][self.goal[1]] = 'G'
        self.wall = [2, 1]
        self.grid[self.wall[0]][self.wall[1]] = 'X'
        self.trap = [1, width-1]
        self.grid[self.trap[0]][self.trap[1]] = 'T'
        self.deterministic = deterministic
        self.numWalls = numWalls
        # for i in range(numWalls):
        #     wallX = np.random.randint(width, size=1)[0]
        #     wallY = np.random.randint(height, size=1)[0]
        #     if (self.isEmpty(wallX, wallY)):
        #         self.setSquare(wallX, wallY, 'X')
        #     else:
        #         i -= 1

    def reset(self):
        self.__init__(self.width, self.height, deterministic=self.deterministic, numWalls=self.numWalls)

    def giveReward(self, pos):
        if (pos[0] == self.goal[1] and pos[1] == self.goal[0]):
            return 1
        if (self.getSquare(*pos) == 'X' or self.getSquare(*pos) == 'T'):
            return -1
        return 0

    def chooseActionProb(self, action):
        if action == Action.UP:
            return np.random.choice([Action.UP, Action.LEFT, Action.RIGHT], p=[0.8, 0.1, 0.1])
        if action == Action.RIGHT:
            return np.random.choice([Action.RIGHT, Action.UP, Action.DOWN], p=[0.8, 0.1, 0.1])
        if action == Action.DOWN:
            return np.random.choice([Action.DOWN, Action.LEFT, Action.RIGHT], p=[0.8, 0.1, 0.1])
        if action == Action.LEFT:
            return np.random.choice([Action.LEFT, Action.UP, Action.DOWN], p=[0.8, 0.1, 0.1])

    def getNextLegalPosition(self, pos, action):
        if (self.deterministic):
            if action == Action.UP:
                nextPos = (pos[0] - 1, pos[1])
            elif action == Action.RIGHT:
                nextPos = (pos[0], pos[1] + 1)
            elif action == Action.DOWN:
                nextPos = (pos[0] + 1, pos[1])
            elif action == Action.LEFT:
                nextPos = (pos[0], pos[1] - 1)
            self.deterministic = False            
        else:
            a = self.chooseActionProb(action)
            self.deterministic = True
            nextPos = self.getNextLegalPosition(pos, a)

        if (nextPos[0] < 0 or nextPos[0] >= self.width or
            nextPos[1] < 0 or nextPos[1] >= self.height):
                return pos
        try:
            if (self.isEmpty(*nextPos) or self.getSquare(*nextPos) == 'G'):
                return nextPos
            else:
                return pos
        except:
            return pos

    
    def draw(self):
        for i in range(self.height):
            print(self.grid[i])
        print()

    def getSquare(self, x, y):
        return self.grid[y][x]

    def setSquare(self, x, y, value):
        self.grid[y][x] = value

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def isEmpty(self, x, y):
        return self.getSquare(x, y) == ' '
