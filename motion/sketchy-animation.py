import numpy as np
import math
import matplotlib.pyplot as plt
import time
from scipy import integrate

v0_x = 0
p0_x = 0
def a_x(t):
    if (t < 1):
        return t
    elif (t < 3):
        return t/2
    else:
        return t/5
def v_x(t):
    return v0_x + (integrate.quad(a_x, 0, t)[0])
def p_x(t):
    return p0_x + (integrate.quad(v_x, 0, t)[0])

v0_y = 0
p0_y = 0
def a_y(t):
    return -9.81
def v_y(t):
    return v0_y + (integrate.quad(a_y, 0, t)[0])
def p_y(t):
    return p0_y + (integrate.quad(v_y, 0, t)[0])

plt.ion()
for t in np.arange(1, 5, 0.1):
    plt.cla()
    x = p_x(t)
    y = p_y(t)
    plt.scatter(x, y, c='tab:blue')
    plt.xlim(0, 50)
    plt.ylim(-50, 0)
    # plt.scatter(0, 0)
    plt.draw()
    plt.pause(0.001)
plt.ioff()
plt.show()