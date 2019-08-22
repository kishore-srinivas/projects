import cv2
import numpy as np

def main(img):
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    high_thresh, thresh_im = cv2.threshold(cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    lowThresh = 0.5*high_thresh
    gradients = cv2.Canny(blur, lowThresh, high_thresh)
    colorGradients = cv2.cvtColor(gradients, cv2.COLOR_GRAY2BGR)
    allWhites = np.argwhere(colorGradients == 255)
    for i in allWhites:
        colorGradients[i[0], i[1]] = [0,0,255]
    lines = cv2.HoughLinesP(gradients, 2, np.pi/180, 0, np.array([]), 1, 0)
    print(len(lines))
    lineImage = np.zeros_like(img)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(lineImage, (x1, y1), (x2, y2), (255, 0, 0), 1)
    result = lineImage

    cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('result', np.shape(img)[1], np.shape(img)[0])
    cv2.imshow('result', result)

    cv2.waitKey(0)