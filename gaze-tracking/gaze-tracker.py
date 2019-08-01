import cv2
from GazeTracking.gaze_tracking import GazeTracking

gaze = GazeTracking()
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

while(True):
    ret, frame = cap.read()
    cv2.imshow('Input', frame)

    gaze.refresh(frame)
    new_frame = gaze.annotated_frame()
    cv2.imshow("Demo", new_frame)

    if (cv2.waitKey(1) == 27):
        break

# cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()