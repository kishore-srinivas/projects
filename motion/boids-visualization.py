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
        self.thetaToTarget = 0
        print(self.num, self.position)

    def fly(self):
        if (abs(self.thetaToTarget) <= self.maxTurnAngle):
            self.heading += self.thetaToTarget
            self.thetaToTarget = 0
        else:
            turn = self.maxTurnAngle if self.thetaToTarget >= 0 else -1*self.maxTurnAngle
            self.heading += turn
            self.thetaToTarget -= turn
        self.heading %= (2 * math.pi)

        dx = self.speed * math.cos(self.heading)
        dy = self.speed * math.sin(self.heading)
        delta = np.array([dx, dy])
        self.position += delta        
        
    '''
    @param theta - the desired heading, in radians
    '''
    def setTargetHeading(self, theta):
        theta %= (2*math.pi)
        self.heading %= (2*math.pi)
        self.thetaToTarget = (theta - self.heading) % math.pi
        # print(self.num, round(self.thetaToTarget, 3), round(self.heading, 3))

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
        return "num:" + str(self.num) + "\tpos:" + str(np.around(self.position, 3)) + "\tspeed:" + str(round(self.speed, 3)) + "\theading:" + str(round(self.heading, 3))

# create birds
birds = []
NUM_BIRDS = 25
FIELD_SIDE_LENGTH = 200
MAX_VEL = 3
ROI = [25, 2*math.pi/3]
MAX_TURN_ANGLE = math.pi/20
PERSONAL_SPACE = 5
for i in range(NUM_BIRDS):
    pos = np.array([-FIELD_SIDE_LENGTH/4, -FIELD_SIDE_LENGTH/4] + ROI[0]*2*np.random.random_sample((2,)))
    vel = MAX_VEL
    ori = math.pi/4
    b = Bird(i, pos, vel, ori, ROI, MAX_TURN_ANGLE, PERSONAL_SPACE)
    birds.append(b)

# create figure
fig = plt.figure()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0.5)
ax = fig.add_subplot(111, aspect='equal', autoscale_on=True, xlim=(-1*FIELD_SIDE_LENGTH/2, FIELD_SIDE_LENGTH/2), ylim=(-1*FIELD_SIDE_LENGTH/2, FIELD_SIDE_LENGTH/2))
ax.grid()

particles = []
for i in range(len(birds)):
    particles.append(ax.plot([], [], marker='$'+str(i)+'$', ms=4)[0])

def init():
    return particles

def animate(i):
    global birds
    global particles
    particles = []
    turnAngles = []
    debug = []
    for i in range(len(birds)):
        b = birds[i]

        # if bird has flown off the screen, turn it back towards the origin
        if (abs(b.getPosition()[0]) > 1.1 * FIELD_SIDE_LENGTH / 2 or
            abs(b.getPosition()[1]) > 1.1 * FIELD_SIDE_LENGTH / 2):
            x = b.getPosition()[0]
            y = b.getPosition()[1]
            mag = math.sqrt(x**2 + y**2)
            if (x > 0): # quadrant 1 or 4
                newHeading = np.arctan(y / x) + math.pi
            else: # quadrant 2 or 3
                newHeading = np.arctan(y / x)
            b.setTargetHeading(newHeading)
            debug.append([b.getNum(), b.getPosition(), round(newHeading, 3), round(b.getHeading(), 3)])
            b.fly()
            continue

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
            for j2 in range(1, n2):
                cur = birdsInPersonalSpace[j2]
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

        # average the valid conditions to find average turn angle
        count = 0
        count += 0 if (angleToAvgLocalHeading == 0) else 1
        count += 0 if (angleToAvgPos == 0) else 1
        count += 0 if (angleToAvoidCollision == 0) else 1
        headingToAvgLocalHeading = b.getHeading() + angleToAvgLocalHeading
        headingToAvgPos = b.getHeading() + angleToAvgPos
        headingToAvoidCollision = b.getHeading() + angleToAvoidCollision
        k1 = 1
        k2 = 1
        k3 = 1
        m = max(k1, k2, k3)
        k1 = k1 / m
        k2 = k2 / m
        k3 = k3 / m
        if (count == 0):
            targetHeading = b.getHeading()
        else:
            targetHeading = (k1*headingToAvgLocalHeading + k2*headingToAvgPos + k3*headingToAvoidCollision) / count
        b.setTargetHeading(targetHeading)
        # debug.append([round(angleToAvgLocalHeading, 3), round(angleToAvgPos, 3), round(angleToAvoidCollision, 3), round(targetHeading, 3)])

        # move birds one timestep forward and update the graphic
        b.fly()
        particles.append(ax.arrow(*b.getPosition(), 2*math.cos(b.getHeading()), 2*math.sin(b.getHeading()), 
            shape='full', head_starts_at_zero=True, width=1, ec="white"))
        particles.append(ax.plot(*b.getPosition(), marker='$'+str(i)+'$', ms=4)[0])
    for x in debug:
        print(x, end=" ")
    print()
    return particles

def display(i):
    res = []
    for b in birds:
        res.append(ax2.text(0, (-b.getNum()-1)*(FIELD_SIDE_LENGTH/(NUM_BIRDS+1)), b.getStatus(), fontsize=6))
    return res

ani = animation.FuncAnimation(fig, animate, frames=60, interval=10, blit=True, init_func=init)

# # second window to show debug information
# fig2 = plt.figure()
# ax2 = fig2.add_subplot(111, aspect='equal', autoscale_on=True, xlim=(0, FIELD_SIDE_LENGTH), ylim=(-1*FIELD_SIDE_LENGTH, 0))
# ani2 = animation.FuncAnimation(fig2, display, frames=60, interval=10, blit=True, init_func=init)

plt.show()