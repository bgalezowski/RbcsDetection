import cv2 as cv
import numpy as np

from source.constants import num_contour_points
from source.Logger import Logger


class ImageProcessor:
    def __init__(self, path):
        self.logger = Logger()

        image = cv.imread(path)
        if image is None:
            self.logger.error('File has invalid format or does not exist')
            exit(1)
        else:
            self.image = image
        self.logger.info(path + ' successfully loaded')

        self.height, self.width, _ = self.image.shape
        self.pre_processing()
        self.get_contours()

    def pre_processing(self):
        self.gray_image = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        self.blur_image = cv.GaussianBlur(self.gray_image, (5, 5), 0)
        ret3, th3 = cv.threshold(self.blur_image, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
        self.binary_image = th3

    def check_parent(self, obj, height, width):
        x_min = np.min(np.min(obj, axis=0), axis=0)[0]
        y_min = np.min(np.min(obj, axis=1), axis=0)[1]
        x_max = np.max(np.max(obj, axis=0), axis=0)[0]
        y_max = np.max(np.max(obj, axis=1), axis=0)[1]
        if x_min == 0 or y_min == 0 or x_max == width - 1 or y_max == height - 1 or len(obj) <= num_contour_points:
            return False
        return True

    def check_child(self, obj):
        if len(obj) <= num_contour_points:
            return False
        return True

    def get_contours(self):
        self.contours, hierarchy = cv.findContours(self.binary_image, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        self.hierarchy = hierarchy[0]

    def show_image(self):
        image = cv.resize(self.image, (600, 600))
        cv.imshow("Result", image)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def search_tree(self, detector):
        self.logger.info('Detection started...')
        for i in range(0, len(self.hierarchy)):
            parent = ''
            child = ''
            if self.hierarchy[i][3] == -1:
                if self.check_parent(self.contours[i], self.height, self.width):
                    parent = self.contours[i]
                    if self.hierarchy[i][2] != -1:
                        if self.check_child(self.contours[self.hierarchy[i][2]]):
                            child = self.contours[self.hierarchy[i][2]]
            if len(parent) != 0:
                detector.detect(parent, child)
