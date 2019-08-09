import numpy as np
import cv2
import math

''' pseudocode:
read in image in color and grayscale
read in sensitivity values
define color clusters based on sensitivity
    strictest sensitivity is purest color
    least strict sensitivity is the most mixed it can be and still be considered that color
classify pixel as a specific cluster
'''

original = cv2.imread('images\\color-picker.png')
grayscale = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

redRange = [150, 255]
blueRange = [200, 255]
greenRange = [100, 255]

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

combo = np.zeros_like(original)
for y in range(np.shape(original)[0]):
    for x in range(np.shape(original)[1]):
        if (isColor(original[y, x], [255, 100, 0], 150), [.5, 1.5, 0]):
            combo[y, x] = original[y, x]
        else:
            combo[y, x] = grayscale[y, x]

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

result = combo
cv2.namedWindow('result', cv2.WINDOW_NORMAL)
cv2.imshow('result', result)

cv2.waitKey(0)
