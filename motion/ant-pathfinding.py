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

NUM_ANTS = 5
NUM_FOOD = 10
NUM_ITERS = 10
FIELD_SIZE = 100
DIST_POW = 3 # how much to favor closer foods while picking the next target 
PHEROMONE_POW = 7 # how much to consider pheromone trails when picking the next target
LENGTH_POW = 5 # how much to punish longer paths when laying down pheromones

def init():
    members = []
    return members

def animate(frame):
    global antsFinishedExploring, pheromoneTrails, startFoodIds, shortestPathLengthFound
    members = []

    for a in ants:
        # if this ant has finished exploring, skip it
        if (a.getId() in antsFinishedExploring):
            continue
        
        nextFood = a.getTarget()
        if nextFood == None:
            # find the id of the food the ant is currently at
            curFoodId = startFoodIds[a.getId()]
            if (len(a.getMeals()) > 0):
                curFoodId = a.getMeals()[-1].getId()

            # calculate the weighted distribution for the foods
            probs = []
            for f in foods:
                if f in a.getMeals():
                    probs.append(0)
                else:
                    dist = np.linalg.norm(f.getPos() - a.getPos())
                    pheromone = (pheromoneTrails[curFoodId][f.getId()] ** PHEROMONE_POW) * dist
                    # print(dist, pheromone)
                    # pheromone = 0
                    if (dist < 0.001):
                        probs.append(pheromone)
                    else:
                        probs.append(
                            ((1/dist) ** DIST_POW) + 
                            (pheromone)
                        )
            # print(probs)
            
            # if this ant has visited all foods stop working on this ant
            if (sum(probs) == 0):
                antsFinishedExploring.append(a.getId())
                continue

            # pick the next food from the weighted dist
            probs = np.array(probs) / sum(probs)
            # print(probs)
            nextFood = np.random.choice(foods, 1, p=probs)[0]

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

    # if all ants are home, plot the paths they took
    if (len(antsFinishedExploring) >= NUM_ANTS):
        postRun()
        return []

    return members

# plot ant paths and lay pheromone trails, called after all ants have visited all foods
def postRun():
    plt.close(fig)
    fig2 = plt.figure('Paths', figsize=(6, 5))
    fig2.subplots_adjust(left=0, right=1, bottom=0.05, top=0.95)
    ax2 = fig2.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(0, FIELD_SIZE), ylim=(0, FIELD_SIZE))

    colors = ['r', 'g', 'b', 'k']
    pathLengths = []

    # plot each ant's path and compute path lengths
    for j in range(NUM_ANTS):
        a = ants[j]
        nodes = [m.getPos() for m in a.getMeals()]
        nodes.append(foods[startFoodIds[a.getId()]].getPos())
        nodes.insert(0, foods[startFoodIds[a.getId()]].getPos())

        pathLength = 0 
        for i in range(1, len(nodes)):
            ax2.plot([nodes[i-1][0], nodes[i][0]], [nodes[i-1][1], nodes[i][1]], colors[j % len(colors)] + '-', lw=1)
            pathLength += np.linalg.norm(nodes[i-1] - nodes[i])
        print(startFoodIds[a.getId()], '-->', [m.getId() for m in a.getMeals()], pathLength)
        pathLengths.append(pathLength)

    # update pheromones based on path lengths
    minPathLength = min(min(pathLengths), shortestPathLengthFound)
    print('min:', minPathLength)
    for j in range(NUM_ANTS):
        a = ants[j]
        pheromoneStrength = (minPathLength / pathLengths[j]) ** LENGTH_POW

        meals = [m for m in a.getMeals()]
        meals.append(foods[startFoodIds[a.getId()]])
        meals.insert(0, foods[startFoodIds[a.getId()]])

        for k in range(len(meals) - 1):
            fromMeal = meals[k]
            toMeal = meals[k+1]
            pheromoneTrails[fromMeal.getId()][toMeal.getId()] += pheromoneStrength #* np.linalg.norm(toMeal.getPos() - fromMeal.getPos())

    # import json
    # print(json.dumps(pheromoneTrails, indent=2))
        
    for f in foods:
        ax2.plot(*f.getPos(), 'bo')
        ax2.text(*f.getPos(), f.getId())

    ax2.grid()
    plt.show()

# place foods on the field
foods = []
for i in range(NUM_FOOD):
    randPos = np.array([np.random.randint(0, FIELD_SIZE), np.random.randint(FIELD_SIZE)])
    foods.append(Food(randPos, i))
# foods = []
# foods.append(Food(np.array([25, 25]), 0))
# foods.append(Food(np.array([50, 50]), 1))
# foods.append(Food(np.array([50, 25]), 2))
# foods.append(Food(np.array([25, 50]), 3))
# foods.append(Food(np.array([75, 50]), 4))
# foods.append(Food(np.array([75, 25]), 5))

# initialize all pheromone trails to 0
pheromoneTrails = {}
for f1 in foods:
    entry = {}
    for f2 in foods:
        entry[f2.getId()] = 0
    pheromoneTrails[f1.getId()] = entry
shortestPathLengthFound = np.inf

# run iterations
for i in range(NUM_ITERS):
    # create figure
    fig = plt.figure('Run {}/{}'.format(i+1, NUM_ITERS), figsize=(6, 5))    
    fig.subplots_adjust(left=0, right=1, bottom=0.05, top=0.95)
    ax = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(0, FIELD_SIZE), ylim=(0, FIELD_SIZE))
    ax.grid()

    # plot foods on grid
    for f in foods:
        ax.plot(*f.getPos(), 'bo')

    # visualize pheromone trails
    for p1 in pheromoneTrails:
        pos1 = foods[p1].getPos()
        maxFromP1 = max(pheromoneTrails[p1].values())
        for p2 in pheromoneTrails[p1]:
            pos2 = foods[p2].getPos()
            strength = pheromoneTrails[p1][p2]
            if (maxFromP1 != 0):
                strength /= maxFromP1
            ax.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]], 'g-', lw=1, alpha=strength)

    # place ants randomly on the field  
    startFoodIds = {}
    ants = []
    for i in range(NUM_ANTS):
        randFood = np.random.choice(foods)
        pos = randFood.getPos()
        ants.append(Ant(pos, i))
        startFoodIds[i] = randFood.getId()

    antsFinishedExploring = []

    ani = animation.FuncAnimation(fig, animate, frames=60, interval=1, blit=True, init_func=init)
    plt.show()