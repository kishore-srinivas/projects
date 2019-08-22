import cv2
import numpy as np
cv2DataPath = 'C:\\Program Files\\Python\\Python37-32\\Lib\\site-packages\\cv2\\data\\'
import time

# original = cv2.imread('images\\timberlake.jpg')
# grayscale = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

face_cascade = cv2.CascadeClassifier(cv2DataPath + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2DataPath + 'haarcascade_eye.xml')
last_keypoint = (0, 0)

def detect_face(img):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    coords = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
    if len(coords) > 1:
        biggest = (0, 0, 0, 0)
        for i in coords:
            if i[3] > biggest[3]:
                biggest = i
        biggest = np.array([i], np.int32)
    elif len(coords) == 1:
        biggest = coords
    else:
        return None
    for (x, y, w, h) in biggest:
        return np.array([x, y, w, h])

def detect_eyes(img):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray_frame, 1.05, 5) # detect eyes
    width = np.size(img, 1) # get face frame width
    height = np.size(img, 0) # get face frame height
    left_eye = None
    right_eye = None
    for (x, y, w, h) in eyes:
        if y > height / 2:
            pass
        eyecenter = x + w / 2  # get the eye center
        if eyecenter < width * 0.5:
            right_eye = np.array([x, y, w, h])
        else:
            left_eye = np.array([x, y, w, h])
    return left_eye, right_eye

def detect_iris(img):
    adjusted = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # adjusted = cv2.GaussianBlur(adjusted, (5, 5), 1)
    height, width = np.shape(adjusted)
    adjusted[0:int(.3*height), 0:width] = 255

    is_v2 = cv2.__version__.startswith("2.")
    if is_v2:
        detector = cv2.SimpleBlobDetector()
    else:
        detector = cv2.SimpleBlobDetector_create()    # Detect blobs.
    keypoints = detector.detect(adjusted)  
    adjusted = cv2.cvtColor(adjusted, cv2.COLOR_GRAY2BGR)
    
    if (len(keypoints) > 0):
        center = keypoints[0].pt
        center = (int(center[0]), int(center[1]))
        print(np.shape(adjusted), ':', center, keypoints[0].size)
        cv2.circle(adjusted, center, 3, (0,255,0), 1)
        cv2.namedWindow('adjusted', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('adjusted', 100, 100)
        cv2.imshow('adjusted', adjusted)        
        return center
    else:
        return (0, 0)

def main(original):
    original = cv2.flip(original, 1)
    result = np.copy(original)

    try:
        x, y, w, h = detect_face(original)
    except TypeError:
        x = 0
        y = 0
        w = np.size(original, 1)
        h = np.size(original, 0)
    face = original[y:y+h, x:x+w]
    cv2.rectangle(result, (x, y), (x+w, y+h), (255, 255, 0), 2)

    try:
        [lx, ly, lw, lh], [rx, ry, rw, rh] = detect_eyes(face)
    except TypeError:
        lx = ly = rx = ry = 0
        lw = rw = int(w/2)
        lh = rh = int(h/2)
    leftEye = face[ly:ly+lh, lx:lx+lw]
    rightEye = face[ry:ry+rh, rx:rx+rw]
    cv2.rectangle(result, (x + lx, y + ly), (x + lx+lw, y + ly+lh), (0, 255, 255), 2)
    cv2.rectangle(result, (x + rx, y + ry), (x + rx+rw, y + ry+rh), (0, 255, 255), 2)

    cv2.circle(result, tuple(map(lambda x, y, z: x + y + z, (x, y), (lx, ly), detect_iris(leftEye))), 1, (0, 0, 255), 3)
    # cv2.circle(result, tuple(map(lambda x, y, z: x + y + z, (x, y), (rx, ry), detect_iris(rightEye))), 1, (0, 0, 255), 3)

    cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('result', int(np.shape(original)[1]/2), int(np.shape(original)[0]/2))
    cv2.imshow('result', result)