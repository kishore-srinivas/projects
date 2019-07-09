import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

TWOPI = 2*np.pi

fig, ax = plt.subplots()

t = np.arange(0.0, TWOPI, 0.001)
s = np.sin(t)
l = plt.plot(t, s)

ax = plt.axis([0,TWOPI,-1,1])

redDot, = plt.plot([0], [np.sin(0)], 'ro')

def animate(i, f):
    redDot.set_data(i, f)
    return redDot,

# create animation using the animate() function
myAnimation = animation.FuncAnimation(fig, animate, fargs=[np.cos], frames=np.arange(0.0, TWOPI, 0.1), interval=10, blit=True, repeat=True)

plt.show()