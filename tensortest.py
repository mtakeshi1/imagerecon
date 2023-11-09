from typing import Optional

import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time

# initialize mediapipe
mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils

# Load the gesture recognizer model
# Load class names
with  open('gestures.txt', 'r') as f:
    classNames = f.read().split('\n')

# Initialize the webcam for Hand Gesture Recognition Python project
cap = cv2.VideoCapture(0)

base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)


# _, frame = cap.read()
# frame = cv2.flip(frame, 1)
# recognition_result = recognizer.recognize(frame)
# print(recognition_result.gestures)
# x, y, c = frame.shape
# cap.release()
# cv2.destroyAllWindows()

image = None

while True:
    # Read each frame from the webcam
    _, frame = cap.read()
    x, y, c = frame.shape

    # Flip the frame vertically
    frame = cv2.flip(frame, 1)
    if frame is not None:
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        recognition_result = recognizer.recognize(image)
        print(recognition_result.gestures)
        # Show the final output
        cv2.imshow("Output", frame)
    if cv2.waitKey(1) == ord('q'):
        break



# release the webcam and destroy all active windows
cap.release()
cv2.destroyAllWindows()

