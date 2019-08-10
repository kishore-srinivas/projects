import numpy as np
import cv2
from tkinter import *
import math
import time

''' pseudocode:
read in image in color and grayscale
read in sensitivity values
define color clusters based on sensitivity
    strictest sensitivity is purest color
    least strict sensitivity is the most mixed it can be and still be considered that color
classify pixel as a specific cluster
'''

original = cv2.imread('images\\abstract.jpg')
grayscale = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

'''
calculates the euclidean distance between a pixel and a color with a specific bias
@param pixel - the pixel to compare
@param color - the BGR color to compare to
@param bias - the weight to give to each color channel (a higher bias makes it harder to be classified as that color)
'''
def euclideanDistance(pixel, color, bias):
    for i in range(len(bias)):
        if (bias[i] < 0):
            bias[i] = 0
    deltaBlue = (pixel[0] - color[0]) * bias[0]
    deltaGreen = (pixel[1] - color[1]) * bias[1]
    deltaRed = (pixel[2] - color[2]) * bias[2]
    return math.sqrt(deltaBlue ** 2 + deltaGreen ** 2 + deltaRed ** 2)

def isColor(pixel, color, tolerance, bias=[1, 1, 1]):
    distance = euclideanDistance(pixel, color, bias)
    return distance <= tolerance

def update(color, biases):    
    print(color, biases)
    combo = np.zeros_like(original)
    for y in range(np.shape(original)[0]):
        for x in range(np.shape(original)[1]):
            if (isColor(original[y, x], color, 150, biases)):
                combo[y, x] = original[y, x]
            else:
                combo[y, x] = grayscale[y, x]

    result = combo
    cv2.imshow('result', result)
    # cv2.waitKey(0)

cv2.namedWindow('result', cv2.WINDOW_NORMAL)
cv2.imshow('result', original)
# cv2.waitKey(0)

def main():
    update([w1.get(), w2.get(), w3.get()], [w4.get(), w5.get(), w6.get()])

master = Tk()
w1 = Scale(master, label='Blue', from_=0, to=255, resolution=1, orient=HORIZONTAL)
w1.pack()
w2 = Scale(master, label='Green', from_=0, to=255, resolution=1, orient=HORIZONTAL)
w2.pack()
w3 = Scale(master, label='Red', from_=0, to=255, resolution=1, orient=HORIZONTAL)
w3.pack()
w4 = Scale(master, label='Blue bias', from_=0, to=15, resolution=0.25, orient=HORIZONTAL)
w4.pack()
w5 = Scale(master, label='Green bias', from_=0, to=15, resolution=0.25, orient=HORIZONTAL)
w5.pack()
w6 = Scale(master, label='Red bias', from_=0, to=15, resolution=0.25, orient=HORIZONTAL)
w6.pack()
Button(master, text='Update', command=main).pack()

mainloop()

# combo = np.zeros_like(original)
# shape = np.shape(original)
# for y in range(shape[0]):
#     for x in range(shape[1]):
#         found = False
#         if (blueRange[0] <= original[y, x, 0] <= blueRange[1]):
#             combo[y, x, 0] = original[y, x, 0]
#             found = True
#         elif (greenRange[0] <= original[y, x, 1] <= greenRange[1]):
#             combo[y, x, 1] = original[y, x, 1]
#             found = True
#         elif (redRange[0] <= original[y, x, 2] <= redRange[1]):
#             combo[y, x, 2] = original[y, x, 2]
#             found = True

#         if (found == False):
#             combo[y, x] = grayscale[y, x]


