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

# theta = math.pi/6
# heading = -math.pi/2
# theta = theta % (2*math.pi)
# heading = heading % (2*math.pi)
# turn = (theta - heading) % math.pi
# print(round(heading, 5), round(turn, 5), round(theta, 5))
# # print((3.92 - math.pi * 2) % (2 * math.pi))

# def f(x, y):
#     return -0.1*x + 0.02*x*y

# x0 = 0
# y0 = 6
# h = 5

# while (x0 < 100):
#     xn = x0 + h
#     yn = round(y0 + h * f(x0, y0), 6)
#     print(round(xn, 2), '\t', yn)
#     x0 = xn
#     y0 = yn

# arr = np.array([4, -3])
# print(abs(arr))
# print(np.linalg.norm(arr))

# a = math.sqrt(2)
# print(a - 1.414 < 0.05)

class Line:
    def __init__(self, p1, p2):
        self.x1 = p1[0]
        self.y1 = p1[1]
        self.x2 = p2[0]
        self.y2 = p2[1]

    def getSlope(self):    
        return (self.y2 - self.y1) / (self.x2 - self.x1)
    
    def getHeading(self):
        return math.atan((self.y2-self.y1)/(self.x2-self.x1))

    def getLength(self):
        return math.sqrt((self.x2-self.x1)**2 + (self.y2-self.y1)**2)

    def isPointOnLine(self, point, tolerance=0.5):
        if (abs(((point[1] - self.y1) / (point[0] - self.x1)) - self.getSlope()) > tolerance):
            print((point[1] - self.y1) / (point[0] - self.x1), self.getSlope())
            return False
        # if (point[0] > self.x1 and point[0] > self.x2 or
        #     point[0] < self.x1 and point[0] < self.x2):
        #     print('out of x')
        #     return False
        # if (point[1] > self.y1 and point[1] > self.y2 or
        #     point[1] < self.y1 and point[1] < self.y2):
        #     print('out of y')
        #     return False
        return True

    def getPoints(self):
        res = []
        res.append(self.x1)
        res.append(self.x2)
        res.append(self.y1)
        res.append(self.y2)
        return res

l = Line([-50, 10], [50, 10])
print(l.isPointOnLine(np.array([0, 10])))
print(l.isPointOnLine(np.array([-8.8583011, 10.15021])))
print(l.isPointOnLine(np.array([-8.8583011, 11.65021])))

p = np.array([2, 4])
a = np.array([2, 2.5])
b = np.array([3, 6])
dot_product = np.dot(a-p, b-p)
print(dot_product)
cos_theta = dot_product / (np.linalg.norm(a-p)*np.linalg.norm(b-p))
print(cos_theta)
sin_theta = math.sqrt(1 - cos_theta**2)
dist = np.linalg.norm(a-p) * sin_theta
print(dist)

# theta = math.acos(np.linalg.norm(a-p)*np.linalg.norm(b-p))
# print(theta)
# print(np.linalg.norm((a-p)*math.sin(theta)))