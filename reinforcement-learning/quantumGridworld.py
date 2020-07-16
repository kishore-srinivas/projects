import gym
import itertools
import matplotlib
import numpy as np
import pandas as pd
import sys

import warnings

import groverIteration as GI
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import execute, Aer

if "../" not in sys.path:
  sys.path.append("../") 

from collections import defaultdict
#from lib.envs.gridworld import GridworldEnv
# from lib import plotting

class GridworldEnv:
    def __init__(self):
        self.grid = [[1,  2,  3,  4,  5],
        			[ 6,  7,  8,  9, 10],
        			[11, 12, -1, 13, 14],
        			[15, 16, -1, 17, 18],
        			[19, 20, 21, 22, 23]]
        self.state = [0, 0]
        self.position = 1
		# self.actions = [0, 1, 2, 3] # left, up, right, down
        self.actions = {}
        self.actions['00']='UP'
        self.actions['01']='LEFT'
        self.actions['10']='DOWN'
        self.actions['11']='RIGHT'
        self.states = 23
        self.final_state = 23
        self.reward =  [[ 0, 0,   0, 0,  0],
                        [ 0, 0,   0, 0,  0],
                        [ 0, 0,   0, 0,  0],
                        [ 0, 0,   0, 0,  0],
                        [ 0, 0, -10, 0, 10]]
        self.done = False
    
    def reset(self):
        self.state = [0, 0]
        self.position = 1
        self.done = False

        return self.position
    
    def give_MDP_info(self):
        return self.states, len(self.actions), self.final_state
        
    def step(self, action):
        # action = self.actions[action]
        if action == '00':
            self.state[1] -= 1
        elif action == '01':
            self.state[0] -= 1
        elif action == '10':
            self.state[1] += 1
        elif action == '11':
            self.state[0] += 1

        if self.state[0] < 0:
            self.state[0] = 0
        elif self.state[0] > 4:
            self.state[0] = 4
        elif self.state[1] < 0:
            self.state[1] = 0
        elif self.state[1] > 4:
            self.state[1] = 4
        elif self.state[1] == 2 and (self.state[0] == 2 or self.state[0] == 3):
            if action == 0:
                self.state[1] = 3
            elif action == 1:
                self.state[0] = 4
            elif action == 2:
                self.state[1] = 1
            elif action == -1 or action == 3:
                self.state[0] = 1

        self.position = self.grid[self.state[0]][self.state[1]]
        reward = self.reward[self.state[0]][self.state[1]]

        if self.position == self.final_state:
            self.done = True
        return self.position, reward, self.done

def groverIteration(qc, qr, action, reward, nextStateValue):

    #if L < 2:
    k = 0.3
    L = int(k*(reward+nextStateValue)) #reward + value of the nextState, k is .3 which is arbitrary
    if(L > 1):
     	L = 1

    if(action == '00'):
        for x in range(L):
            qc, qr = GI.gIteration00(qc, qr)
    elif(action == '01'):
       	for x in range(L):
            qc, qr = GI.gIteration01(qc, qr)
    elif(action == '10'):
       	for x in range(L):
       	    qc, qr = GI.gIteration10(qc, qr)
    elif(action == '11'):
       	for x in range(L):
       	    qc, qr = GI.gIteration11(qc, qr)

    return qc, qr

def remember(eigenState, action, stateValue, nextStateValue, reward, done):
    memory[eigenState].append([action, stateValue, nextStateValue, reward, done])

    ### determines the action to make, collapses/measures the eigenAction into a move to make
def collapseActionSelectionMethod(qc, qr, cr):
    qc.measure(qr, cr)
    backend_sim = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend=backend_sim, shots=1024).result()
    counts = result.get_counts(qc)
    maxKey = list(counts.keys())[0]
    maxVal = counts[maxKey]
    for k in list(counts.keys()):
        if counts[k] > maxVal:
            maxKey = k
            maxVal = counts[k]
    classical_state = maxKey

    return classical_state

