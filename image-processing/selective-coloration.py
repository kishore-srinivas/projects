import numpy as np
import cv2

original = cv2.imread('images\\abstract.jpg')
grayscale = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

redRange = [0, 255]
blueRange = [0, 255]
greenRange = [0, 255]

def nothing(val):
    pass

# cv2.resizeWindow('result', np.shape(img)[1], np.shape(img)[0])
# cv2.createTrackbar('Blue', 'result', 0, 255, nothing)
# cv2.createTrackbar('Green', 'result', 0, 255, nothing)
# cv2.createTrackbar('Red', 'result', 0, 255, nothing)

# lastBlue = cv2.getTrackbarPos('Blue', 'result')
# lastGreen = cv2.getTrackbarPos('Green', 'result')
# lastRed = cv2.getTrackbarPos('Red', 'result')

combo = np.zeros_like(original)
shape = np.shape(original)
for y in range(shape[0]):
    for x in range(shape[1]):
        found = False
        if (blueRange[0] <= original[y, x, 0] <= blueRange[1]):
            combo[y, x, 0] = original[y, x, 0]
            found = True
        if (greenRange[0] <= original[y, x, 1] <= greenRange[1]):
            combo[y, x, 1] = original[y, x, 1]
            found = True
        if (redRange[0] <= original[y, x, 2] <= redRange[1]):
            combo[y, x, 2] = original[y, x, 2]
            found = True

        if (found == False):
            combo[y, x] = grayscale[y, x]

result = combo
cv2.namedWindow('result', cv2.WINDOW_NORMAL)
cv2.imshow('result', result)

cv2.waitKey(0)
