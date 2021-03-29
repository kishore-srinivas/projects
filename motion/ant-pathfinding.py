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
        print(self.getId(), 'eating', food.getId())
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

NUM_ANTS = 2
NUM_FOOD = 10
FIELD_SIZE = 100
DIST_POW = 5

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

# init function
def init():
    members = []
    return members

antsReturnedHome = 0
# animate function, called repeatedly
def animate(frame):
    global antsReturnedHome
    members = []

    for a in ants:
        nextFood = a.getTarget()

        if nextFood == None:
            # if this ant has visited all foods, return home
            if (len(a.getMeals()) >= len(foods)):
                nextFood = Food(a.getStartPos())
                # if at home, continue to next ant
                if (np.linalg.norm(nextFood.getPos() - a.getPos()) < a.getReach()):
                    print(a.getId(), 'returned home')
                    antsReturnedHome += 1
                    continue
            # else pick the next food
            else:
                probs = []
                remaining = []
                for f in foods:
                    if not f in a.getMeals():
                        remaining.append(f)
                        dist = np.linalg.norm(f.getPos() - a.getPos())
                        probs.append((1/dist) ** DIST_POW)
                nextFood = np.random.choice(remaining, 1, probs)[0]
                print(a.getId(), '-->', nextFood.getId())

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
    for ef in eatenFoods:
        members.append(ax.plot(*ef.getPos(), 'kx')[0])

    # if all ants are home, plot the paths they took
    if (antsReturnedHome >= len(ants)):
        plt.close(fig)
        fig2 = plt.figure(figsize=(6, 5))
        fig2.subplots_adjust(left=0, right=1, bottom=0.05, top=0.95)
        ax2 = fig2.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(0, FIELD_SIZE), ylim=(0, FIELD_SIZE))

        colors = ['r', 'g', 'b', 'k']
        for j in range(len(ants)):
            a = ants[j]

            nodes = [m.getPos() for m in a.getMeals()]
            nodes.append(a.getStartPos())
            nodes.insert(0, a.getStartPos())
            
            ax2.plot(*a.getStartPos(), 'gs')
            for i in range(1, len(nodes)):
                ax2.arrow(nodes[i-1][0], nodes[i-1][1], nodes[i][0] - nodes[i-1][0], nodes[i][1] - nodes[i-1][1],
                    shape='full', length_includes_head=True, head_starts_at_zero=True, width=0.1, ec=colors[j], fc=colors[j])

            # ax2.plot([a.getStartPos()[0], a.getMeals()[0].getPos()[0]], [a.getStartPos()[1], a.getMeals()[0].getPos()[1]], colors[j] + '-', lw=1)
            # for i in range(1, len(a.getMeals())):
            #     ax2.plot([a.getMeals()[i-1].getPos()[0], a.getMeals()[i].getPos()[0]], [a.getMeals()[i-1].getPos()[1], a.getMeals()[i].getPos()[1]], colors[j] + '-', lw=1)
            # ax2.plot([a.getMeals()[-1].getPos()[0], a.getStartPos()[0]], [a.getMeals()[-1].getPos()[1], a.getStartPos()[1]], colors[j] + '-', lw=1)

        for f in foods:
            ax2.plot(*f.getPos(), 'bo')
        ax2.grid()
        plt.show()
        return []

    return members

ani = animation.FuncAnimation(fig, animate, frames=60, interval=1, blit=True, init_func=init)
plt.show()