def q_learning(env, num_episodes, discount_factor=0.9, alpha=0.8):#, epsilon=0.1):
    """
    Q-Learning algorithm: Off-policy TD control. Finds the optimal greedy policy
    while following an epsilon-greedy policy
    
    Args:
        env: OpenAI environment.
        num_episodes: Number of episodes to run for.
        discount_factor: Gamma discount factor.
        alpha: TD learning rate.
        epsilon: Chance the sample a random action. Float betwen 0 and 1.
    
    Returns:
        A tuple (Q, episode_lengths).
        Q is the optimal action-value function, a dictionary mapping state -> action values.
        stats is an EpisodeStats object with two numpy arrays for episode_lengths and episode_rewards.
    """
    
    # The final action-value function.
    # A nested dictionary that maps state -> (action -> action-value).
    Q = defaultdict(lambda: np.zeros(env.action_space.n))
    memory = defaultdict(list)

    # Keeps track of useful statistics
    # stats = plotting.EpisodeStats(
    #     episode_lengths=np.zeros(num_episodes),
    #     episode_rewards=np.zeros(num_episodes))    
    
    # The policy we're following
    #policy = make_epsilon_greedy_policy(Q, epsilon, env.action_space.n)
    
    for i_episode in range(num_episodes):
        # Print out which episode we're on, useful for debugging.
        # print("Episode ", i_episode)
        if (i_episode + 1) % 100 == 0:
            print("Episode {}/{}".format(i_episode + 1, num_episodes))
            #sys.stdout.flush()
        
        # Reset the environment and pick the first action
        eigenState = env.reset()

        # One step in the environment
        # total_reward = 0.0
        for t in itertools.count():
            if eigenState in memory:
                memList = memory[eigenState]
                action = memList[0]
                stateValue = memList[1]
                nextState = memList[2]

                if nextState in memory:
                    nextStateValue = memory[nextState][1]
                else:
                    nextStateValue = 0.0
                reward = memList[3]

                qr = QuantumRegister(2)
                cr = ClassicalRegister(2)
                qc = QuantumCircuit(qr, cr)
                qc.h(qr)
                qc, qr = groverIteration(qc, qr, action, reward, nextStateValue)

            else:
                #################### Prepare the n-qubit registers #########################################
                qr = QuantumRegister(2)
                cr = ClassicalRegister(2)
                qc = QuantumCircuit(qr, cr)
                qc.h(qr)
                ############################################################################################

                stateValue = 0.0

            # print(qc)
            action = collapseActionSelectionMethod(qc, qr, cr)
            nextEigenState, reward, done = env.step(action)
            # print(nextEigenState)

            if nextEigenState in memory:
               	memList = memory[nextEigenState]
               	nextStateValue = memList[1]
            else:
            	nextStateValue = 0.0

            #Update state value
            stateValue = stateValue + alpha*(reward + (discount_factor * nextStateValue) - stateValue)
            #print(stateValue)

            memory[eigenState] = (action, stateValue, nextEigenState, reward)

            # stats.episode_rewards[i_episode] += (discount_factor ** t) * reward
            # stats.episode_lengths[i_episode] = t
            stats = None

            if done:
                break
                
            #state = next_state
            eigenState = nextEigenState
    
    return Q, stats, memory


warnings.simplefilter("ignore", DeprecationWarning)

matplotlib.style.use('ggplot')
env = GridworldEnv()
Q, stats, memory = q_learning(env, 500)

optimal_paths = {}
for state in sorted(list(memory.keys())):
    print(state, memory[state])
    arr = []
    originalState = state
    while True:
        arr.append(state)
        try:
            state = memory[state][2]
        except:
            break
    optimal_paths[originalState] = arr

print()
for s in sorted(list(optimal_paths.keys())):
    print(s, optimal_paths[s])

# plotting.plot_episode_stats(stats)