import numpy as np
import cv2
from mss import mss
from PIL import Image

bounding_box = {'top': 160, 'left': 235, 'width':550, 'height': 550}

sct = mss()
frames = []
recording = False

while True:
    sct_img = sct.grab(bounding_box)
    cv2.imshow('screen', np.array(sct_img))
    if (not recording and cv2.waitKey(1) & 0xFF) == ord('c'):
        print('recording')
        recording = True
    if recording:
        frames.append(np.array(sct_img))

    if (cv2.waitKey(1) & 0xFF) == 27:
        print('stopped')
        cv2.destroyAllWindows()
        recording = False
        break

print(len(frames))
print(frames[0].shape)
result = cv2.VideoWriter('balls.mp4',  
                         cv2.VideoWriter_fourcc('H', '2', '6', '4'), 
                         60, (frames[0].shape[0], frames[0].shape[1]))
for i in range(len(frames)):
    result.write(frames[i])
    cv2.imshow('captured', frames[i])

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break