import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Ball:
    def __init__(self, pos, mass, radius, elasticity, vel=np.array([0., 0.]), acc=np.array([0., 0.])):
        self.pos = pos
        self.mass = mass
        self.radius = radius
        self.elasticity = elasticity
        self.vel = vel
        self.acc = acc

    def move(self, force):
        self.acc = np.divide(force, self.mass)
        self.vel += self.acc * T
        self.pos += (self.vel * T) + (0.5 * self.acc * T**2)

    def getPosition(self):
        return self.pos

    def getMass(self):
        return self.mass

    def getVelocity(self):
        return self.vel

    def getVelocityDirection(self):
        x = self.vel[0]
        y = self.vel[1]
        length = np.linalg.norm(self.vel)
        return math.acos(x / length) * (1 if y >= 0 else -1)
        
    def getElasticity(self):
        return self.elasticity

    def getRadius(self):
        return self.radius

class Line:
    def __init__(self, p1, p2, kFriction=0.2):
        self.x1 = p1[0]
        self.y1 = p1[1]
        self.x2 = p2[0]
        self.y2 = p2[1]
        self.kFriction = kFriction

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

    def isPointOnLine(self, point, tolerance=0.5):
        p = point
        if (point[0] < min(self.x1, self.x2) or point[0] > max(self.x1, self.x2)):
            return False
        p1 = np.array([point[0], self.getY(point[0])])
        p2 = np.array([self.x2, self.y2])
        a = p - p1
        b = p2 - p1
        dot_product = np.dot(a, b)
        if (abs(dot_product - 1) < 0.00005):
            return True
        cos_theta = dot_product / (np.linalg.norm(a)*np.linalg.norm(b))
        theta = math.acos(cos_theta)
        sin_theta = math.sqrt(1 - cos_theta**2)
        dist = np.linalg.norm(a) * sin_theta
        return dist <= tolerance

    def getPoints(self):
        res = []
        res.append(self.x1)
        res.append(self.x2)
        res.append(self.y1)
        res.append(self.y2)
        return res

    def getKFriction(self):
        return self.kFriction

# create balls
FIELD_SIDE_LENGTH = 100
NUM_BALLS = 5
MAX_RADIUS = np.float64(10.0)
MAX_MASS = np.float64(10.0)
GRAVITY = 9.81
T = 0.02 # the length of one time interval, constant for the whole program
balls = []
for i in range(NUM_BALLS):
    xPos = np.random.normal(loc=0, scale=0.3) * 50
    yPos = FIELD_SIDE_LENGTH
    pos = np.array([xPos, yPos])
    mass = np.random.random() * MAX_MASS
    radius = mass * 2
    elasticity = np.random.normal(loc=0.7, scale=0.1)
    xVel = 0.0
    yVel = np.random.normal(loc=0, scale=0.3) * 3
    vel = np.array([xVel, yVel])
    b = Ball(pos, mass, radius, elasticity, vel)
    balls.append(b)

# create figure
fig = plt.figure()
fig.subplots_adjust(left=0, right=1, bottom=0.05, top=0.95)
ax = fig.add_subplot(111, aspect='equal', autoscale_on=True, xlim=(-1*FIELD_SIDE_LENGTH/2, FIELD_SIDE_LENGTH/2), ylim=(0, FIELD_SIDE_LENGTH))
ax.grid()

# stage parameters
lines = []
# horizontal lines
lines.append(Line([-FIELD_SIDE_LENGTH/2, 50], [0, 50]))
lines.append(Line([0, 30], [FIELD_SIDE_LENGTH/2, 30]))

# angled lines
# lines.append(Line([-FIELD_SIDE_LENGTH/2, 70], [FIELD_SIDE_LENGTH/8, 50]))
# lines.append(Line([-FIELD_SIDE_LENGTH/8, 10], [FIELD_SIDE_LENGTH/2, 30]))

# 45deg lines
# lines.append(Line([-30, 70], [10, 30]))
# lines.append(Line([40, 50], [0, 10]))

# 30deg lines
# lines.append(Line([10-20*math.sqrt(3), 70], [10, 50]))
# lines.append(Line([40, 50], [-20, -10]))

# lines.append([0, FIELD_SIDE_LENGTH/2, 10, 50])

# draw the stage from the stage parameters
for l in lines:
    points = l.getPoints()
    ax.plot([points[0], points[1]], [points[2], points[3]], 'k-', lw=2)

particles = []
for i in range(len(balls)):
    particles.append(ax.plot([], [], 'bo', ms=4)[0])

def init():
    return particles

def animate(j):
    global balls
    global particles
    particles = []

    for i in range(len(balls)):
        b = balls[i]
        acc = np.array([0, -GRAVITY])
        force = acc * b.getMass()
        vel = np.linalg.norm(b.getVelocity())

        for l in lines:
            if (l.isPointOnLine(b.getPosition())):
                angleOfNormal = l.getHeading() + math.pi/2
                lineAngle = l.getHeading()
                velAngle = b.getVelocityDirection()
                theta = abs((lineAngle - velAngle)) % math.pi
                vParallel = vel * math.cos(theta)
                vPerpendicular = vel * math.sin(theta)
                
                if (vPerpendicular > 2):
                    vfx = vel * math.cos(angleOfNormal)
                    vfy = vel * math.sin(angleOfNormal)
                    impulse = b.getMass() * (np.array([vfx, vfy]) - b.getVelocity())
                    force = (impulse / T) * b.getElasticity()
                else:
                    force = b.getMass() * GRAVITY * np.array([math.cos(angleOfNormal), math.sin(angleOfNormal)])

                # if (abs(GRAVITY - force[1]) < 0.001):
                #     force[1] = 0.0
                # particles.append(ax.arrow(*b.getPosition(), 10*math.cos(angleOfNormal), 10*math.sin(angleOfNormal),
                #     shape='full', head_starts_at_zero=True, width=1, ec="white", fc="green"))

        b.move(force)
        particles.append(ax.plot(*b.getPosition(), 'bo', ms=b.getRadius()/2)[0])
        # particles.append(ax.arrow(*b.getPosition(), *force,
        #             shape='full', head_starts_at_zero=True, width=1, ec="white", fc="red"))        
        # particles.append(ax.arrow(*b.getPosition(), vel*math.cos(b.getVelocityDirection()), vel*math.sin(b.getVelocityDirection()), 
        #     shape='full', head_starts_at_zero=True, width=1, ec="white"))

    return particles

ani = animation.FuncAnimation(fig, animate, frames=30, interval=0.5, blit=True, init_func=init)
plt.show()