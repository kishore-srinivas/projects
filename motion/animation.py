import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
#xdata, ydata1, ydata2 = [], [], []
xdata, ydata = [], [[0], []]
ln1, = plt.plot([], [], 'ro')
ln2, = plt.plot([], [], 'b+')

def init():
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    return ln1, ln2,

def update(frame):
    xdata.append(np.cos(frame))
    ydata[0][0] = np.sin(frame)
    ydata[1].append(frame - np.pi)
    ln1.set_data(xdata[-1], ydata[0])
    ln2.set_data(xdata, ydata[1])
    return ln1, ln2,

ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                    init_func=init, blit=True, interval=5)
plt.show()