from grid import Grid
from agent import Agent
from qagent import QAgent

g = Grid(10, 6)
g.draw()
# a = Agent(g, 0.1)

# print(a.chooseAction())
# a.play(200)

qa = QAgent(g, 0.1)
g.draw()
qa.play(100)
qValues = qa.getQValues()
for k in qValues.keys():
    print(k)
    for k2 in qValues[k].keys():
        print("{}\t{}".format(k2, qValues[k][k2]))
qa.reset()

print()
reward = qa.grid.giveReward(qa.getPosition())
count = 0
while (reward != 1):
    print(qa.getPosition())
    action = qa.chooseAction(exp=0)
    print(action)
    qa.takeAction(action)
    reward = qa.grid.giveReward(qa.getPosition())
    g.draw()
    count += 1
print(qa.getPosition(), 'GOAL')
print(count, 'steps')