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
    def __init__(self, pos, id, theta = np.pi/4, speed = 5, reach = 3):
        self.pos = pos.astype(np.float64)
        self.startPos = pos
        self.theta = theta
        self.id = id
        self.speed = speed
        self.reach = reach
        self.meals = []
        self.target = None

    def step(self):
        if self.target == None:
            return

        # face towards target
        foodAngle = np.arctan2((self.target.getPos()[1] - self.getPos()[1]), (self.target.getPos()[0] - self.getPos()[0]))
        self.theta = foodAngle

        # move towards target
        dx = self.speed * np.cos(self.theta)
        dy = self.speed * np.sin(self.theta)
        delta = np.array([dx, dy])
        self.pos += delta

    def eat(self, food):
        self.meals.append(food)
        self.target = None

    def getTarget(self):
        return self.target

    def setTarget(self, target):
        self.target = target
    
    def getStartPos(self):
        return self.startPos

    def getPos(self):
        return self.pos

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

NUM_ANTS = 10
# NUM_FOOD = 10
FIELD_SIZE = 100
DIST_POW = 5

# create figure
fig = plt.figure(figsize=(6, 5))
fig.subplots_adjust(left=0, right=1, bottom=0.05, top=0.95)
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(0, FIELD_SIZE), ylim=(0, FIELD_SIZE))
ax.grid()

# place ants and foods randomly on the field
# foods = []
# for i in range(NUM_FOOD):
#     randPos = np.array([np.random.randint(0, FIELD_SIZE), np.random.randint(FIELD_SIZE)])
#     foods.append(Food(randPos, i))
#     ax.plot(*randPos, 'bo')
foods = []
foods.append(Food(np.array([25, 25]), 0))
foods.append(Food(np.array([50, 50]), 1))
foods.append(Food(np.array([50, 25]), 2))
foods.append(Food(np.array([25, 50]), 3))
foods.append(Food(np.array([75, 50]), 4))
foods.append(Food(np.array([75, 25]), 5))
ants = []
for i in range(NUM_ANTS):
    randFood = np.random.choice(foods)
    pos = randFood.getPos()
    ants.append(Ant(pos, i))
    print(i, 'starts at', randFood.getId())

def init():
    members = []
    return members

antsFinishedExploring = []
def animate(frame):
    global antsFinishedExploring
    members = []

    for a in ants:
        # if this ant has finished exploring, skip it
        if (a.getId() in antsFinishedExploring):
            continue
        
        nextFood = a.getTarget()
        if nextFood == None:
            # calculate the weighted distribution for the foods
            probs = []
            for f in foods:
                if f in a.getMeals():
                    probs.append(0)
                else:
                    dist = np.linalg.norm(f.getPos() - a.getPos())
                    if (dist < 0.001):
                        probs.append(0)
                    else:
                        probs.append((1/dist) ** DIST_POW)
            
            # if this ant has visited all foods stop working on this ant
            if (sum(probs) == 0):
                antsFinishedExploring.append(a.getId())
                continue

            # pick the next food from the weighted dist
            probs = np.array(probs) / sum(probs)
            nextFood = np.random.choice(foods, 1, p=probs)[0]
            # print(a.getId(), '-->', nextFood.getId())

            # set the next food as the ant's target
            a.setTarget(nextFood)

        # advance one step
        a.step()

        # eat food if within range
        if (np.linalg.norm(a.getPos() - nextFood.getPos()) < a.getReach()):
            a.eat(nextFood)

        # plot the ant
        members.append(ax.arrow(*a.getPos(), np.cos(a.getHeading()), np.sin(a.getHeading()), 
            shape='full', head_starts_at_zero=True, width=1, ec="white", fc="red"))

    # plot the foods
    for f in foods:
        members.append(ax.plot(*f.getPos(), 'bo')[0])        

    # if all ants are home, plot the paths they took
    if (len(antsFinishedExploring) >= NUM_ANTS):
        plt.close(fig)
        fig2 = plt.figure(figsize=(6, 5))
        fig2.subplots_adjust(left=0, right=1, bottom=0.05, top=0.95)
        ax2 = fig2.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(0, FIELD_SIZE), ylim=(0, FIELD_SIZE))

        colors = ['r', 'g', 'b', 'k']
        for j in range(NUM_ANTS):
            a = ants[j]

            nodes = [m.getPos() for m in a.getMeals()]
            nodes.append(a.getStartPos())
            nodes.insert(0, a.getStartPos())

            pathLength = 0 
            for i in range(1, len(nodes)):
                ax2.plot([nodes[i-1][0], nodes[i][0]], [nodes[i-1][1], nodes[i][1]], colors[j % len(colors)] + '-', lw=1)
                pathLength += np.linalg.norm(nodes[i-1] - nodes[i])
            print(a.getId(), [m.getId() for m in a.getMeals()], pathLength)
            
        for f in foods:
            ax2.plot(*f.getPos(), 'bo')
            ax2.text(*f.getPos(), f.getId())
        ax2.plot(*a.getStartPos(), 'gs')

        ax2.grid()
        plt.show()
        return []

    return members

ani = animation.FuncAnimation(fig, animate, frames=60, interval=1, blit=True, init_func=init)
plt.show()