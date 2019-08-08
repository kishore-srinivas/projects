''' 
from the tutorial at: https://www.youtube.com/watch?v=eLTLtUVuuy4

steps:
1. read in image as grayscale
2. gaussian blur to reduce noise
3. canny filter to find basic edges
4. create mask with triangular shape for regionOfInterest
5. bitwise and the mask and image to only show features in regionOfInterest
6. hough transform
7. average out all the lines detected and draw them with height 2/5 of the image height

'''
import cv2
import numpy as np

def makeCoordinates(image, lineParams):
    slope, intercept = lineParams
    y1 = image.shape[0]
    y2 = int(y1*0.6)
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1, y1, x2, y2])

def averageSlopeIntercept(image, lines):
    leftFit = []
    rightFit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            leftFit.append((slope, intercept))
        else:
            rightFit.append((slope, intercept))
    leftFitAvg = np.average(leftFit, axis=0)
    rightFitAvg = np.average(rightFit, axis=0)
    leftLine = makeCoordinates(image, leftFitAvg)
    rightLine = makeCoordinates(image, rightFitAvg)
    return np.array([leftLine, rightLine])

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    gradients = cv2.Canny(blur, 50, 150)
    return gradients

def displayLines(image, lines):
    lineImage = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(lineImage, (x1, y1), (x2, y2), (255, 0, 0), 5)
    return lineImage

def regionOfInterest(image):
    height = image.shape[0]
    polygons = np.array([
        [(200, height), (1100, height), (550, 250)]
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    maskedImage = cv2.bitwise_and(image, mask)
    return maskedImage

''' for images '''
# img = cv2.imread('images\\test_image.jpg')
# laneImage = np.copy(img)
# cannyImage = canny(laneImage)
# cropped = regionOfInterest(cannyImage)
# lines = cv2.HoughLinesP(cropped, 2, np.pi/180, 100, np.array([]), 40, 5)
# averagedLines = averageSlopeIntercept(laneImage, lines)
# linedImage = displayLines(laneImage, averagedLines)
# combo = cv2.addWeighted(laneImage, 0.8, linedImage, 1, 1)
# cv2.namedWindow('result', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('result', 400, 300)
# cv2.imshow('result', combo)
# cv2.waitKey(0)

''' for videos '''
cap = cv2.VideoCapture('images\\test2.mp4')
while (cap.isOpened()):
    _, frame = cap.read()
    cannyImage = canny(frame)
    cropped = regionOfInterest(cannyImage)
    lines = cv2.HoughLinesP(cropped, 2, np.pi/180, 100, np.array([]), 40, 5)
    averagedLines = averageSlopeIntercept(frame, lines)
    linedImage = displayLines(frame, averagedLines)
    combo = cv2.addWeighted(frame, 0.8, linedImage, 1, 1)
    cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('result', 400, 300)
    cv2.imshow('result', combo)
    if (cv2.waitKey(1) == ord('q')):
        break
cap.release()
cv2.destroyAllWindows()