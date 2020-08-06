import numpy as np

class ReplayBuffer():
    def __init__(self, maxSize, inputShape, numActions):
        self.memSize = memSize
        self.memCounter = 0
        self.stateMemory = np.zeros((self.memSize, *inputShape), dtype=np.float32)
        self.nextStateMemory = np.zeros((self.memSize, *inputShape), dtype=np.float32)
        self.actionMemory = np.zeros(self.memSize, dtype=np.int64)
        self.rewardMemory = np.zeros(self.memSize, dtype=np.float32)
        self.terminalMemory = np.zeros(self.memSize, dtype=np.uint8)

    def storeTransition(self, state, action, reward, nextState, done):
        index = self.memCounter % self.memSize
        self.stateMemory[index] = state
        self.actionMemory[index] = action
        self.rewardMemory[index] = reward
        self.newStateMemory[index] = nextState
        self.memCounter += 1

    def sampleFromBuffer(self, batchSize):
        numEntries = len(self.stateMemory)
        batch = np.random.choice(numEntries, batchSize, replace=False)

        states = self.stateMemory[batch]
        actions = self.actionMemory[batch]
        rewards = self.rewardMemory[batch]
        nextStates = self.nextStateMemory[batch]
        dones = self.terminalMemory[batch]

        return states, actions, rewards, nextStates, dones