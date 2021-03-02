import math
import numpy as np

a = np.array([0, -9.81])
t = math.pi/4
b = np.array([math.cos(t), math.sin(t)])

print(b)
print(-9.81*b)

a = np.array([3, 0])
b = np.array([0, 1])
c = np.array([-1, 0.1])
print(np.cross(a, c)/(np.linalg.norm(a) * np.linalg.norm(c)))