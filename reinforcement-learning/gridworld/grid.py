import numpy as np
import random
from enum import Enum

class Action(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

class Grid: 
    def __init__(self, rows, cols, deterministic=False, numWalls=1):
        if (numWalls >= rows * cols - 1):
            numWalls = 1
        self.grid = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(' ')
            self.grid.append(row)
        self.numRows = rows
        self.numCols = cols
        self.goal = (0, cols-1)
        self.setSquare(self.goal, 'G')
        self.wall = (2, 1)
        self.setSquare(self.wall, 'X')
        self.trap = (1, cols-1)
        self.setSquare(self.trap, 'T')
        self.deterministic = deterministic
        self.numWalls = numWalls

    def reset(self):
        self.__init__(self.numRows, self.numCols, deterministic=self.deterministic, numWalls=self.numWalls)

    def giveReward(self, pos):
        if (pos == self.goal):
            return 1
        if (self.getSquare(pos) == 'X' or self.getSquare(pos) == 'T'):
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

        if (nextPos[0] < 0 or nextPos[0] >= self.numRows or
            nextPos[1] < 0 or nextPos[1] >= self.numCols):
                return pos
        try:
            if (self.isEmpty(nextPos) or self.isGoal(nextPos)):
                return nextPos
            else:
                return pos
        except:
            return pos

    
    def draw(self):
        for i in range(self.numRows):
            print(self.grid[i])
        print()

    def getSquare(self, pos):
        return self.grid[pos[0]][pos[1]]

    def setSquare(self, pos, value):
        self.grid[pos[0]][pos[1]] = value

    def getNumCols(self):
        return self.numCols

    def getNumRows(self):
        return self.numRows

    def isEmpty(self, pos):
        return self.getSquare(pos) == ' '

    def isGoal(self, pos):
        return self.getSquare(pos) == 'G'
