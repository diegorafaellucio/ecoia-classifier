import os
import logging

from src.enum.image_state_enum import ImageStateEnum

class ImageUtils:
    logger = logging.getLogger(__name__)
    @staticmethod
    def have_data_to_classify(data):
        if data is None or len(data) == 0:
            return False
        else:
            return True


    @staticmethod
    def has_image(image_absolute_path, flag_img, state):
        has_image = False

        if os.path.exists(image_absolute_path) and int(flag_img) == 1 and (int(state) == (ImageStateEnum.WAITING_PROCESSING.value)):
            has_image = True
        elif not os.path.exists(image_absolute_path):
            has_image = False

        return has_image
