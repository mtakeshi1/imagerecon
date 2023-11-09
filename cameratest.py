from typing import Optional

import cv2
import numpy as np

class CameraHelper:
    def __init__(self, capture: Optional[cv2.VideoCapture] = None, window_name: Optional[str] = None):
        if capture is None:
            capture = cv2.VideoCapture(0)
        self.cap = capture
        if window_name is None:
            window_name = 'video_capture'
        self.window_name = window_name

    def next_frame(self):
        ret, frame = self.cap.read()
        if ret:
            return cv2.flip(frame, 1)
        return None

    def show_next_frame(self):
        cv2.imshow(self.window_name, self.next_frame())
        cv2.waitKey(1)

    def reshape(self, img, fit_to_shape):
        ratio = 1.0
        if img.shape[0] > fit_to_shape[0]:
            ratio = fit_to_shape[0] / img.shape[0]

        if img.shape[1] > fit_to_shape[1]:
            ratio = min(fit_to_shape[1] / img.shape[1], ratio)
        # new_shape = [int(img.shape[0] * ratio), int(img.shape[1] * ratio), img.shape[2]]

        return cv2.resize(img, fx=ratio, fy=ratio, interpolation=cv2.INTER_CUBIC)

    def overlay_camera(self, img_path: str):
        img = cv2.imread(img_path)
        frame = self.next_frame()
        frame_shape = frame.shape
        img_shape = img.shape
        if img_shape[0] > frame_shape[0] or img_shape[1] > frame_shape[1]:
            img = self.reshape(img, frame_shape)
        frame[0:img.shape[0], 0:img.shape[1]] = img
        cv2.imshow(self.window_name, frame)
        cv2.waitKey(1)

        pass

    def show_image(self, path):
        if path:
            img = cv2.imread(path)
            cv2.imshow(self.window_name, img)
            cv2.waitKey(1)

    def show_video(self, duration: int = 30):
        import time
        try:
            end = time.time() + duration
            while time.time() < end:
                self.show_next_frame()
                cv2.waitKey(1)
        finally:
            if self.window_name:
                cv2.destroyWindow(self.window_name)

    def release(self):
        if self.cap:
            self.cap.release()
        if self.window_name:
            cv2.destroyWindow(self.window_name)
