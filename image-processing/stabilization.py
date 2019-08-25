import cv2
import numpy as np
from scipy.ndimage import shift

referenceImage = None
minY = 275
maxY = 385
minX = 100
maxX = 210
def __init__(source):
    global referenceImage, minY, maxY, minX, maxX
    print("init")
    vidcap = cv2.VideoCapture(source)
    success, frame = vidcap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    referenceImage = frame[minY:maxY, minX:maxX]
    if success:
        cv2.imshow("first_frame", referenceImage)  

def main(img):
    # cv2.imshow('pre', img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray,referenceImage,cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # cv2.circle(img, max_loc, 3, (0, 0, 255))
    cv2.rectangle(img, max_loc, tuple(map(lambda x, y: x + y, max_loc, np.shape(referenceImage))), (0,0,255))
    (dx, dy) = tuple(map(lambda x, y: x - y, max_loc, (minX, minY)))
    print(max_loc, (dx, dy))
    img = np.roll(img, -1 * dx, axis=1)
    img = np.roll(img, -1 * dy, axis=0)
    for i in range(0, dy, -1 if dy < 0 else 1):
        img[-1*i,:]=(0, 0, 0)
    for i in range(0, dx, -1 if dx < 0 else 1):
        img[:,-1*i]=(0, 0, 0)
    cv2.imshow('result', img)