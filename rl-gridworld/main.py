from grid import Grid
from agent import Agent
from qagent import QAgent

g = Grid(3, 4)
g.draw()
a = Agent(g, 0.1)
g.draw()

# print(a.chooseAction())
# a.play(200)

qa = QAgent(g, 0.1)
print('initial Q:\n', qa.getQValues())
qa.play(200)
print('final Q:\n', qa.getQValues())
