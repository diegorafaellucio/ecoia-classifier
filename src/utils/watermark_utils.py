import cv2
import cv2 as cv
import numpy as np
import imutils
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum

class WatermarkUtils:


    @staticmethod
    def insert_watermark_in_image(img, watermarker, alpha=1, beta=0.8):
        h_img, w_img, _ = img.shape

        logo = cv.resize(watermarker, (w_img, h_img))
        result = cv.addWeighted(img, alpha, logo, beta, 0)
        return result

    @staticmethod
    def create_watermark_based_on_image_size(image, watermark_path=None):

        if watermark_path is None:

                logo_path = ConfigurationStorageController.get_config_data_value(
                    ConfigurationEnum.MODULE_GENERATE_WATERMARK_LOGO_PATH.name)
        else:
            logo_path = watermark_path

        h_target, w_target, _ = image.shape

        logo = cv2.imread(logo_path)

        h_logo, w_logo, _ = logo.shape

        qt_cols = int(w_target / w_logo)
        qt_rows = int(h_target / h_logo)
        logo_copy = logo.copy()
        logo_copy_2 = logo.copy()
        rows = []
        for row in range(0, qt_rows):
            for col in range(0, qt_cols):
                logo_copy_2 = np.hstack([logo_copy_2, logo_copy])
            # mask = np.vstack([logo_copy_2,logo_copy_2])
            rows.append(logo_copy_2)
            logo_copy_2 = logo_copy
        mask_for_watermarker = np.vstack(rows)
        return mask_for_watermarker

    @staticmethod
    def get_image_with_watermarker(image, watermark_path=None):
        watermarker = WatermarkUtils.create_watermark_based_on_image_size(image, watermark_path)
        image_with_watermark = WatermarkUtils.insert_watermark_in_image(image, watermarker)

        return image_with_watermark