import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# f = open("debug.txt", "w")

class Ball:
    def __init__(self, pos, mass, radius, elasticity):
        self.pos = pos
        self.mass = mass
        self.radius = radius
        self.elasticity = elasticity
        self.vel = np.zeros_like(pos, float)
        self.acc = np.zeros_like(pos, float)

    def move(self, force):
        self.acc = np.divide(force, self.mass)
        self.vel += self.acc * T
        self.pos += (self.vel * T) + (0.5 * self.acc * T**2)
        # string = '{:.5f}'.format(self.pos[1]) + '\t' + '{:.5f}'.format(self.vel[1]) + '\t' + '{:.5f}'.format(self.acc[1]) + '\n'
        # f.write(string)

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

class Line:
    def __init__(self, p1, p2):
        self.x1 = p1[0]
        self.y1 = p1[1]
        self.x2 = p2[0]
        self.y2 = p2[1]

    def getSlope(self): 
        if (self.x1 == self.x2):
            return math.inf
        if (self.y1 == self.y2):
            return 0   
        return (self.y2 - self.y1) / (self.x2 - self.x1)
    
    def getHeading(self):
        return math.atan((self.y2-self.y1)/(self.x2-self.x1))

    def getLength(self):
        return math.sqrt((self.x2-self.x1)**2 + (self.y2-self.y1)**2)

    def getY(self, x):
        if (self.getSlope() == math.inf):
            return self.y1
        return self.getSlope() * (x - self.x1) + self.y1

    # TODO: change to use the distance from the point to the line
    def isPointOnLine(self, point, tolerance=0.5):
        p = point
        if (point[0] < min(self.x1, self.x2) or point[0] > max(self.x1, self.x2)):
            return False
        p1 = np.array([point[0], self.getY(point[0])])
        p2 = np.array([self.x2, self.y2])
        a = p - p1
        b = p2 - p1
        # print(p1, p2, a, b)
        dot_product = np.dot(a, b)
        # print(dot_product)
        if (abs(dot_product - 1) < 0.00005):
            return True
        cos_theta = dot_product / (np.linalg.norm(a)*np.linalg.norm(b))
        # print(cos_theta)
        theta = math.acos(cos_theta)
        # print(theta)
        sin_theta = math.sqrt(1 - cos_theta**2)
        # print(sin_theta)
        dist = np.linalg.norm(a) * sin_theta
        # print(dist, dist <= tolerance)
        return dist <= tolerance

    def getPoints(self):
        res = []
        res.append(self.x1)
        res.append(self.x2)
        res.append(self.y1)
        res.append(self.y2)
        return res

# create balls
FIELD_SIDE_LENGTH = 100
NUM_BALLS = 3
MAX_RADIUS = 10
MAX_MASS = 10
GRAVITY = -9.81
T = 0.02 # the length of one time interval, constant for the whole program
balls = []
for i in range(NUM_BALLS):
    xPos = np.random.normal(loc=0, scale=0.3) * 20
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
lines.append(Line([-FIELD_SIDE_LENGTH/2, 50], [0, 50]))
lines.append(Line([0, 30], [FIELD_SIDE_LENGTH/2, 30]))

# lines.append([0, FIELD_SIDE_LENGTH/2, 10, 50])

# draw the stage from the stage parameters
for l in lines:
    points = l.getPoints()
    ax.plot([points[0], points[1]], [points[2], points[3]], 'k-', lw=1)

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

        # print(lines[0].isPointOnLine(b.getPosition()))
        for l in lines:
            if (l.isPointOnLine(b.getPosition())):
                impulse = -1 * b.getMass() * 2 * b.getVelocity()[1]
                force = (impulse / T) * b.getElasticity()
                acc = np.array([0, force / b.getMass()])

        b.move(acc * b.getMass())
        particles.append(ax.plot(*b.getPosition(), 'bo', ms=b.getRadius()/2)[0])

    return particles

ani = animation.FuncAnimation(fig, animate, frames=60, interval=1, blit=True, init_func=init)
plt.show()
# f.close()