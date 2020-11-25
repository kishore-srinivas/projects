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
        # print(self.num, 'off by', self.thetaToTarget)
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
        self.thetaToTarget = (theta - self.heading)
        if (self.thetaToTarget != math.pi):
            self.thetaToTarget %= math.pi
        # print(self.num, round(theta, 3), round(self.heading, 3), 'off by', round(self.thetaToTarget, 3))

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
NUM_BIRDS = 50
FIELD_SIDE_LENGTH = 200
MAX_VEL = 3
ROI = [25, 2*math.pi/3]
MAX_TURN_ANGLE = math.pi/20
PERSONAL_SPACE = 5
for i in range(NUM_BIRDS):
    pos = np.array([-FIELD_SIDE_LENGTH/4, -FIELD_SIDE_LENGTH/4] + 50*2*np.random.random_sample((2,)))
    vel = MAX_VEL
    ori = -math.pi/4
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
    for i in range(len(birds)):
        b = birds[i]
        count = 0

        b.setTargetHeading(b.getHeading())
        
        # if bird has flown off the screen, turn it back towards the origin
        if (abs(b.getPosition()[0]) > 0.75 * FIELD_SIDE_LENGTH / 2 or
            abs(b.getPosition()[1]) > 0.75 * FIELD_SIDE_LENGTH / 2):
            x = b.getPosition()[0]
            y = b.getPosition()[1]
            if (x > 0): # quadrant 1 or 4
                newHeading = np.arctan(y / x) + math.pi
            else: # quadrant 2 or 3
                newHeading = np.arctan(y / x)
            b.setTargetHeading(newHeading) 
            continue   

        factorsToConsider = {}
        factorsToConsider['avgHeading'] = b.getHeading()
        factorsToConsider['angleOfAvgPos'] = b.getHeading()
        factorsToConsider['angleToAvoidCollision'] = b.getHeading()

        # find birds nearby to influence current bird's actions
        birdsInRoi = []
        birdsInPersonalSpace = []
        for b2 in birds:
            if (b.getNum() != b2.getNum()):
                vect1 = b2.getPosition() - b.getPosition()
                dist = np.linalg.norm(vect1)
                if (dist <= ROI[0]):
                    birdsInRoi.append(b2)
                if (dist <= PERSONAL_SPACE):
                    birdsInPersonalSpace.append(b2)
        
        if (len(birdsInPersonalSpace) > 0):
            # steer away from birds in close proximity (separation)
            avgPosInPersonalSpace = sum(b2.getPosition() for b2 in birdsInPersonalSpace) / len(birdsInPersonalSpace)
            vectToAvgPosInPersonalSpace = avgPosInPersonalSpace - b.getPosition()
            factorsToConsider['angleToAvoidCollision'] = math.pi + np.arctan2(vectToAvgPosInPersonalSpace[1], vectToAvgPosInPersonalSpace[0])

        if (len(birdsInRoi) > 0):        
            # align heading with the birds it can see (alignment)
            # calculates avg heading by summing individual unit vectors and computing the angle from the resulting vector
            headingUVSX = sum(np.cos(b2.getHeading()) for b2 in birdsInRoi) # heading unit vector sum x
            headingUVSY = sum(np.sin(b2.getHeading()) for b2 in birdsInRoi) # heading unit vector sum y
            factorsToConsider['avgHeading'] = np.arctan2(headingUVSY, headingUVSX)

            # steer towards the center of mass of the birds it can see (cohesion)
            avgPos = sum(b2.getPosition() for b2 in birdsInRoi) / len(birdsInRoi)
            vectToAvgPos = avgPos - b.getPosition()
            factorsToConsider['angleOfAvgPos'] = np.arctan2(vectToAvgPos[1], vectToAvgPos[0])

        targetUVSX = targetUVSY = 0 # initialize target unit vector sum x and y
        for v in factorsToConsider.values():
            targetUVSX += np.cos(v)
            targetUVSY += np.sin(v)
        targetHeading = np.arctan2(targetUVSY, targetUVSX)
        b.setTargetHeading(targetHeading)
        
        if (i != 0):
            particles.append(ax.arrow(*b.getPosition(), math.cos(b.getHeading()), math.sin(b.getHeading()), 
                shape='full', head_starts_at_zero=False, width=1, ec="white")) 
        else:
            particles.append(ax.arrow(*b.getPosition(), math.cos(b.getHeading()), math.sin(b.getHeading()), 
                shape='full', head_starts_at_zero=False, width=1, ec="white", fc="red"))
            particles.append(ax.add_artist(plt.Circle((b.getPosition()[0], b.getPosition()[1]), ROI[0], fill=False))) 
            particles.append(ax.arrow(*b.getPosition(), 5*math.cos(factorsToConsider['avgHeading']), 5*math.sin(factorsToConsider['avgHeading']), 
                shape='full', head_starts_at_zero=False, width=1, ec="white", fc="orange"))

            # particles.append(ax.plot(*avgPos, 'bo')[0])
            # particles.append(ax.arrow(*b.getPosition(), math.cos(angleOfAvgPos), math.sin(angleOfAvgPos), 
            #     shape='full', head_starts_at_zero=True, width=1, ec="white", fc="green")) 
            for b2 in birdsInRoi:
                particles.append(ax.plot([b.getPosition()[0], b2.getPosition()[0]], [b.getPosition()[1], b2.getPosition()[1]], linewidth=0.5, color='green')[0])
                
        
        b.fly()

    return particles

