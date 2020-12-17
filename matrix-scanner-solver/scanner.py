import cv2
import matplotlib.pyplot as plt
import numpy as np

# load, grayscale, and blur image
im = cv2.imread('matrices\\matrix2.jpg')
im = cv2.resize(im, (int(im.shape[1]/2), int(im.shape[0]/2)))
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (9, 9), 0)

# apply thresholding on blurred image for cleaner edges and bolder strokes
_, thresh = cv2.threshold(blurred, 255, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
# cv2.imshow('thresh', thresh)

# find contours and bounding boxes
contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]
boundingBoxes = np.array([cv2.boundingRect(c) for c in contours])
avgBoundingBoxSize = np.mean(boundingBoxes, axis=0)[2:]
print(avgBoundingBoxSize)

# # find tall and extra tall bounding boxes - likely to be left and right brackets
# tallBoxes = boundingBoxes[boundingBoxes[:,3] > avgBoundingBoxSize[1]]
# print(tallBoxes.shape)
# while (tallBoxes.shape[0] > 2):
#     avgTallBBSize = np.mean(tallBoxes, axis=0)[2:]
#     extraTallBoxes = tallBoxes[tallBoxes[:,3] > avgTallBBSize[1]]
#     print('>>>', avgTallBBSize, extraTallBoxes.shape)
#     tallBoxes = extraTallBoxes
# print(tallBoxes.shape)

# find tallest 2 bounding boxes - likely to be left and right brackets
sortedBB = boundingBoxes[boundingBoxes[:,3].argsort()]
print(boundingBoxes.shape, sortedBB.shape)
tallBoxes = sortedBB[-2:]

for x, y, w, h in boundingBoxes:
    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
for x, y, w, h in tallBoxes:
    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 2)

xMin = np.amin(tallBoxes[:, 0])
yMin = np.amin(tallBoxes[:, 1])
xMax = max(x + w for x, y, w, h in tallBoxes)
yMax = max(y + h for x, y, w, h in tallBoxes)

cropped = im[yMin:yMax, xMin:xMax]
cv2.imshow('cropped', cropped)

cv2.imshow('image', im)
cv2.waitKey()
