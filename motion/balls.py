import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

f = open("debug.txt", "w")

class Ball:
    def __init__(self, pos, mass, radius, elasticity):
        self.pos = pos
        self.mass = mass
        self.radius = radius
        self.elasticity = elasticity
        self.vel = np.zeros_like(pos, float)
        self.acc = np.zeros_like(pos, float)
        print(self.pos[0])

    def move(self, force):
        self.acc = np.divide(force, self.mass)
        self.vel += self.acc * T
        self.pos += (self.vel * T) + (0.5 * self.acc * T**2)
        string = '{:.5f}'.format(self.pos[1]) + '\t' + '{:.5f}'.format(self.vel[1]) + '\t' + '{:.5f}'.format(self.acc[1]) + '\n'
        f.write(string)

    def getPosition(self):
        return self.pos

    def getMass(self):
        return self.mass

    def getVelocity(self):
        return self.vel

    def getElasticity(self):
        return self.elasticity

    def getRadius(self):
        return self.radius

# create balls
FIELD_SIDE_LENGTH = 100
NUM_BALLS = 1
MAX_RADIUS = 10
MAX_MASS = 10
GRAVITY = -9.81
T = 0.02 # the length of one time interval, constant for the whole program
balls = []
for i in range(NUM_BALLS):
    xPos = 0.0 #np.random.normal(loc=0, scale=0.3) * 20
    yPos = FIELD_SIDE_LENGTH
    pos = np.array([xPos, yPos])
    mass = MAX_MASS ** np.random.rand(1)[0]
    radius = MAX_RADIUS ** np.random.rand(1)[0]
    elasticity = np.random.normal(loc=0.7, scale=0.1)
    b = Ball(pos, mass, radius, elasticity)
    balls.append(b)

# create figure
fig = plt.figure()
fig.subplots_adjust(left=0, right=1, bottom=0.05, top=0.95)
ax = fig.add_subplot(111, aspect='equal', autoscale_on=True, xlim=(-1*FIELD_SIDE_LENGTH/2, FIELD_SIDE_LENGTH/2), ylim=(0, FIELD_SIDE_LENGTH))
ax.grid()

# stage parameters
lines = []
lines.append([-FIELD_SIDE_LENGTH/2, FIELD_SIDE_LENGTH/2, 10, 10])
lines.append([0, FIELD_SIDE_LENGTH/2, 10, 50])

# draw the stage from the stage parameters
for l in lines:
    ax.plot([l[0], l[1]], [l[2], l[3]], 'k-', lw=1)

particles = []
for i in range(len(balls)):
    particles.append(ax.plot([], [], 'bo', ms=4)[0])

def init():
    return particles

def animate(i):
    global balls
    global particles
    particles = []

    for i in range(len(balls)):
        b = balls[i]
        yPos = b.getPosition()[1]
        acc = np.array([0, GRAVITY])

        if (yPos < 10):
            impulse = b.getMass() * 2 * b.getVelocity()[1]
            force = (impulse / T) * b.getElasticity()
            acc = np.array([0, force / b.getMass()])

        b.move(acc * b.getMass())
        particles.append(ax.plot(*b.getPosition(), 'bo', ms=b.getRadius()/2)[0])

    return particles

ani = animation.FuncAnimation(fig, animate, frames=60, interval=1, blit=True, init_func=init)
plt.show()
f.close()