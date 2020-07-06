import cv2
import numpy as np

''' figures out the average and dominant colors of an image 
meant to be used to provide a better backlighting experience '''

def main(img):
    print(np.shape(img))
    pixels = np.float32(img.reshape(-1, 3))

    n_colors = 5
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)
    dominant = palette[np.argmax(counts)]
    print('dominant:', dominant)

    imgShape = np.shape(img)
    scaleFactor = 1.25
    scaled = np.multiply(imgShape, (scaleFactor, scaleFactor, 1)).astype(int)
    color = np.zeros((scaled[0], scaled[1], scaled[2]), np.uint8)
    color[:] = (dominant[0], dominant[1], dominant[2])
    # lo = np.amin(color, axis=2, keepdims=True)
    # hi = np.amax(color, axis=2, keepdims=True)
    # color = (lo + hi) - color #sets color to its complement
    minY = int((scaled[1]-imgShape[1])/2)
    maxY = int(scaled[1] - (scaled[1]-imgShape[1])/2)
    minX = int((scaled[0]-imgShape[0])/2)
    maxX = int(scaled[0] - (scaled[0]-imgShape[0])/2)
    for x in range(minX, maxX):
        for y in range(minY, maxY):
            color[x, y] = img[x-minX, y-minY]

    cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('result', int(np.shape(color)[1]), int(np.shape(color)[0]))
    cv2.imshow('result', color)

    cv2.waitKey(0)

# img = cv2.imread('C://Users//kisho//Documents//git//projects//image-processing//images//painting.jpg')
# main(img)