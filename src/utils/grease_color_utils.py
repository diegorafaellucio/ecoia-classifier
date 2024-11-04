import cv2
from src.enum.grease_color_enum import GreaseColorEnum
import numpy as np
class GreaseColorUtils:

    @staticmethod
    def remove_background(image, binary_mask):
        image_without_background = cv2.bitwise_and(image, image, mask=binary_mask)
        return image_without_background



    @staticmethod
    def predict(detector, image, binary_mask):

        image_without_background = GreaseColorUtils.remove_background(image, binary_mask)

        image_features = GreaseColorUtils.get_histogram(image_without_background)

        detection_results = detector.predict(image_features)
        grease_color_model_id = str(detection_results[0])
        grease_color_database_id = GreaseColorEnum.get_value(grease_color_model_id)

        return grease_color_database_id

    @staticmethod
    def get_histogram(img, hsv=True):

        if hsv:
            img_analysy = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        else:
            img_analysy = img.copy()

        channels = cv2.split(img_analysy)
        features = []
        for c in channels:
            hist = cv2.calcHist([c], [0], None, [256], [0, 256])
            features.append(hist[1:])

        features = np.hstack(features)
        features = features.T
        features = features.flatten()
        return features.reshape((1, -1))

