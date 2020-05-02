import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def getMagnitude(vector):
    total = 0
    for i in vector:
        total += i**2
    return math.sqrt(total)

'''
redefining Bird using vectors for position, velocity, and acceleration
'''
class Bird2:
    def __init__(self, num, initialPosition, initialVelocity, initialAcceleration, maxVelocity, maxAcceleration, roi, personalSpace):
        self.num = num
        self.position = initialPosition
        self.velocity = initialVelocity
        self.acceleration = initialAcceleration
        self.maxVelocity = maxVelocity
        self.maxAcceleration = maxAcceleration
        self.roi = roi
        self.personalSpace = personalSpace
    
    def fly(self):
        self.velocity += self.acceleration
        if (getMagnitude(self.velocity) > self.maxVelocity):
            self.velocity = (self.velocity / getMagnitude(self.velocity)) * self.maxVelocity
        self.position += self.velocity
        print(self.position, self.velocity, self.acceleration)    

    def accelerate(self, force):
        self.acceleration += force #assumes mass is 1 (F=ma)
        if (getMagnitude(self.acceleration) > self.maxAcceleration):
            self.acceleration = (self.acceleration / getMagnitude(self.acceleration)) * self.maxAcceleration 

    def getNum(self):
        return self.num

    def getPosition(self):
        return self.position

    def getVelocity(self):
        return self.velocity

    def getAcceleration(self):
        return self.acceleration

    def getPersonalSpace(self):
        return self.personalSpace

# create birds
birds = []
NUM_BIRDS = 10
FIELD_SIDE_LENGTH = 200
MAX_VEL = 3
MAX_ACC = 10
ROI = [25, 2*math.pi/3]
PERSONAL_SPACE = 5
for i in range(NUM_BIRDS):
    pos = FIELD_SIDE_LENGTH/2 * np.random.random_sample((2,)) - FIELD_SIDE_LENGTH/4
    vel = MAX_VEL * np.random.random_sample((2,))
    acc = np.array([1, 0])
    b = Bird2(i, pos, vel, acc, MAX_VEL, MAX_ACC, ROI, PERSONAL_SPACE)
    birds.append(b)

# create figure
fig = plt.figure()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(-1*FIELD_SIDE_LENGTH/2, FIELD_SIDE_LENGTH/2), ylim=(-1*FIELD_SIDE_LENGTH/2, FIELD_SIDE_LENGTH/2))
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
    debug = []
    for i in range(len(birds)):
        b = birds[i]

        # # if bird has flown off the screen, reverse its heading to bring it back
        # if (abs(b.getPosition()[0]) > 1.1 * FIELD_SIDE_LENGTH / 2 or
        #     abs(b.getPosition()[1]) > 1.1 * FIELD_SIDE_LENGTH / 2):
        #     b.setTargetHeading(b.getHeading() + math.pi)

        # # find birds nearby to influence current bird's actions
        # birdsInRoi = []
        # birdsInPersonalSpace = []
        # for b2 in birds:
        #     if (b.getNum() == b2.getNum()):
        #         continue
        #     v1 = b.getPosition() - b2.getPosition()
        #     dist = np.linalg.norm(v1)
        #     if (dist <= b.getPersonalSpace()):
        #         birdsInPersonalSpace.append(b2)
        #     if (dist <= ROI[0]):
        #         # check if angle between b and b2 is within tolerance
        #         thirdPoint = b.getPosition() + np.array([math.cos(b.getHeading()), math.sin(b.getHeading())])
        #         v2 = thirdPoint - b.getPosition()
        #         cosine_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        #         angle = np.arccos(cosine_angle)
        #         if (angle < ROI[1]):
        #             birdsInRoi.append(b2)

        b.fly()
        # particles.append(ax.arrow(*b.getPosition(), 2*math.cos(b.getHeading()), 2*math.sin(b.getHeading()), 
            # shape='full', head_starts_at_zero=True, width=1, ec="white"))
        particles.append(ax.plot(*b.getPosition(), marker='$'+str(i)+'$', ms=4)[0])
    return particles

ani = animation.FuncAnimation(fig, animate, frames=60, interval=1000, blit=True, init_func=init)
plt.show()