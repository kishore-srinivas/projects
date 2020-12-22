import cv2
import matplotlib.pyplot as plt
import numpy as np

def deskew(img):
    m = cv2.moments(img)
    if abs(m['mu02']) < 1e-2:
        # no deskewing needed.
        return img.copy()

    # Calculate skew based on central momemts.
    skew = m['mu11']/m['mu02']
    # Calculate affine transform to correct skewness.
    M = np.float32([[1, skew, -0.5*skew], [0, 1, 0]])
    # Apply affine transform
    rows, cols = img.shape
    img = cv2.warpAffine(img, M, (cols, rows), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR)

    return img

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
            if abs((y + h) - cy) < threshY:
                clustersY[cy].append((x, y + h))
                foundY = True
                break
        if not foundY:
            clustersY[y+h] = [(x, y + h)]

    return clustersX, clustersY

def splitMatrix(matrixImage, visualize=False):
    # recalculate bounding boxes on cropped image
    bb = calculateBoundingBoxes(matrixImage, 21)      

    # identify large bounding boxes
    threshBBSize = np.mean(bb[:,2]*bb[:,3]) - 0.5 * np.std(bb[:,2]*bb[:,3])
    threshBBHeight = np.mean(bb[:,3])
    largeBB = bb[np.logical_or((bb[:,2]*bb[:,3] > threshBBSize), (bb[:,3] > threshBBHeight))]      

    # determine x and y thresholds for optimal clustering of large bounding boxes, extract matrix dimension from this clustering
    clusterResults = {}
    height, width, _ = matrixImage.shape
    # try a range of x and y threshold values
    for i in range(2, 10):
        for j in range(2, 10):
            threshX = width / i
            threshY = height / j
            clustersX, clustersY = clusterBoundingBoxes(largeBB, threshX, threshY)
            dims = (len(clustersY.keys()), len(clustersX.keys()))
            if dims in clusterResults.keys():
                clusterResults[dims].append((threshX, threshY))
            else:
                clusterResults[dims] = [(threshX, threshY)]
    # determine the matrix dimension identified by the most clusters, and use those threshold values for optimal clustering
    maxCount = 0
    optimalThreshold = (threshX, threshY)
    for cr in clusterResults.keys():
        numVals = len(clusterResults[cr])
        if numVals > maxCount:
            maxCount = numVals
            optimalThreshold = clusterResults[cr][-1]
            dims = cr        
    
    # recalculate clusters with optimal threshold values to identify horizontal and vertical splits
    clustersX, clustersY = clusterBoundingBoxes(largeBB, *optimalThreshold)
    xSplits = []
    ySplits = []
    for cx in clustersX.keys():
        vals = clustersX[cx]
        xSplits.append(max(x for x, y in vals))
    for cy in clustersY.keys():
        vals = clustersY[cy]
        ySplits.append(max(y for x, y in vals))

    if visualize:
        for cr in clusterResults.keys():
            print(cr, len(clusterResults[cr]))
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>', dims)

        for x, y, w, h in bb:
            cv2.rectangle(matrixImage, (x, y), (x + w, y + h), (0, 255, 0), 2)
            plt.plot(x, y, 'bo')

        for x, y, w, h in largeBB:
            cv2.rectangle(matrixImage, (x, y), (x + w, y + h), (0, 0, 255), 2)
            plt.plot(x, y, 'r+')

        print('clustersX')
        for cx in clustersX.keys():
            print(cx)
            cv2.line(matrixImage, (cx, 0), (cx, matrixImage.shape[0]), (255, 0, 0), 1)
            for v in clustersX[cx]:
                print(' ', v)
        print()
        print('clustersY')
        for cy in clustersY.keys():
            print(cy)
            cv2.line(matrixImage, (0, cy), (matrixImage.shape[1], cy), (255, 0, 0), 1)
            for v in clustersY[cy]:
                print(' ', v)

        print()
        print(len(list(clustersY.keys())), 'x', len(list(clustersX.keys())), 'matrix')
        cv2.imshow('dimension calculation', matrixImage)

    return xSplits, ySplits

def __main__(imgPath):
    # load, grayscale, and blur image
    orig = cv2.imread(imgPath)
    orig = cv2.resize(orig, (int(orig.shape[1]/2), int(orig.shape[0]/2)))
    im = orig.copy()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    deskewed = deskew(gray)
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
    xSplits, ySplits = splitMatrix(cropped.copy(), visualize=True)
    print(len(ySplits), 'x', len(xSplits))
    for x in xSplits:
        cv2.line(cropped, (int(x), 0), (int(x), cropped.shape[0]), (0, 128, 0), 2)
    for y in ySplits:
        cv2.line(cropped, (0, int(y)), (cropped.shape[1], int(y)), (0, 128, 0), 2)
    cv2.imshow('split', cropped)

    plt.show()
    cv2.waitKey()

__main__('matrices\\matrix8.jpg')