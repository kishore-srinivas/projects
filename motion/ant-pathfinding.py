''' inspired by Coding Adventure: Ant and Slime Simulations by Sebastian Lague (https://www.youtube.com/watch?v=X-iSQQgOd1A) '''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

class Food:
    def __init__(self, pos, id = -1):
        self.pos = pos.astype(np.float64)
        self.id = id

    def getPos(self):
        return self.pos

    def getId(self):
        return self.id

class Ant:
    def __init__(self, pos, id, theta = np.pi/4, speed = 3, reach = 3):
        self.pos = pos.astype(np.float64)
        self.startPos = pos
        self.theta = theta
        self.id = id
        self.speed = speed
        self.reach = reach
        self.meals = []
        self.target = None

    def walk(self):
        dx = self.speed * np.cos(self.theta)
        dy = self.speed * np.sin(self.theta)
        delta = np.array([dx, dy])
        self.pos += delta

    def turnTo(self, angle):
        self.theta = angle

    def eat(self, food):
        self.meals.append(food)
        self.target = None

    def hasTarget(self):
        return (self.target != None)
    
    def getStartPos(self):
        return self.startPos

    def getPos(self):
        return self.pos

    def setPos(self, pos):
        self.pos = pos

    def getId(self):
        return self.id

    def getHeading(self):
        return self.theta

    def getSpeed(self):
        return self.speed

    def getReach(self):
        return self.reach

    def getMeals(self):
        return self.meals

NUM_ANTS = 2
NUM_FOOD = 15
FIELD_SIZE = 100
DIST_POW = 1

# create figure
fig = plt.figure(figsize=(6, 5))
fig.subplots_adjust(left=0, right=1, bottom=0.05, top=0.95)
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(0, FIELD_SIZE), ylim=(0, FIELD_SIZE))
ax.grid()

# place ants and foods randomly on the field
ants = []
for i in range(NUM_ANTS):
    randPos = np.array([np.random.randint(0, FIELD_SIZE), np.random.randint(FIELD_SIZE)])
    ants.append(Ant(randPos, i))
    ax.plot(*randPos, 'gs')
foods = []
for i in range(NUM_FOOD):
    randPos = np.array([np.random.randint(0, FIELD_SIZE), np.random.randint(FIELD_SIZE)])
    foods.append(Food(randPos, i))
    ax.plot(*randPos, 'bo')
eatenFoods = []

def plotPaths():
    print('plotting paths')

counter = 0
colors = ['r', 'g', 'b', 'k']

# handle key presses
def on_press(event):
    print('press', event.key)
    if event.key == 'right':
        global counter

        if (counter == len(foods) + 1):
            counter += 1
            plotPaths()
            return

        if (counter > len(foods)):
            return
        
        counter += 1
        for f in foods:
            ax.plot(*f.getPos(), 'bo')

        for a in ants:
            nextFood = None
            color = colors[a.getId()]

            # if this ant has visited all foods, return home
            if (len(a.getMeals()) == len(foods)):
                print(a.getId(), 'done')
                nextFood = Food(a.getStartPos())
            # else pick the next food
            else:
                probs = []
                for f in foods:
                    if f in a.getMeals():
                        probs.append(0)
                    else:
                        dist = np.linalg.norm(f.getPos() - a.getPos())
                        probs.append((1/dist) ** DIST_POW)
                # print(a.getId(), [f.getId() for f in foods], probs)
                nextFood = random.choices(foods, probs)[0]
                print(a.getId(), 'going to', nextFood.getId())

            # move ant to next food
            ax.plot([a.getPos()[0], nextFood.getPos()[0]], [a.getPos()[1], nextFood.getPos()[1]], color + '-', lw=1)
            a.setPos(nextFood.getPos())
            a.eat(nextFood)

            # redraw ant
            ax.plot(*a.getPos(), 'ro')
            ax.plot(*a.getStartPos(), 'gs')
        
        fig.canvas.draw()

