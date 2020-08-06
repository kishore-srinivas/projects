''' assignment for section 4 of udemy course: https://www.udemy.com/course/deep-q-learning-from-paper-to-code/ '''

import os
import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

class DeepQNetwork(nn.Module):
    def __init__(self, learningRate, numActions, inputDims, fileName, fileDir):
        super(DeepQNetwork, self).__init__()
        self.fileDir = fileDir
        self.fileLoc = os.path.join(self.fileDir, fileName)

        self.conv1 = nn.Conv2d(inputDims[0], 32, 8, stride=4)
        self.conv2 = nn.Conv2d(32, 64, 4, stride=2)
        self.conv3 = nn.Conv2d(64, 64, 3, stride=1)

        fcInputDims = self.calculateConvOutputDims(inputDims)
        self.fc1 = nn.Linear(fcInputDims, 512)
        self.fc2 = nn.Linear(512, numActions)

        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.optimizer = optim.RMSprop(self.parameters(), lr=learningRate)
        self.loss = nn.MSELoss()
        self.to(self.device)

    def calculateConvOutputDims(self, inputDims):
        state = T.zeros(1, *inputDims)
        dims1 = self.conv1(state)
        dims2 = self.conv2(dims1)
        dims3 = self.conv3(dims2)
        return int(np.prod(dims3.size()))

    def forward(self, state):
        out1 = F.relu(self.conv1(state))
        out2 = F.relu(self.conv2(out1))
        out3 = F.relu(self.conv3(out2))
        convState = out3.view(out3.size()[0], -1)
        out4 = F.relu(self.fc1(convState))
        out5 = self.fc2(out4)
        return out5

    def saveCheckpoint(self):
        T.save(self.state_dict(), self.fileLoc)

    def loadCheckpoint(self):
        self.load_state_dict(T.load(self.fileLoc))