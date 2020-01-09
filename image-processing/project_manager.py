import cv2
from enum import Enum

import dominant_colors
import gaussian_smoothing
import gaze_tracking
import lane_detection
import selective_coloration
import text_extraction
import stabilization

class InputType(Enum):
    IMAGE = 0
    VIDEO = 1
    CAMERA = 2

''' change these to match the program you wish to call '''
inputType = InputType.IMAGE
source = 'images\\abstract.jpg'
cameraSource = 0
PROGRAM = selective_coloration

try:
    PROGRAM.__init__(source)
except TypeError:
    pass

try:
    if (inputType == InputType.IMAGE):
        img = cv2.imread(source)
        PROGRAM.main(img)
    elif (inputType == InputType.VIDEO):
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            raise IOError("Cannot open video source")
        while(True):
            _, img = cap.read()
            PROGRAM.main(img)
            if (cv2.waitKey(1) == 27):
                break
        cap.release()
        cv2.destroyAllWindows()
    elif (inputType == InputType.CAMERA):
        cap = cv2.VideoCapture(cameraSource)
        if not cap.isOpened():
            raise IOError("Cannot open camera")
        while(True):
            _, img = cap.read()
            PROGRAM.main(img)
            if (cv2.waitKey(1) == 27):
                break
        cap.release()
        cv2.destroyAllWindows()
except AttributeError:
    print('input type and source do not match, quitting')