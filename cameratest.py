import time
from typing import Optional

import cv2
import numpy as np


def reshape(img, fit_to_shape):
    ratio = min(0.9, fit_to_shape[1] / img.shape[1], fit_to_shape[0] / img.shape[0])
    return cv2.resize(img, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_CUBIC)


def skip(rgba: np.ndarray):
    if rgba[0] == rgba[1] and rgba[0] == rgba[2]:
        return rgba[0] == 255 or rgba[0] == 0
    if len(rgba) == 4:
        return rgba[3] > 0
    return False


def cut(img):
    x_removes = []
    for x in range(img.shape[0]):
        found = False
        for y in range(img.shape[1]):
            if not skip(img[x][y]):
                found = True
                break
        if not found:
            x_removes.append(x)
    y_removes = []
    for y in range(img.shape[1]):
        found = False
        for x in range(img.shape[0]):
            if not skip(img[x][y]):
                found = True
                break
        if not found:
            y_removes.append(y)
    # if x_removes:
    #     img = np.delete(img, x_removes, 0)
    if y_removes:
        img = np.delete(img, y_removes, 1)
    return img


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

    def overlay_camera(self, img_path: str):
        img = cut(cv2.imread(img_path))
        frame = self.next_frame()
        frame_shape = frame.shape
        img = reshape(img, frame_shape)
        from detect import  draw_into
        draw_into(frame, img)
        cv2.imshow(self.window_name, frame)
        cv2.waitKey(1)

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


if __name__ == '__main__':
    cam = CameraHelper()
    cam.overlay_camera('thumbsdown.png')
    time.sleep(10)

