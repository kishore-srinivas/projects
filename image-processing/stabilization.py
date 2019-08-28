import cv2
import numpy as np
from scipy.ndimage import shift
import sys

roi = None
minY = 80
maxY = 155
minX = 440
maxX = 515
def __init__(source):
    # TODO add cropping to set roi
    global roi, minY, maxY, minX, maxX
    print("init")
    vidcap = cv2.VideoCapture(source)
    success, frame = vidcap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    roi = frame[minY:maxY, minX:maxX]
    cv2.rectangle(frame, (minX,minY), (maxX,maxY), (0,0,255))
    if success:
        # cv2.imshow('frame', frame)
        cv2.imshow('roi', roi)  
        # cv2.waitKey(0)

def main(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray, roi, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    corner = min_loc
    # cv2.rectangle(img, corner, (corner[0] + np.shape(roi)[1], corner[1] + np.shape(roi)[0]), (0, 0, 255))
    (dx, dy) = tuple(map(lambda x, y: x - y, corner, (minX, minY)))
    # print(corner, (dx, dy))
    # if (cv2.waitKey(0) == 27):
    #     sys.exit()
    img = np.roll(img, -1 * dx, axis=1)
    img = np.roll(img, -1 * dy, axis=0)
    for i in range(0, dy, -1 if dy < 0 else 1):
        img[-1*i,:]=(0, 0, 0)
    for i in range(0, dx, -1 if dx < 0 else 1):
        img[:,-1*i]=(0, 0, 0)
    cv2.imshow('result', img)