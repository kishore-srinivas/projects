import cv2
import numpy as np
from scipy.ndimage import shift
import sys

roi = None
minY = 80
maxY = 155
minX = 440
maxX = 515
startCorner = None
stopCorner = None
frame = None
copy = None

def crop(event, x, y, flags, param):
    global startCorner, stopCorner, roi, copy
    if (startCorner != None):
        frame = np.copy(copy)
        cv2.rectangle(frame, startCorner, (x,y), (0,255,0), 2)
        cv2.imshow('frame', frame)
    if (event == cv2.EVENT_LBUTTONDOWN):
        startCorner = (x, y)
    elif (event == cv2.EVENT_LBUTTONUP):
        stopCorner = (x, y)

def __init__(source):
    global roi, minY, maxY, minX, maxX, startCorner, stopCorner, frame, copy
    vidcap = cv2.VideoCapture(source)
    success, frame = vidcap.read()
    copy = np.copy(frame)
    cv2.imshow('frame', frame)
    cv2.setMouseCallback('frame', crop)
    if cv2.waitKey(0) == ord("c"):
        if (startCorner != None) and (stopCorner != None):
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            roi = frame[startCorner[1]:stopCorner[1], startCorner[0]:stopCorner[0]]
            cv2.imshow("ROI", roi)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

def main(img):
    cv2.imshow('img', img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray, roi, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    corner = min_loc
    (dx, dy) = tuple(map(lambda x, y: x - y, corner, (minX, minY)))
    img = np.roll(img, -1 * dx, axis=1)
    img = np.roll(img, -1 * dy, axis=0)
    for i in range(0, dy, -1 if dy < 0 else 1):
        img[-1*i,:]=(0, 0, 0)
    for i in range(0, dx, -1 if dx < 0 else 1):
        img[:,-1*i]=(0, 0, 0)
    cv2.imshow('result', img)