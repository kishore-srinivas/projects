import cv2
import numpy as np

''' figures out the average and dominant colors of an image 
meant to be used to provide a better backlighting experience '''

img = cv2.imread('abstract.jpg')
print(np.shape(img))
pixels = np.float32(img.reshape(-1, 3))

n_colors = 5
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
flags = cv2.KMEANS_RANDOM_CENTERS
_, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
_, counts = np.unique(labels, return_counts=True)
dominant = palette[np.argmax(counts)]

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 300, 250)
cv2.imshow('image', img)

color = np.zeros((300, 250, 3), np.uint8)
color[:] = (dominant[0], dominant[1], dominant[2])
cv2.namedWindow('color', cv2.WINDOW_NORMAL)
cv2.resizeWindow('color', 300, 250)
cv2.imshow('color', color)

lo = np.amin(color, axis=2, keepdims=True)
hi = np.amax(color, axis=2, keepdims=True)
complement = (lo + hi) - color
cv2.namedWindow('complement', cv2.WINDOW_NORMAL)
cv2.resizeWindow('complement', 300, 250)
cv2.imshow('complement', complement)

cv2.waitKey(0)