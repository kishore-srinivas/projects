import math
import numpy as np

def calcVectors(c, p1, p2):
    v1 = p1 - c
    v2 = p2 - c
    return [v1, v2]

center = np.array([0, 0])
p1 = np.array([0, 1])
p2 = np.array([1, 1])
v1, v2 = calcVectors(center, p1, p2)
print(v1, v2)

cosine_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
angle = np.arccos(cosine_angle)
print(angle)