def animate2(i):
    global birds
    global particles
    particles = []
    turnAngles = []
    debug = []
    for i in range(len(birds)):
        b = birds[i]
        count = 0

        # if bird has flown off the screen, turn it back towards the origin
        if (abs(b.getPosition()[0]) > 0.5 * FIELD_SIDE_LENGTH / 2 or
            abs(b.getPosition()[1]) > 0.5 * FIELD_SIDE_LENGTH / 2):
            count += 1
            x = b.getPosition()[0]
            y = b.getPosition()[1]
            # mag = math.sqrt(x**2 + y**2)
            if (x > 0): # quadrant 1 or 4
                newHeading = np.arctan(y / x) + math.pi
            else: # quadrant 2 or 3
                newHeading = np.arctan(y / x)
            b.setTargetHeading(newHeading)
            # print("{:d} off screen, new target: {:0.3f}".format(b.getNum(), newHeading))
            debug.append([b.getNum(), b.getPosition(), round(newHeading, 3), round(b.getHeading(), 3)])
            b.fly()
            continue

        # find birds nearby to influence current bird's actions
        birdsInRoi = []
        birdsInPersonalSpace = []
        for b2 in birds:
            if (b.getNum() == b2.getNum()):
                continue
            vect1 = b2.getPosition() - b.getPosition()
            dist = np.linalg.norm(vect1)
            if (dist <= b.getPersonalSpace()):
                birdsInPersonalSpace.append(b2)
            # if (dist <= ROI[0]):
            #     # check if angle between b and b2 is within tolerance
            #     thirdPoint = b.getPosition() + 5*np.array([math.cos(b.getHeading()), math.sin(b.getHeading())])
            #     vect2 = thirdPoint - b.getPosition()
            #     cosine_angle = np.dot(vect1, vect2) / (np.linalg.norm(vect1) * np.linalg.norm(vect2))
            #     angle = np.arccos(cosine_angle)
            #     if (abs(angle) < ROI[1]):
            #         birdsInRoi.append(b2)
            #         particles.append(ax.arrow(*b.getPosition(), dist * math.cos(b.getHeading() + angle), dist * math.sin(b.getHeading() + angle), 
            #             shape='full', head_starts_at_zero=False, width=1, ec="white", fc="blue"))
            if (dist <= ROI[0]):
                birdsInRoi.append(b2)
        
        # if any other birds are nearby, adjust heading accordingly
        if (len(birdsInRoi) > 0):
            count += 1
            n = len(birdsInRoi)
            avgPos = sum(b2.getPosition() for b2 in birdsInRoi) / n
            avgLocalHeading = (sum(b2.getHeading() for b2 in birdsInRoi) / n) % (2*math.pi)
            # particles.append(ax.plot(*avgPos, 'bo')[0])
            # particles.append(ax.arrow(*b.getPosition(), 10 * math.cos(avgLocalHeading), 10 * math.sin(avgLocalHeading), 
            #     shape='full', head_starts_at_zero=False, width=1, ec="white", fc="red"))

            p3 = b.getPosition() + np.array([math.cos(b.getHeading()), math.sin(b.getHeading())])
            vect1 = avgPos - b.getPosition()
            vect2 = p3 - b.getPosition()
            angleToAvgPos = b.getHeading() + np.arccos(np.dot(vect1, vect2) / (np.linalg.norm(vect1) * np.linalg.norm(vect2)))
            # particles.append(ax.arrow(*b.getPosition(), 10 * math.cos(angleToAvgPos), 10 * math.sin(angleToAvgPos), 
            #     shape='full', head_starts_at_zero=False, width=1, ec="white", fc="green"))

            # avgLocalHeading = (headingTotal / n) % (2*math.pi)
            angleToAvgLocalHeading = b.getHeading() - avgLocalHeading
        else:
            angleToAvgPos = 0
            angleToAvgLocalHeading = 0

        # steer away from birds in personal space to avoid collisions
        if (len(birdsInPersonalSpace) > 0):
            count += 1
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
        else:
            angleToAvoidCollision = 0

        # average the valid conditions to find average turn angle
        # print('count:', count)
        headingToAvgLocalHeading = angleToAvgLocalHeading
        headingToAvgPos = angleToAvgPos
        headingToAvoidCollision = angleToAvoidCollision
        k1 = 0
        k2 = 0
        k3 = 0
        m = max(k1, k2, k3)
        try:
            k1 = k1 / m
            k2 = k2 / m
            k3 = k3 / m
        except:
            pass
        targetHeading = b.getHeading()
        # if (count == 0):
        #     targetHeading = b.getHeading()
        # else:
        #     targetHeading = (k1*headingToAvgLocalHeading + k2*headingToAvgPos + k3*headingToAvoidCollision) / count
        # targetHeading = math.pi/2
        b.setTargetHeading(targetHeading)
        # print(b.getNum(), 'at', b.getHeading(), 'ordered to', targetHeading)
        # print("{:d}: {:0.3f} -> {:0.3f} | {:d}".format(b.getNum(), b.getHeading(), targetHeading, count))

        # move birds one timestep forward and update the graphic
        b.fly()
        particles.append(ax.arrow(*b.getPosition(), math.cos(b.getHeading()), math.sin(b.getHeading()), 
            shape='full', head_starts_at_zero=True, width=1, ec="white"))
        # particles.append(ax.arrow(*b.getPosition(), 2*math.cos(targetHeading), 2*math.sin(targetHeading), 
        #     shape='full', head_starts_at_zero=True, width=1, ec="white", fc="red"))
        # try:
        #     # particles.append(ax.plot(*avgPos, 'bo')[0])
        #     # particles.append(ax.arrow(*b.getPosition(), *(avgPos - b.getPosition()), 
        #     #     shape='full', head_starts_at_zero=False, width=1, ec="white", fc="green"))
        #     particles.append(ax.arrow(*b.getPosition(), math.cos(targetHeading), math.sin(targetHeading), 
        #         shape='full', head_starts_at_zero=False, width=1, ec="white", fc="red"))
        # except UnboundLocalError:
        #     pass
        # particles.append(ax.plot(*b.getPosition(), marker='$'+str(i)+'$', ms=4)[0])
        # particles.append(ax.add_artist(plt.Circle((b.getPosition()[0], b.getPosition()[1]), ROI[0], fill=False)))
    # print('----')

    return particles

def display(i):
    res = []
    for b in birds:
        res.append(ax2.text(0, (-b.getNum()-1)*(FIELD_SIDE_LENGTH/(NUM_BIRDS+1)), b.getStatus(), fontsize=6))
    return res

ani = animation.FuncAnimation(fig, animate, frames=60, interval=1, blit=True, init_func=init)

# # second window to show debug information
# fig2 = plt.figure()
# ax2 = fig2.add_subplot(111, aspect='equal', autoscale_on=True, xlim=(0, FIELD_SIDE_LENGTH), ylim=(-1*FIELD_SIDE_LENGTH, 0))
# ani2 = animation.FuncAnimation(fig2, display, frames=60, interval=10, blit=True, init_func=init)

plt.show()