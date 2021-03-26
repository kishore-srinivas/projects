''' inspired by Coding Adventure: Ant and Slime Simulations by Sebastian Lague (https://www.youtube.com/watch?v=X-iSQQgOd1A) '''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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

    def walk(self):
        dx = self.speed * np.cos(self.theta)
        dy = self.speed * np.sin(self.theta)
        delta = np.array([dx, dy])
        self.pos += delta

    def turnTo(self, angle):
        self.theta = angle

    def eat(self, food):
        self.meals.append(food)

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

NUM_ANTS = 3
NUM_FOOD = 15
FIELD_SIZE = 100

# create figure
fig = plt.figure(figsize=(6, 5))
fig.subplots_adjust(left=0, right=1, bottom=0.05, top=0.95)
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(0, FIELD_SIZE*1.5), ylim=(0, FIELD_SIZE*1.5))

# place ants and foods randomly on the field
ants = []
for i in range(NUM_ANTS):
    randPos = np.array([np.random.randint(0, FIELD_SIZE), np.random.randint(FIELD_SIZE)])
    ants.append(Ant(randPos, i))
foods = []
for i in range(NUM_FOOD):
    randPos = np.array([np.random.randint(0, FIELD_SIZE), np.random.randint(FIELD_SIZE)])
    foods.append(Food(randPos, i))
eatenFoods = []

antsReturnedHome = 0
while (antsReturnedHome < len(ants)):
    ax.grid()

    for a in ants:
        ax.plot(*a.getStartPos(), 'gs')

        # find the closest food
        closestFood = None
        minDist = np.inf
        for f in foods:
            dist = np.linalg.norm(f.getPos() - a.getPos())
            if (dist < minDist):
                minDist = dist
                closestFood = f

        # if no foods remain, return home
        if (closestFood == None):
            closestFood = Food(a.getStartPos())
            # if at home, continue to next ant
            if (np.linalg.norm(closestFood.getPos() - a.getPos()) < a.getReach()):
                antsReturnedHome += 1
                continue

        # turn to face the closest food
        foodAngle = np.arctan2((closestFood.getPos()[1] - a.getPos()[1]), (closestFood.getPos()[0] - a.getPos()[0]))
        a.turnTo(foodAngle)

        # move towards the closest food
        a.walk()

        # eat the food when within reach
        if (minDist < a.getReach()):
            a.eat(closestFood)
            foods.remove(closestFood)
            eatenFoods.append(closestFood)

        # plot the ant
        ax.arrow(*a.getPos(), np.cos(a.getHeading()), np.sin(a.getHeading()), 
            shape='full', head_starts_at_zero=True, width=1, ec="white", fc="red")

    # plot the foods
    for f in foods:
        ax.plot(*f.getPos(), 'bo')
    for ef in eatenFoods:
        ax.plot(*ef.getPos(), 'kx')
    plt.pause(0.000000001)
    plt.cla()

for a in ants:
    ax.plot(*a.getStartPos(), 'gs')
    ax.plot([a.getStartPos()[0], a.getMeals()[0].getPos()[0]], [a.getStartPos()[1], a.getMeals()[0].getPos()[1]], 'r-', lw=1)
    for i in range(1, len(a.getMeals())):
        ax.plot([a.getMeals()[i-1].getPos()[0], a.getMeals()[i].getPos()[0]], [a.getMeals()[i-1].getPos()[1], a.getMeals()[i].getPos()[1]], 'r-', lw=1)
    ax.plot([a.getMeals()[-1].getPos()[0], a.getStartPos()[0]], [a.getMeals()[-1].getPos()[1], a.getStartPos()[1]], 'r-', lw=1)

for ef in eatenFoods:
    ax.plot(*ef.getPos(), 'kx')
ax.grid()

plt.show()