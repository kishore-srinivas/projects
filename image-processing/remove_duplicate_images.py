### based on this PyImageSearch tutorial: 
### https://www.pyimagesearch.com/2020/04/20/detect-and-remove-duplicate-images-from-a-dataset-for-deep-learning/

from imutils import paths
import numpy as np
import cv2
import os
import json

REMOVE_DUPLICATES = False # set to True to remove duplicate files from the directory

# hash function to represent an image as a number
def hash(image, size=50):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (size, size+1))
    
    # computes vertical gradient at each pixel
    diff = np.zeros((size, size))
    for i in range(size):
        row = resized[i]
        nextRow = resized[i+1]
        diff[i] = nextRow - row
    return sum(diff.flatten())

allImagePaths = list(paths.list_images('images'))
hashTable = {}
for path in allImagePaths:
    img = cv2.imread(path)
    key = hash(img)
    entry = hashTable.get(key, [])
    entry.append(path)
    hashTable[key] = entry

duplicates = []
keys = hashTable.keys()
for k in keys:
    arr = hashTable[k]
    if (len(arr) < 2): # if fewer than 2 images mapped to this location there will be no duplicate
        continue

    # check if the possible duplicates have the same height
    lengths = {}
    sameHeight = []
    for path in arr:
        img = cv2.imread(path)
        l = len(img)
        try:
            val = lengths[l]
            if (val not in sameHeight):
                sameHeight.append(val)
            sameHeight.append(path)
        except:
            lengths[l] = path

    # check if the possible duplicates have the same width
    widths = {}
    sameWidth = []
    for path in sameHeight:
        img = cv2.imread(path)
        w = len(img[0])
        try:
            val = widths[w]
            if (val not in sameWidth):
                sameWidth.append(val)
            sameWidth.append(path)
        except:
            widths[w] = path

    # check if specific pixel values match
    if (len(sameWidth) > 0):
        img1 = cv2.imread(sameWidth[0])
        h = len(img1)
        w = len(img1[0])
        points =  [[0, int(w/2)], [int(h/2), 0], [h-1, int(w/2)], [int(h/2), int(w/2)]]
        pixelValues = {}
        for i in range(len(points)):
            pixelValues[i] = []

        # extract the values for pixels of interest
        for path in sameWidth:
            img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_RGB2GRAY)
            for i in range(len(points)):                
                val = img[points[i][0], points[i][1]]
                arr = pixelValues[i]
                arr.append(val)
                pixelValues[i] = arr

        # check if corresponding pixels match in the possibly duplicate images
        for k in pixelValues.keys():
            values = {}
            arr = pixelValues[k]
            for i in range(len(arr)):
                v = arr[i]
                try:
                    values[v] = values[v] + 1
                    if (sameWidth[i] not in duplicates): duplicates.append(sameWidth[i])
                except:
                    values[v] = 1
                    pass
            
print("Duplicates:", duplicates)

if (REMOVE_DUPLICATES):
    for d in duplicates:
        os.remove(d)
