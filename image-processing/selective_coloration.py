import numpy as np
import cv2
from tkinter import *
import math

''' pseudocode:
read in image in color and grayscale
read in sensitivity values
define color clusters based on sensitivity
    strictest sensitivity is purest color
    least strict sensitivity is the most mixed it can be and still be considered that color
classify pixel as a specific cluster
'''

# original = cv2.imread('images\\lion.jpg')
# grayscale = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
# loading = cv2.imread('images\\loading.jpg')

'''
calculates the euclidean distance between a pixel and a color with a specific weight
@param pixel - the pixel to compare
@param color - the BGR color to compare to
@param weight - the weight to give to each color channel (a higher weight makes it harder to be classified as that color)
'''
def euclideanDistance(pixel, color, weight):
    for i in range(len(weight)):
        if (weight[i] < 0):
            weight[i] = 0
    deltaBlue = (pixel[0] - color[0]) * weight[0]
    deltaGreen = (pixel[1] - color[1]) * weight[1]
    deltaRed = (pixel[2] - color[2]) * weight[2]
    return math.sqrt(deltaBlue ** 2 + deltaGreen ** 2 + deltaRed ** 2)

def isColor(pixel, color, tolerance, weights=[1, 1, 1]):
    distance = euclideanDistance(pixel, color, weights)
    return distance <= tolerance

def update(original, color, weights, tolerance): 
    print(color, weights, tolerance)
    if (tolerance <= 0):
        return
    grayscale = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    solid = np.zeros((10, 10, 3), np.uint8)   
    solid[:] = (color[0], color[1], color[2])
    # print(solid)
    print(np.shape(solid))
    cv2.namedWindow('color', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('color', 10, 10)
    cv2.imshow('color', solid)   
    print('COLOR DISPLAYED')
    # cv2.waitKey(0)
    combo = np.zeros_like(original)
    rangeY = np.shape(original)[0]
    rangeX = np.shape(original)[1]
    print('RANGE:', rangeX, rangeY)
    for y in range(rangeY):
        for x in range(rangeX):
            if (isColor(original[y, x], color, tolerance, weights)):
                combo[y, x] = original[y, x]
            else:
                combo[y, x] = grayscale[y, x]

    result = combo
    cv2.imshow('result', result)
    print("DONE")
    # cv2.waitKey(0)

# def buttonClick(c1, c2, c3, w1, w2, w3, t):
#     update([c1.get(), c2.get(), c3.get()], [w1.get(), w2.get(), w3.get()], t.get())

def main(img):
    cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    cv2.imshow('result', img)

    master = Tk()
    c1 = Scale(master, label='Blue', from_=0, to=255, resolution=1, orient=HORIZONTAL)
    c1.pack()
    c2 = Scale(master, label='Green', from_=0, to=255, resolution=1, orient=HORIZONTAL)
    c2.pack()
    c3 = Scale(master, label='Red', from_=0, to=255, resolution=1, orient=HORIZONTAL)
    c3.pack()
    w1 = Scale(master, label='Blue weight', from_=0, to=15, resolution=0.25, orient=HORIZONTAL)
    w1.pack()
    w2 = Scale(master, label='Green weight', from_=0, to=15, resolution=0.25, orient=HORIZONTAL)
    w2.pack()
    w3 = Scale(master, label='Red weight', from_=0, to=15, resolution=0.25, orient=HORIZONTAL)
    w3.pack()
    t = Scale(master, label='Tolerance', from_=0, to=255, resolution=1, orient=HORIZONTAL)
    t.pack()
    Button(master, text='Update', command=update(img, [c1.get(), c2.get(), c3.get()], [w1.get(), w2.get(), w3.get()], t.get())).pack()

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


