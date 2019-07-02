import numpy as np
import math

r0 = 5
r1 = 3
r2 = 1

destination = np.array([4, 3])

def calcCost(radii, angles):
    return True

def calcTip(tail, radius, theta):
    x = tail[0] + radius * math.cos(theta)
    y = tail[1] + radius * math.sin(theta)
    return [round(x,3), round(y,3)]

'''
calculates the vector sum of multiple vectors
@param vectors - all the vectors to be summed, in the following format:
    [[r0, theta0], [r1, theta1], ...]
'''
def vectorSum(vectors):
    tail = [0, 0]
    for v in vectors:
        tail = calcTip(tail, v[0], v[1])
    return np.array([round(tail[0],3), round(tail[1],3)])

end = (vectorSum([[5, 0], [3, math.pi/2], [1, -math.pi]]))
print(end)
print(end - destination)