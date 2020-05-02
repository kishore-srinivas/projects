import math
import numpy as np

# def calcVectors(c, p1, p2):
#     v1 = p1 - c
#     v2 = p2 - c
#     return [v1, v2]

# center = np.array([0, 0])
# p1 = np.array([0, 1])
# p2 = np.array([1, 1])
# v1, v2 = calcVectors(center, p1, p2)
# print(v1, v2)

# cosine_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
# angle = np.arccos(cosine_angle)
# print(angle)

# arr = np.arange(10)
# avg = np.average(arr)
# print(avg)

# arr2 = np.arange(50).reshape((5, 10))
# # arr2.reshape((5, 10))
# print(arr2)
# for x in arr2:
#     print(np.average(x))
# print(arr2 * -1)

# x = 5
# print(x)
# x += 3
# print(x)

# v = np.array([2, 2])
# print(v)
# mag = math.sqrt(8)
# print(mag)
# v = v / mag * 1.5
# print(v)

theta = math.pi/6
heading = -math.pi/2
theta = theta % (2*math.pi)
heading = heading % (2*math.pi)
turn = (theta - heading) % math.pi
print(round(heading, 5), round(turn, 5), round(theta, 5))
# print((3.92 - math.pi * 2) % (2 * math.pi))