import cv2
import numpy as np

img = cv2.imread('images\\painting.jpg', 0)

print(img[100, 100])
print(img.item(100, 100))

print(img.shape)
print(img.dtype)

region = img[200:300, 400:500]
img[0:100, 0:100] = region
 
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 300, 250)
cv2.imshow('image', img)

kernel1 = np.ones((5,5), np.float32)/25
blur1 = cv2.filter2D(img, -1, kernel1)
cv2.namedWindow('blur1', cv2.WINDOW_NORMAL)
cv2.resizeWindow('blur1', 300, 250)
cv2.imshow('blur1', blur1)

gauss1 = cv2.GaussianBlur(img, (111,111), 0)
cv2.namedWindow('gauss1', cv2.WINDOW_NORMAL)
cv2.resizeWindow('gauss1', 300, 250)
cv2.imshow('gauss1', gauss1)

gauss2 = cv2.GaussianBlur(img, (71,71), 0)
# cv2.namedWindow('gauss2', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('gauss2', 300, 250)
# cv2.imshow('gauss2', gauss2)

gauss3 = cv2.GaussianBlur(img, (31,31), 0)
# cv2.namedWindow('gauss2', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('gauss2', 300, 250)
# cv2.imshow('gauss2', gauss3)

kernel2 = np.array([[0, -0.25, 0],
                    [-0.25, 2, -0.25],
                    [0, -0.25, 0]])
blur2 = cv2.filter2D(img, -1, kernel2)
# cv2.namedWindow('blur2', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('blur2', 300, 250)
# cv2.imshow('blur2', blur2)

diff = gauss1 - gauss2
cv2.namedWindow('diff', cv2.WINDOW_NORMAL)
cv2.resizeWindow('diff', 300, 250)
cv2.imshow('diff', diff)

diff2 = gauss1 + diff
# cv2.namedWindow('diff2', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('diff2', 300, 250)
# cv2.imshow('diff2', diff2)

cv2.waitKey(0)
cv2.destroyAllWindows()