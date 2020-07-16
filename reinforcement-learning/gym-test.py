import gym
import matplotlib.pyplot as plt
import sys

environments = ['Acrobot-v1', 'CartPole-v1', 'MountainCar-v0', 'MountainCarContinuous-v0', 'Pendulum-v0']
ENV_NUM = 2
env = gym.make(environments[ENV_NUM])
print(env.action_space)
print(env.observation_space)

rewards = {}
errors = {}
if (ENV_NUM == 0):
    pass
elif (ENV_NUM == 1):
    pass
elif (ENV_NUM == 2):
    for i_episode in range(5):
        observation = env.reset()
        arr = []
        arr.append(observation[0])
        arr2 = []
        for t in range(1000):
            env.render()
            action = env.action_space.sample()
            observation, reward, done, info = env.step(action)
            arr.append(observation[0])
            arr2.append(reward)
            if done:
                print("Episode finished after {} timesteps".format(t+1))
                print(observation, reward)
                break
        errors[i_episode] = arr
        rewards[i_episode] = arr2
elif (ENV_NUM == 3):
    pass
else:
    pass

fig, axs = plt.subplots(nrows=1, ncols=len(errors.keys()))
for i in range(len(errors.keys())):
    k = list(errors.keys())[i]
    axs[i].plot(errors[k])
    axs[i].plot(rewards[k])

plt.show()
env.close()