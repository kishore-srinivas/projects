import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.lines as lines

class Pendulum:
    def __init__(self, pos, mass, length, theta=0, velocity=0, following=None):
        self.following = following
        self.mass = mass
        self.length = length
        self.theta = theta
        self.graphTheta = self.theta - math.pi/2
        self.velocity = velocity
        if (following == None):
            self.pos = pos
        else:
            self.pos = following.getTip()
        self.tip = self.pos + np.array([self.length * math.cos(self.graphTheta), self.length * math.sin(self.graphTheta)])


    def swing(self, force):
        acc = force * math.sin(self.theta)
        self.velocity += acc
        self.theta += self.velocity
        self.graphTheta = self.theta - math.pi/2
        try:
            self.pos = self.following.getTip()
        except:
            pass
        self.tip = self.pos + np.array([self.length * math.cos(self.graphTheta), self.length * math.sin(self.graphTheta)])

    def getPos(self):
        return self.pos

    def getTip(self):
        return self.tip

# create figure
fig = plt.figure()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(-20, 20), ylim=(-20, 20))
ax.grid()

objects = []
p1 = Pendulum(np.array([0, 0]), 20, 15, math.pi/3)
p2 = Pendulum(p1.getTip(), 1, 5, 3*math.pi/4, following=p1)
GRAVITY = -0.00981

def init():
    return objects

def animate(i):
    global objects
    objects = []
    p1.swing(GRAVITY)
    p2.swing(GRAVITY)
    objects.append(ax.add_line(lines.Line2D([p1.getPos()[0], p1.getTip()[0]], [p1.getPos()[1], p1.getTip()[1]])))
    objects.append(ax.add_line(lines.Line2D([p2.getPos()[0], p2.getTip()[0]], [p2.getPos()[1], p2.getTip()[1]])))
    objects.append(ax.plot(*p1.getTip(), 'ko', ms=4)[0])
    objects.append(ax.plot(*p2.getTip(), 'ko', ms=4)[0])
    return objects

ani = animation.FuncAnimation(fig, animate, frames=60, interval=10, blit=True, init_func=init)
plt.show()