fig.canvas.mpl_connect('key_press_event', on_press)


# # init function
# def init():
#     members = []
#     return members

# antsReturnedHome = 0
# # animate function, called repeatedly
# def animate(frame):
#     global antsReturnedHome
#     members = []

#     for a in ants:
#         # if this ant has visited all foods, return home
#         if (len(a.getMeals()) == len(foods)):
#             closestFood = Food(a.getStartPos())
#             # if at home, continue to next ant
#             if (np.linalg.norm(closestFood.getPos() - a.getPos()) < a.getReach()):
#                 antsReturnedHome += 1
#                 continue

#         # pick the next food
#         probs = []
#         for f in foods:
#             if f in a.getMeals():
#                 probs.append(0)
#             else:
#                 dist = np.linalg.norm(f.getPos() - a.getPos())
#                 probs.append((1/dist) ** DIST_POW)
#         nextFood = np.random.choice(foods, 1, probs)

#         # turn to face the next food
#         foodAngle = np.arctan2((nextFood.getPos()[1] - a.getPos()[1]), (nextFood.getPos()[0] - a.getPos()[0]))
#         a.turnTo(foodAngle)

#         # move towards the closest food
#         a.walk()

#         # eat the food when within reach
#         if (minDist < a.getReach()):
#             a.eat(closestFood)
#             # foods.remove(closestFood)
#             # eatenFoods.append(closestFood)

#         # plot the ant
#         members.append(ax.arrow(*a.getPos(), np.cos(a.getHeading()), np.sin(a.getHeading()), 
#             shape='full', head_starts_at_zero=True, width=1, ec="white", fc="red"))

#     # plot the foods
#     for f in foods:
#         members.append(ax.plot(*f.getPos(), 'bo')[0])
#     for ef in eatenFoods:
#         members.append(ax.plot(*ef.getPos(), 'kx')[0])

#     # if all ants are home, plot the paths they took
#     if (antsReturnedHome >= len(ants)):
#         plt.close(fig)
#         fig2 = plt.figure(figsize=(6, 5))
#         fig2.subplots_adjust(left=0, right=1, bottom=0.05, top=0.95)
#         ax2 = fig2.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(0, FIELD_SIZE), ylim=(0, FIELD_SIZE))

#         colors = ['r', 'g', 'b', 'k']
#         for j in range(len(ants)):
#             a = ants[j]

#             nodes = [m.getPos() for m in a.getMeals()]
#             nodes.append(a.getStartPos())
#             nodes.insert(0, a.getStartPos())
            
#             ax2.plot(*a.getStartPos(), 'gs')
#             for i in range(1, len(nodes)):
#                 ax2.arrow(nodes[i-1][0], nodes[i-1][1], nodes[i][0] - nodes[i-1][0], nodes[i][1] - nodes[i-1][1],
#                     shape='full', length_includes_head=True, head_starts_at_zero=True, width=0.1, ec=colors[j], fc=colors[j])

#             # ax2.plot([a.getStartPos()[0], a.getMeals()[0].getPos()[0]], [a.getStartPos()[1], a.getMeals()[0].getPos()[1]], colors[j] + '-', lw=1)
#             # for i in range(1, len(a.getMeals())):
#             #     ax2.plot([a.getMeals()[i-1].getPos()[0], a.getMeals()[i].getPos()[0]], [a.getMeals()[i-1].getPos()[1], a.getMeals()[i].getPos()[1]], colors[j] + '-', lw=1)
#             # ax2.plot([a.getMeals()[-1].getPos()[0], a.getStartPos()[0]], [a.getMeals()[-1].getPos()[1], a.getStartPos()[1]], colors[j] + '-', lw=1)

#         for f in foods:
#             ax2.plot(*f.getPos(), 'bo')
#         ax2.grid()
#         plt.show()
#         return []

#     return members

# ani = animation.FuncAnimation(fig, animate, frames=60, interval=1, blit=True, init_func=init)
plt.show()