import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

def getX(s):
    return 26*s**3 - 40*s**2 + 15*s - 1

def getY(s):
    return -4*s**2 + 3*s

s = np.linspace(0, 1, 50)
x = getX(s)
y = getY(s)

fig = plt.figure(figsize=(6, 5))
fig.subplots_adjust(left=0, right=1, bottom=0.05, top=0.95)
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(-5, 5), ylim=(-5, 5))
ax.grid()

ax.plot(x, y)
plt.show()