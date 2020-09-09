import numpy as np
import cv2
import math
import sys

canvas = np.ones((600, 600, 3))
clearCanvas = np.copy(canvas)
origin = None
reflections = 1
alpha = 2 * math.pi / reflections
drawing = False

def getReflectedPos(x, y, current):
    global origin, reflections, alpha
    theta = current * alpha
    deltaX = x - origin[0]
    deltaY = y - origin[1]
    newX = int(origin[0] + math.cos(theta) * (x - origin[0]) - math.sin(theta) * (y - origin[1]))
    newY = int(origin[1] + math.sin(theta) * (x - origin[0]) + math.cos(theta) * (y - origin[1]))
    return (newY, newX)

def draw(event, x, y, flags, param):
    global canvas, drawing, origin
    if (event == cv2.EVENT_LBUTTONDOWN):
        if (origin == None):
            origin = (x, y)
            cv2.circle(canvas, origin, 5, (0, 0, 255))
        else:
            drawing = True
    elif (event == cv2.EVENT_LBUTTONUP):
        drawing = False
    if (drawing):
        for i in range(0, reflections):
            canvas[getReflectedPos(x, y, i)] = 0
    cv2.imshow('result', canvas)

cv2.imshow('result', canvas)
cv2.setMouseCallback('result', draw)
while True:
    key = cv2.waitKey(0)
    if key == ord("r"):
        reflections *= 2
        alpha = 2 * math.pi / reflections
        print('>>>', reflections)
    elif key == ord("R"):
        reflections = int(reflections / 2)
        reflections = reflections if reflections > 1 else 1
        alpha = 2 * math.pi / reflections
        print('>>>', reflections)
    elif key == ord("c"):
        print('clearing...')
        canvas = np.copy(clearCanvas)
        reflections = 1
        origin = None
        cv2.imshow('result', canvas)
    elif key == 27:
        cv2.destroyAllWindows()
        sys.exit()