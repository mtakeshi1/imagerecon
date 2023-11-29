import unittest

import cv2

from detect import CompactImage

red = [255, 0, 0, 0]
black = [255, 255, 255, 0]
white = [0, 0, 0, 0]
transparent = [0, 0, 0, 255]


class MyTestCase(unittest.TestCase):

    def test_start_zeroes(self):
        r = CompactImage.compact_row([white, white, white, red, red])
        self.assertEqual([[3, [red, red]]], r)

    def test_all_zeroes(self):
        r = CompactImage.compact_row([white, white, white, transparent])
        self.assertEqual(None, r)

    def test_real_img(self):
        t = cv2.imread('thumbsup.png')


if __name__ == '__main__':
    unittest.main()
