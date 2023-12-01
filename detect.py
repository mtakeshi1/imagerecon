import time
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import mediapipe as mp
import numpy as np
import cv2
from mediapipe.tasks.python.components.containers import Category
from typing import List, Dict, Tuple, Union
from compact import CompactImage
import pyvirtualcam

from cameratest import cut, skip, reshape

image_paths: Dict[str, str] = {'Thumb_Up': 'thumbsup.png',
                               'Thumb_Down': 'thumbsdown.png',
                               'Closed_Fist': 'closedfist.png'
                               }

duration_secs = 5


class FakeCategory:
    def __init__(self, cat_name):
        self.category_name = cat_name


def init_recon():
    base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
    options = vision.GestureRecognizerOptions(base_options=base_options)
    # options.running_mode = VisionTaskRunningMode.LIVE_STREAM
    return vision.GestureRecognizer.create_from_options(options)


def refresh_gesture(category: Union[Category, FakeCategory], icons: Dict[str, Tuple[CompactImage, float]],
                    img_cache: Dict[str, np.ndarray],
                    shape):
    if category.category_name in image_paths.keys():
        visible_secs = time.time() + duration_secs
        img = get_image(category, img_cache, shape)
        icons[category.category_name] = (img, visible_secs)


def get_image(category, img_cache, shape):
    img_file = image_paths[category.category_name]
    img = img_cache.get(img_file)
    if img is None:
        img: np.ndarray = cut(cv2.imread(image_paths[category.category_name]))
        img = reshape(img, shape)
        img_cache[img_file] = img
    return CompactImage(img)


def draw_into(target: np.ndarray, icon: np.ndarray):
    x_off = (target.shape[0] - icon.shape[0]) // 2
    y_off = (target.shape[1] - icon.shape[1]) // 2
    for x in range(icon.shape[0]):
        for y in range(icon.shape[1]):
            if not skip(icon[x][y]):
                target[x + x_off][y + y_off] = icon[x][y]


def main():
    recon = init_recon()
    cap = cv2.VideoCapture(0)
    icons: Dict[str, Tuple[CompactImage, float]] = {}
    image_cache = {}
    with pyvirtualcam.Camera(width=640, height=480, fps=20, device='/dev/video2') as cam:
        while True:
            ret, frame = cap.read()
            if not ret:
                time.sleep(1)
                continue
            image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            recognition_result = recon.recognize(image)
            if recognition_result and recognition_result.gestures:
                for gesture in recognition_result.gestures:
                    for category in gesture:
                        print(f'detected gesture: {category}')
                        refresh_gesture(category, icons, image_cache, frame.shape)

            now = time.time()
            for icon in icons.values():
                if icon[1] > now:
                    icon[0].copy_into(frame)
            cam.send(frame)
            # must resize to target shape =(
            # color scheme or something else is also strange
            cam.sleep_until_next_frame()
            # cv2.imshow('capture', frame)
            # key = cv2.waitKey(1)
            # if key == ord('q'):
            #     break
            # elif key == ord('u'):
            #     refresh_gesture(FakeCategory('Thumb_Up'), icons, image_cache, frame.shape)
            # elif key == ord('d'):
            #     refresh_gesture(FakeCategory('Thumb_Down'), icons, image_cache, frame.shape)


if __name__ == '__main__':
    main()
