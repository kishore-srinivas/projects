''' uses data set from https://www.kaggle.com/clarencezhao/handwritten-math-symbol-dataset, extracted to ./archive '''

import cv2
import numpy as np
import os
import random
import sys

np.random.seed(1212)
import keras
from keras.models import Model
from keras.layers import *
from keras import optimizers
from keras.layers import Input, Dense
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
K.set_image_data_format('channels_last')
from keras.utils.np_utils import to_categorical
from keras.models import model_from_json
import time
from matplotlib import pyplot as plt

### prep x and y test and train data ###
toConsider = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'minus', 'minus val']
nameToVal = {'zero':0, 'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9, 'minus':10, 'minus val':10}
IM_SHAPE = (135, 150, 1)

print('training data...')
# load data from training folder
TRAIN_PATH = 'archive\\train'
trainData = {}
filesToPaths = {}
for d in os.listdir(TRAIN_PATH):
    if d not in toConsider:
        continue
    local = TRAIN_PATH + '\\' + d
    files = [f for f in os.listdir(local) if os.path.isfile(os.path.join(local, f))]
    val = nameToVal[d]
    for f in files:
        trainData[local + '\\' + f] = val
        filesToPaths[f] = local + '\\' + f

# populate x and y train sets
xTrain = []
yTrain = []
keys = (list(filesToPaths.keys()))
# random.shuffle(keys)
for k in keys:
    k2 = filesToPaths[k]
    im = cv2.imread(k2, 0)
    xTrain.append(cv2.resize(im, IM_SHAPE[:2]).reshape(IM_SHAPE))
    labels = np.zeros(11)
    labels[trainData[k2]] = 1
    yTrain.append(labels)

print('testing data...')
# load data from eval folder
EVAL_PATH = 'archive\\eval'
testData = {}
filesToPaths = {}
for d in os.listdir(EVAL_PATH):
    if d not in toConsider:
        continue
    local = EVAL_PATH + '\\' + d
    files = [f for f in os.listdir(local) if os.path.isfile(os.path.join(local, f))]
    val = nameToVal[d]
    for f in files:
        testData[local + '\\' + f] = val
        filesToPaths[f] = local + '\\' + f

# populate x and y test sets
xTest = []
yTest = []
keys = (list(filesToPaths.keys()))
# random.shuffle(keys)
for k in keys:
    k2 = filesToPaths[k]
    im = cv2.imread(k2, 0)
    xTest.append(cv2.resize(im, IM_SHAPE[:2]).reshape(IM_SHAPE))
    labels = np.zeros(11)
    labels[testData[k2]] = 1
    yTest.append(labels)

print(xTrain[0].shape, yTrain[0], type(xTrain[0]), type(yTrain[0]))
print(xTest[0].shape, yTest[0], type(xTest[0]), type(yTest[0]))
xTrain = np.array(xTrain)
yTrain = np.array(yTrain)
print(xTrain.shape, yTrain.shape)

### we have xTrain, yTrain, xTest, yTest lists, so now we create, train, and save the model ###
# create the model
np.random.seed(7)
model = Sequential()
model.add(Conv2D(30, (5, 5), input_shape=(xTrain[0].shape), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(15, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(50, activation='relu'))
model.add(Dense(11, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit training data to model
print('model prepped, training...')
start = time.time()
model.fit(x=np.array(xTrain), y=np.array(yTrain), epochs=10, batch_size=200, shuffle=True, verbose=1)
print('time: {:.3f} seconds'.format(time.time() - start))

# save model and weights to files
print('model trained, writing...')
model_json = model.to_json()
with open("model2.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("model2.h5")