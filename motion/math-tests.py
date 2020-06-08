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

    def getY(self, x):
        if (self.getSlope() == math.inf):
            return self.y1
        return self.getSlope() * (x - self.x1) + self.y1

    def isPointOnLine(self, point, tolerance=0.01):
        p = point
        if (point[0] < min(self.x1, self.x2) or point[0] > max(self.x1, self.x2)):
            return False
        p1 = np.array([point[0], self.getY(point[0])])
        p2 = np.array([self.x2, self.y2])
        a = p - p1
        b = p2 - p1
        if (np.linalg.norm(b) == 0):
            b = np.array([self.x1, self.y1]) - p1
        print(p, p1, p2, a, b)
        # if (np.linalg.norm(a) == 0):
        #     return True
        dot_product = np.dot(a, b)
        print(dot_product)
        if (abs(dot_product - 1) < 0.00005 and np.linalg.norm(a) <= 1.1*self.getLength()):
            return True
        cos_theta = dot_product / (np.linalg.norm(a)*np.linalg.norm(b))
        print(cos_theta)
        theta = math.acos(cos_theta)
        print(theta)
        sin_theta = math.sqrt(1 - cos_theta**2)
        print(sin_theta)
        dist = np.linalg.norm(a) * sin_theta
        print(dist)
        return dist <= tolerance

    def getPoints(self):
        res = []
        res.append(self.x1)
        res.append(self.x2)
        res.append(self.y1)
        res.append(self.y2)
        return res

l = Line([2, 0], [4, 0])
print(l.getLength())
print(l.isPointOnLine(np.array([3, 3.5])))
print(l.isPointOnLine(np.array([3.5, 3.25])))
print(l.isPointOnLine(np.array([4, 0.05])))

# p = np.array([2, 4])
# a = np.array([2, 2.5])
# b = np.array([3, 6])
# dot_product = np.dot(a-p, b-p)
# print(dot_product)
# cos_theta = dot_product / (np.linalg.norm(a-p)*np.linalg.norm(b-p))
# print(cos_theta)
# sin_theta = math.sqrt(1 - cos_theta**2)
# dist = np.linalg.norm(a-p) * sin_theta
# print(dist)

# theta = math.acos(np.linalg.norm(a-p)*np.linalg.norm(b-p))
# print(theta)
# print(np.linalg.norm((a-p)*math.sin(theta)))

def getDirection(vector):
    x = vector[0]
    y = vector[1]
    length = np.linalg.norm(vector)
    if (y >= 0):
        return math.acos(x / length)
    else:
        return 2 * math.pi - math.acos(x / length)
    # if (x >= 0):
    #     if (y >= 0):
    #         return math.asin(y / np.linalg.norm(vector))
    #     else:
    #         return math.acos(x / np.linalg.norm(vector))
    # else:
    #     return math.asin(y / np.linalg.norm(vector))

print(getDirection(np.array([1, 1])))
print(getDirection(np.array([-1, 1])))
print(getDirection(np.array([-1, -1])))
print(getDirection(np.array([1, -1])))

a = np.array([1, 2])
b = np.array([3, 4])
print(a+b)
print(a*b)

from tkinter import *
window = Tk() 
window.geometry('500x300') 

def display():
    # print(var1.get(), var2.get())
    print(var2.get())

# var1 = IntVar()
# Checkbutton(window, text="male", variable=var1).grid(row=0, sticky=W)
var2 = BooleanVar()
Checkbutton(window, text="text2", variable=var2).grid(row=1, sticky=W)
Button(window, text='Show', command=display).grid(row=4, sticky=W, pady=4)
# window.mainloop()

x = np.array([0,0])
x += np.array([1,4])
x += np.array([-4,4])
x += np.array([-2,3])
x += np.array([0,4])
x = x/4
print(x)

a = np.array([1,-1])
b = np.array([0,0])
c = b + np.array([math.cos(2*math.pi/3), math.sin(2*math.pi/3)])
vect1 = a - b
vect2 = c - b
angle = np.arccos(np.dot(vect1, vect2) / (np.linalg.norm(vect1) * np.linalg.norm(vect2)))
print(angle)
