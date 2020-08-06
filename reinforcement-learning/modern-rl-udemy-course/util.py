import numpy as np
import matplotlib.pyplot as plt
import gym
import collections
import cv2

def plotLearningCurve(x, scores, epsilons, filename):
    fig = plt.figure()
    ax1 = fig.add_subplot(111, label='1')
    ax2 = fig.add_subplot(111, label='2', frame_on=False)

    ax1.plot(x, epsilons, color='C0')
    ax1.set_xlabel('Training steps', color='C0')
    ax1.set_ylabel('Epsilon', color='C0')
    ax1.tick_params(axis='x', colors='C0')
    ax1.tick_params(axis='y', colors='C0')

    N = len(scores)
    runningAvg = np.empty(N)
    for t in range(N):
        runningAvg[t] = np.mean(scores[max(0, t-100):(t+1)])
    ax2.scatter(x, runningAvg, color='C1')
    ax2.axes.get_xaxis().set_visible(False)
    ax2.yaxis.tick_right()
    ax2.set_ylabel('Score', color='C1')
    ax2.yaxis.set_label_position('right')
    ax2.tick_params(axis='y', colors='C1')

    plt.savefig(filename)    

class RepeatActionAndMaxFrame(gym.Wrapper):
    def __init__(self, env=None, repeat=4):
        super(RepeatActionAndMaxFrame, self).__init__(env)
        self.repeat = repeat
        self.shape = env.observation_space.low.shape
        self.frameBuffer = np.zeros_like((2, self.shape))

    def step(self, action):
        tReward = 0.0
        done = False
        for i in range(self.repeat):
            obs, reward, done, info = self.env.step(action)
            tReward += reward
            index = i % 2
            self.frameBuffer[index] = obs
            if done:
                break
        
        maxFrame = np.maximum(self.frameBuffer[0], self.frameBuffer[1])
        return maxFrame, tReward, done, info

    def reset(self):
        obs = self.env.reset()
        self.frameBuffer = np.zeros_like((2, self.shape))
        self.frameBuffer[0] = obs
        return obs

class PreprocessFrame(gym.ObservationWrapper):
    def __init__(self, shape, env=None):
        super(PreprocessFrame, self).__init__(env)
        self.shape = (shape[2], shape[0], shape[1])
        self.observationSpace = gym.spaces.Box(low=0.0, high=1.0, shape=self.shape, dtype=np.float32)

    def observation(self, obs):
        newFrame = cv2.cvtColor(obs, cv2.COLOR_RGB2GRAY)
        resizedScreen = cv2.resize(newFrame, self.shape[1:], interpolation=cv2.INTER_AREA)
        newObs = np.array(resizedScreen, dtype=np.uint8).reshape(self.shape)
        newObs /= 255.0
        return newObs

class StackFrames(gym.ObservationWrapper):
    def __init__(self, env, repeat):
        super(StackFrames, self).__init__(env)
        self.observationSpace = gym.spaces.Box(env.observation_space.low.repeat(repeat, axis=0), env.observation_space.high.repeat(repeat, axis=0), dtype=np.float32)
        self.stack = collections.deque(maxlen=repeat)

    def reset(self):
        self.stack.clear()
        obs = self.env.reset()
        for _ in range(self.stack.maxlen):
            self.stack.append(obs)
        return np.array(self.stack).reshape(self.observationSpace.low.shape)

    def observation(self, obs):
        self.stack.append(obs)
        return np.array(self.stack).reshape(self.observationSpace.low.shape)

def makeEnv(envName, shape=(84, 84, 1), repeat=4):
    env = gym.make(envName)
    env = RepeatActionAndMaxFrame(env, repeat)
    env = PreprocessFrame(shape, env)
    env = StackFrames(env, repeat)
    return env