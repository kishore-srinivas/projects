# based on the algorithm described on this page: http://www.red3d.com/cwr/boids/

import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Bird:
    '''
    constructs a Bird object
    @param num - the integer id of the bird
    @param initialPosition - a numpy array with 2 elements representing the x and y position of the bird
    @param initialSpeed - a float representing the initial speed of the bird
    @param initialHeading - a float representing the initial heading of the bird in radians
    @param roi - an array of 2 floats (in the format of [distance, angle]) representing the bird's region of interest when making a decision
    '''
    def __init__(self, num, initialPosition, initialSpeed, initialHeading, roi):
        self.num = num
        self.position = initialPosition
        self.speed = initialSpeed
        self.heading = initialHeading
        self.roi = roi

    def fly(self):
        dx = self.speed * math.cos(self.heading)
        dy = self.speed * math.sin(self.heading)
        delta = np.array([dx, dy])
        self.setPosition(self.position + delta)

    def turn(self, newHeading):
        self.heading = newHeading

    def setPosition(self, pos):
        self.position = pos
    
    def setSpeed(self, speed):
        self.speed = speed

    def setHeading(self, heading):
        self.heading = heading

    def getNum(self):
        return self.num

    def getPosition(self):
        return self.position

    def getSpeed(self):
        return self.speed

    def getHeading(self):
        return self.heading

    def getStatus(self):
        return "num:" + str(self.num) + "\tpos:" + str(np.around(self.position, 3)) + "\tvel:" + str(round(self.speed, 3)) + "\tori:" + str(round(self.heading, 3))

# create birds
birds = []
NUM_BIRDS = 10
FIELD_SIDE_LENGTH = 200
MAX_VEL = 5
ROI = [10, 2*math.pi/3]
for i in range(NUM_BIRDS):
    pos = FIELD_SIDE_LENGTH/2 * np.random.random_sample((2,)) - FIELD_SIDE_LENGTH/4
    vel = MAX_VEL * np.random.random_sample()
    ori = (2 * math.pi) * np.random.random_sample()
    b = Bird(i, pos, vel, ori, ROI)
    birds.append(b)

# create figure
fig = plt.figure()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(-1*FIELD_SIDE_LENGTH/2, FIELD_SIDE_LENGTH/2), ylim=(-1*FIELD_SIDE_LENGTH/2, FIELD_SIDE_LENGTH/2))
ax.grid()

particles = []
for i in range(len(birds)):
    particles.append(ax.plot([], [], marker='$'+str(i)+'$', ms=4)[0])
    # particles.append(ax.plot([], [], marker=(4, 0), ms=4)[0])

def init():
    for p in particles:
        p.set_data([], [])
    return particles

def animate(i):
    global birds
    for i in range(len(birds)):
        b = birds[i]
        birdsInRoi = []
        for b2 in birds:
            if (b.getNum() == b2.getNum()):
                continue
            v1 = b.getPosition() - b2.getPosition()
            dist = np.linalg.norm(v1)
            if (dist <= ROI[0]):
                # check if angle between b and b2 is within tolerance
                thirdPoint = b.getPosition() + np.array([math.cos(b.getHeading()), math.sin(b.getHeading())])
                v2 = thirdPoint - b.getPosition()
                cosine_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
                angle = np.arccos(cosine_angle)
                if (angle < ROI[1]):
                    birdsInRoi.append(b2)
        
        if (len(birdsInRoi) > 0):
            n = len(birdsInRoi)
            firstBird = birdsInRoi[0]
            xTotal = firstBird.getPosition()[0]
            yTotal = firstBird.getPosition()[1]
            headingTotal = firstBird.getHeading()
            for j in range(1, n):
                cur = birdsInRoi[j]
                xTotal += cur.getPosition()[0]
                yTotal += cur.getPosition()[1]
                headingTotal += cur.getHeading()
            avgPos = np.array([xTotal / n, yTotal / n])
            avgHeading = headingTotal / n
            
            prevHeading = b.getHeading()
            b.setHeading(avgHeading)
            curHeading = b.getHeading()
            if (abs(prevHeading - curHeading) > 0.01):
                print(i, ":", prevHeading, "-->", b.getHeading())

        b.fly()
        particles[i].set_data(*b.getPosition())
    return particles

ani = animation.FuncAnimation(fig, animate, frames=60, interval=1000, blit=True, init_func=init)

plt.show()