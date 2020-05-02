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
    @param maxTurnAngle - a float between 0 and pi representing the maximum turning angle of the bird over a single time step
    '''
    def __init__(self, num, initialPosition, initialSpeed, initialHeading, roi, maxTurnAngle, personalSpace):
        self.num = num
        self.position = initialPosition
        self.speed = initialSpeed
        self.heading = initialHeading
        self.roi = roi
        self.maxTurnAngle = maxTurnAngle
        self.personalSpace = personalSpace

    def fly(self):
        dx = self.speed * math.cos(self.heading)
        dy = self.speed * math.sin(self.heading)
        delta = np.array([dx, dy])
        self.position += delta

    '''
    turns the bird by theta radians if its magnitude is less than maxTurnAngle, else turns by maxTurnAngle
    @param theta - the angle to turn the bird by, in radians
    '''
    def turn(self, theta):
        if (abs(theta) <= self.maxTurnAngle):
            self.heading += theta
        else:
            self.heading += self.maxTurnAngle if theta >= 0 else -1*self.maxTurnAngle
        self.heading %= (2 * math.pi)

    def forceTurn(self, theta):
        self.heading += theta
        self.heading %= (2 * math.pi)

    def getNum(self):
        return self.num

    def getPosition(self):
        return self.position

    def getSpeed(self):
        return self.speed

    def getHeading(self):
        return self.heading

    def getPersonalSpace(self):
        return self.personalSpace

    def getStatus(self):
        return "num:" + str(self.num) + "\tpos:" + str(np.around(self.position, 3)) + "\tvel:" + str(round(self.speed, 3)) + "\tori:" + str(round(self.heading, 3))

# create birds
birds = []
NUM_BIRDS = 10
FIELD_SIDE_LENGTH = 200
MAX_VEL = 5
ROI = [10, 2*math.pi/3]
MAX_TURN_ANGLE = math.pi/2
PERSONAL_SPACE = 1
for i in range(NUM_BIRDS):
    pos = FIELD_SIDE_LENGTH/2 * np.random.random_sample((2,)) - FIELD_SIDE_LENGTH/4
    vel = MAX_VEL #* np.random.random_sample()
    ori = (2 * math.pi) * np.random.random_sample()
    b = Bird(i, pos, vel, ori, ROI, MAX_TURN_ANGLE, PERSONAL_SPACE)
    birds.append(b)

# create figure
fig = plt.figure()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(-1*FIELD_SIDE_LENGTH/2, FIELD_SIDE_LENGTH/2), ylim=(-1*FIELD_SIDE_LENGTH/2, FIELD_SIDE_LENGTH/2))
ax.grid()

particles = []
for i in range(len(birds)):
    particles.append(ax.plot([], [], marker='$'+str(i)+'$', ms=4)[0])
    # particles.append(ax.plot([], [], marker=(2, 1, 0), ms=7)[0])
    # particles.append(ax.arrow([], [], [], []))

def init():
    # for p in particles:
    #     p.set_data([], [])
    return particles

def animate(i):
    global birds
    global particles
    particles = []
    turnAngles = []
    debug = []
    for i in range(len(birds)):
        b = birds[i]
        # if bird has flown off the screen, reverse its heading to bring it back
        if (abs(b.getPosition()[0]) > 1.1 * FIELD_SIDE_LENGTH / 2 or
            abs(b.getPosition()[1]) > 1.1 * FIELD_SIDE_LENGTH / 2):
            b.forceTurn(math.pi)

        # find birds nearby to influence current bird's actions
        birdsInRoi = []
        birdsInPersonalSpace = []
        for b2 in birds:
            if (b.getNum() == b2.getNum()):
                continue
            v1 = b.getPosition() - b2.getPosition()
            dist = np.linalg.norm(v1)
            if (dist <= b.getPersonalSpace()):
                birdsInPersonalSpace.append(b2)
            if (dist <= ROI[0]):
                # check if angle between b and b2 is within tolerance
                thirdPoint = b.getPosition() + np.array([math.cos(b.getHeading()), math.sin(b.getHeading())])
                v2 = thirdPoint - b.getPosition()
                cosine_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
                angle = np.arccos(cosine_angle)
                if (angle < ROI[1]):
                    birdsInRoi.append(b2)
        
        # if any other birds are nearby, adjust heading accordingly
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
            p3 = b.getPosition() + np.array([math.cos(b.getHeading()), math.sin(b.getHeading())])
            vect1 = avgPos - b.getPosition()
            vect2 = p3 - b.getPosition()
            angleToAvgPos = np.arccos(np.dot(vect1, vect2) / (np.linalg.norm(vect1) * np.linalg.norm(vect2)))
            # print(i, b.getPosition(), angleToAvgPos)

            avgLocalHeading = (headingTotal / n) % (2*math.pi)
            angleToAvgLocalHeading = b.getHeading() - avgLocalHeading
            # print(i, b.getPosition(), round(b.getHeading(), 3), round(avgLocalHeading, 3), round(angleToAvgLocalHeading, 3))
        else:
            angleToAvgPos = 0
            angleToAvgLocalHeading = 0

        # steer away from birds in personal space to avoid collisions
        if (len(birdsInPersonalSpace) > 0):
            n2 = len(birdsInPersonalSpace)
            firstBird2 = birdsInPersonalSpace[0]
            xTotal2 = firstBird2.getPosition()[0]
            yTotal2 = firstBird2.getPosition()[1]
            for j in range(1, n):
                cur = birdsInPersonalSpace[j]
                xTotal2 += cur.getPosition()[0]
                yTotal2 += cur.getPosition()[1]
            avgPos2 = np.array([xTotal2 / n2, yTotal2 / n2])
            p = b.getPosition() + np.array([math.cos(b.getHeading()), math.sin(b.getHeading())])
            vect01 = avgPos2 - b.getPosition()
            vect02 = p - b.getPosition()
            angleToAvgLocalPos = np.arccos(np.dot(vect01, vect02) / (np.linalg.norm(vect01) * np.linalg.norm(vect02)))
            angleToAvoidCollision = angleToAvgLocalPos + math.pi
            # print(i, avgPos2)
        else:
            angleToAvoidCollision = 0

        # average the three conditions to find average turn angle
        toTurn = (angleToAvgLocalHeading + angleToAvgPos + angleToAvoidCollision) / 3
        b.forceTurn(toTurn)
        debug.append([round(angleToAvgLocalHeading, 3), round(angleToAvgPos, 3), round(angleToAvoidCollision, 3), round(toTurn, 3)])

        # move birds one timestep forward and update the graphic
        b.fly()
        particles.append(ax.arrow(*b.getPosition(), 2*math.cos(b.getHeading()), 2*math.sin(b.getHeading()), 
            shape='full', head_starts_at_zero=True, width=1, ec="white"))
        particles.append(ax.plot(*b.getPosition(), marker='$'+str(i)+'$', ms=4)[0])
    for x in range(len(debug)):
        if (sum(debug[x]) == 0):
            print(x, end=" ")
        else:
            print(debug[x], end=" ")
    print()
    return particles

ani = animation.FuncAnimation(fig, animate, frames=60, interval=1000, blit=True, init_func=init)

plt.show()