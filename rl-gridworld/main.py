from grid import Grid
from agent import Agent
from qagent import QAgent

g = Grid(3, 4)
g.draw()
a = Agent(g, 0.1)
g.draw()

# print(a.chooseAction())
# a.play(200)

qa = QAgent(g, 0.3)
qValues = qa.getQValues()
for k in qValues.keys():
    print(k)
    for k2 in qValues[k].keys():
        print("{}\t{}".format(k2, qValues[k][k2]))
qa.play(1000)
qValues = qa.getQValues()
for k in qValues.keys():
    print(k)
    for k2 in qValues[k].keys():
        print("{}\t{}".format(k2, qValues[k][k2]))
g.draw()

print()
reward = qa.grid.giveReward(qa.getPosition())
while (reward != 1):
    print(qa.getPosition())
    action = qa.chooseAction(exp=0)
    print(action)
    qa.takeAction(action)
    reward = qa.grid.giveReward(qa.getPosition())
    g.draw()
print(qa.getPosition(), 'GOAL')

