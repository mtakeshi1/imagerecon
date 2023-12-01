import numpy as np


def skip(rgba: np.ndarray):
    if rgba[0] == rgba[1] and rgba[0] == rgba[2]:
        return rgba[0] == 255 or rgba[0] == 0
    if len(rgba) == 4:
        return rgba[3] > 0
    return False


class CompactImage:

    @staticmethod
    def compact_row(row):
        result = list()
        begin = -1
        for i in range(0, len(row)):
            if not skip(row[i]):
                if begin == -1:
                    begin = i
            elif begin >= 0:
                result.append([begin, row[begin:i]])
                begin = -1
        if begin >= 0:
            result.append([begin, row[begin:]])
        return result if len(result) > 0 else None

    @staticmethod
    def compact(img):
        matrix = dict()
        for i, row in enumerate(img):
            cpt = CompactImage.compact_row(row)
            if cpt:
                matrix[i] = cpt
        return matrix

    def __init__(self, img: np.ndarray):
        self.compacted = CompactImage.compact(img)

    def copy_into(self, frame: np.ndarray):
        for row_i, row in self.compacted.items():
            for slice_i, section in row:
                frame[row_i][slice_i:slice_i+len(section)] = section
