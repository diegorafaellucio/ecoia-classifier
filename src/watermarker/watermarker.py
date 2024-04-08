import cv2 as cv
import numpy as np
import imutils

class Watermarker:
    def __init__(self, path_for_logo):
        self.logo = cv.imread(path_for_logo)

    def insert_water_marker(self, img, watermarker, alpha=1, beta=0.8):
        h_img, w_img, _ = img.shape

        logo = cv.resize(watermarker, (w_img, h_img))
        result = cv.addWeighted(img, alpha, logo, beta, 0)
        return result

    def create_mask(self, target):
        h_target, w_target, _ = target.shape
        h_logo, w_logo, _ = self.logo.shape

        qt_cols = int(w_target / w_logo)
        qt_rows = int(h_target / h_logo)
        logo_copy = self.logo.copy()
        logo_copy_2 = self.logo.copy()
        rows = []
        for row in range(0, qt_rows):
            for col in range(0, qt_cols):
                logo_copy_2 = np.hstack([logo_copy_2, logo_copy])
            # mask = np.vstack([logo_copy_2,logo_copy_2])
            rows.append(logo_copy_2)
            logo_copy_2 = logo_copy
        mask_for_watermarker = np.vstack(rows)
        return mask_for_watermarker

    def get_image_with_watermarker(self, image):
        watermarker = self.create_mask(image)
        return imutils.resize(self.insert_water_marker(image, watermarker), height=500)