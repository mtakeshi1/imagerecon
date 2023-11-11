import time
from enum import StrEnum
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import mediapipe as mp
import numpy as np
import cv2
from mediapipe.tasks.python.components.containers import Category
from typing import List, Dict, Tuple

from cameratest import cut, skip, reshape

image_paths: Dict[str, str] = {'Thumb_Up': 'thumbsup.png',
                               'Thumb_Down': 'thumbsdown.png'
                               }


# class Category(StrEnum):
#     thumbs_up = 'Thumb_Up'
#     thumbs_down = 'Thumb_Down'
#     open_palm = 'Open_Palm'
#     i_love_you = 'ILoveYou'


def init_recon():
    base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
    options = vision.GestureRecognizerOptions(base_options=base_options)
    return vision.GestureRecognizer.create_from_options(options)


def refresh_gesture(category: Category, icons: Dict[str, Tuple[np.ndarray, float]], img_cache: Dict[str, np.ndarray],
                    shape):
    if category.category_name in image_paths.keys():
        visible_secs = time.time() + 5
        img_file = image_paths[category.category_name]
        img = img_cache.get(img_file)
        if img is None:
            img: np.ndarray = cut(cv2.imread(image_paths[category.category_name]))
            img = reshape(img, shape)
            img_cache[img_file] = img
        icons[category.category_name] = (img, visible_secs)


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
    icons: Dict[str, Tuple[np.ndarray, float]] = {}
    image_cache = {}
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
                    refresh_gesture(category, icons, image_cache, frame.shape)

        now = time.time()
        for icon in icons.values():
            if icon[1] > now:
                draw_into(image, icon[0])
            pass
