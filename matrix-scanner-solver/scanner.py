import cv2
import matplotlib.pyplot as plt
import numpy as np

def calculateBoundingBoxes(img, blur=9):
    # grayscale and blur
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (blur, blur), 0)

    # tresholding for cleaner edges and bolder strokes
    _, thresh = cv2.threshold(blurred, 255, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # find contours and bounding boxes
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    boundingBoxes = np.array([cv2.boundingRect(c) for c in contours])

    return boundingBoxes

def clusterBoundingBoxes(boxes, threshX, threshY):
    clustersX = {}
    clustersY = {}    
    for x, y, w, h in boxes:
        foundX = False
        foundY = False
        for cx in clustersX.keys():
            if abs((x + w) - cx) < threshX:
                clustersX[cx].append((x + w, y))
                foundX = True
                break
        if not foundX:
            clustersX[x+w] = [(x + w, y)]
        for cy in clustersY.keys():
            if abs(y - cy) < threshY:
                clustersY[cy].append((x, y))
                foundY = True
                break
        if not foundY:
            clustersY[y] = [(x, y)]

    return clustersX, clustersY

def identifyMatrixDimension(matrixImage, visualize=False):
    # recalculate bounding boxes on cropped image
    bb = calculateBoundingBoxes(matrixImage, 21)      

    # identify large bounding boxes
    avgBBSize = np.mean(bb[:,2]*bb[:,3])
    largeBB = bb[bb[:,2]*bb[:,3] > avgBBSize]      

    # cluster large bounding boxes along x and y axes
    threshX = matrixImage.shape[1] / 10
    threshY = matrixImage.shape[0] / 10
    clustersX, clustersY = clusterBoundingBoxes(largeBB, threshX, threshY)

    if visualize:
        for x, y, w, h in bb:
            cv2.rectangle(matrixImage, (x, y), (x + w, y + h), (0, 255, 0), 2)
            plt.plot(x, y, 'bo')

        for x, y, w, h in largeBB:
            cv2.rectangle(matrixImage, (x, y), (x + w, y + h), (0, 0, 255), 2)
            plt.plot(x, y, 'r+')

        print('clustersX')
        for cx in clustersX.keys():
            print(cx)
            cv2.line(matrixImage, (cx, 0), (cx, matrixImage.shape[0]), (255, 0, 0), 2)
            # for v in clustersX[cx]:
            #     print(' ', v)
        print()
        print('clustersY')
        for cy in clustersY.keys():
            print(cy)
            cv2.line(matrixImage, (0, cy), (matrixImage.shape[1], cy), (255, 0, 0), 2)
            # for v in clustersY[cy]:
            #     print(' ', v)

        print()
        print(len(list(clustersY.keys())), 'x', len(list(clustersX.keys())), 'matrix')

    return (len(list(clustersY.keys())), len(list(clustersX.keys())))

def __main__():
    # load, grayscale, and blur image
    orig = cv2.imread('matrices\\matrix4.jpg')
    orig = cv2.resize(orig, (int(orig.shape[1]/2), int(orig.shape[0]/2)))
    im = orig.copy()
    boundingBoxes = calculateBoundingBoxes(im)

    # find tallest 2 bounding boxes - likely to be left and right brackets
    sortedBB = boundingBoxes[boundingBoxes[:,3].argsort()]
    tallBoxes = sortedBB[-2:]

    # plot bounding boxes
    for x, y, w, h in boundingBoxes:
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
    for x, y, w, h in tallBoxes:
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 2)
    # cv2.imshow('image', im)

    # crop image to contain just the matrix
    xMin = min(x + w for x, y, w, h in tallBoxes)
    yMin = np.amin(tallBoxes[:, 1])
    xMax = np.amax(tallBoxes[:, 0])
    yMax = max(y + h for x, y, w, h in tallBoxes)
    cropped = orig[yMin:yMax, xMin:xMax]

    # identify matrix dimensions and split image accordingly
    matrixDims = identifyMatrixDimension(cropped, visualize=True)
    print('>>>', matrixDims)
    xSplits = np.linspace(0, cropped.shape[1], matrixDims[1]+1)[1:-1]
    ySplits = np.linspace(0, cropped.shape[0], matrixDims[0]+1)[1:-1]
    # for x in xSplits:
    #     cv2.line(cropped, (int(x), 0), (int(x), cropped.shape[0]), (255, 255, 0), 1)
    # for y in ySplits:
    #     cv2.line(cropped, (0, int(y)), (cropped.shape[1], int(y)), (255, 255, 0), 1)
    cv2.imshow('cropped', cropped)

    plt.show()
    cv2.waitKey()

__main__()