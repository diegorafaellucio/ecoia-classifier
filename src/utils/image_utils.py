import traceback

import cv2
import imutils
import logging
import numpy as np
from wand.color import Color
from wand.image import Image

import os
import re

from src.controller.image_controller import ImageController
from src.enum.image_name_generate_approach_enum import ImageNameGenerateApproachEnum
from src.enum.configuration_enum import ConfigurationEnum
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.utils.email_utils import EmailUtils
from src.enum.notification_email_enum import NotificationEmailEnum
from src.enum.country_enum import CountryEnum
from src.enum.classification_error_enum import ClassificationErrorEnum

class ImageUtils:

    logger = logging.getLogger(__name__)
    regex = r'^(\d{4})(\d{2})(\d{2})-(\d{4})-(\d)-(\d{4})-(\d{4})\.jpg$'

    black_color_lab = np.array([0, 128, 128], dtype=np.uint8)
    white_color_lab = np.array([205, 128, 128], dtype=np.uint8)

    @staticmethod
    def is_carcass(model, img):
        results = model.detect(img)
        for results in results:
            conf_score = results['confidence']
            if conf_score >= 0.8:
                return True
            else:
                return False

    @staticmethod
    def adjust_color(img):
        img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
        black_luminance = img_lab[..., 0].min()
        white_luminance = img_lab[..., 0].max()

        targetBlackLuminance = ImageUtils.black_color_lab[0]
        targetWhiteLuminance = ImageUtils.white_color_lab[0]

        img_lab[..., 0] = np.interp(img_lab[..., 0], (black_luminance, white_luminance),
                                   (targetBlackLuminance, targetWhiteLuminance))

        imgAdjusted = cv2.cvtColor(img_lab, cv2.COLOR_Lab2BGR)

        return imgAdjusted
    @staticmethod
    def get_ajusted_image(image):

        rotation_angle = int(ConfigurationStorageController.get_config_data_value(ConfigurationEnum.CAPTURE_ROTATION_ANGLE.name))

        top_crop = int(ConfigurationStorageController.get_config_data_value(ConfigurationEnum.CAPTURE_TOP_CROP.name))
        left_crop = int(ConfigurationStorageController.get_config_data_value(ConfigurationEnum.CAPTURE_LEFT_CROP.name))
        bottom_crop = int(ConfigurationStorageController.get_config_data_value(ConfigurationEnum.CAPTURE_BOTTOM_CROP.name))
        right_crop = int(ConfigurationStorageController.get_config_data_value(ConfigurationEnum.CAPTURE_RIGHT_CROP.name))

        output_width = int(ConfigurationStorageController.get_config_data_value(ConfigurationEnum.CAPTURE_OUTPUT_WIDTH.name))
        output_height = int(ConfigurationStorageController.get_config_data_value(ConfigurationEnum.CAPTURE_OUTPUT_HEIGHT.name))

        crop_image = int(ConfigurationStorageController.get_config_data_value(ConfigurationEnum.CAPTURE_CROP_IMAGE.name))
        resize_image = int(ConfigurationStorageController.get_config_data_value(ConfigurationEnum.CAPTURE_RESIZE_IMAGE.name))

        rotated_image = imutils.rotate_bound(image, rotation_angle)
        output_image = rotated_image


        if crop_image == 1:
            rotated_height, rotated_width = rotated_image.shape[:2]
            cropped_image = output_image[top_crop:rotated_height-bottom_crop,
                            left_crop:rotated_width - right_crop]
            output_image = cropped_image
        if resize_image == 1:
            new_dimension = (output_width, output_height)
            resized_image = cv2.resize(output_image, new_dimension,
                                       interpolation=cv2.INTER_AREA)
            output_image = resized_image

        # output_image = cv2.addWeighted(output_image, 1.2, output_image, 0, 0)
        # output_image = ImageUtils.adjust_color(output_image)

        return output_image

    @staticmethod
    def get_image_name(image_name_generation_approach, decoded_data, seq_list_old, classification_id):
        image_name = None

        if classification_id == ClassificationErrorEnum.ERRO_93.value:
            image_name = ImageController.get_new_image_data_when_has_error()

        else:
            if image_name_generation_approach == ImageNameGenerateApproachEnum.AUTOMATIC.value.upper():
                try:
                    country = str(
                        ConfigurationStorageController.get_config_data_value(ConfigurationEnum.COUNTRY.name))
                    if country == CountryEnum.BRAZIL.value:
                        image_name = ImageController.get_new_image_data_br()
                    if country == CountryEnum.PARAGUAY.value:
                        image_name = ImageController.get_new_image_data_py()

                except Exception as e:
                    ImageUtils.logger.error("Exception with Database connection: {}".format(e))
                    ImageController.update_image_if_has_error(image_name)
                    image_name = None

            elif image_name_generation_approach == ImageNameGenerateApproachEnum.SEQ_AND_SIDE.value.upper():
                try:
                    if len(decoded_data) >= 13:  # Verifica se a string tem pelo menos 13 caracteres
                        seq = decoded_data[0:4]
                        side_temp = decoded_data[12]
                        print("Banda: ", side_temp)
                        if side_temp == 'A':
                            side = 1
                        else:
                            side = 2
                        seq_side_list = [seq, side]
                        if seq_side_list != seq_list_old:
                            image_name = ImageController.get_new_image_data_by_seq_and_side(seq, side)
                            seq_list_old = seq_side_list
                        else:
                            print("Slaughter stopped, no record made in the database.", seq_list_old)
                    else:
                        raise ValueError("decoded_data não possui comprimento suficiente")
                except Exception as e:
                    ImageUtils.logger.error("Exception with Database connection: {}".format(e))
                    ImageController.update_image_if_has_error(image_name)
                    image_name = None
        return image_name, seq_list_old

    @staticmethod
    def get_amount_of_zeros_in_image(image):
        height, width, channels = image.shape

        amount_of_pixels = height * width * channels

        no_zeros = image[np.where(image == 0)].size

        percent_amount_of_zeros = no_zeros / amount_of_pixels

        return percent_amount_of_zeros

    @staticmethod
    def image_correction(frame):
        img = Image.from_array(frame)
        img.resize(1440, 2560)
        img.background_color = Color('black')
        img.virtual_pixel = 'background'
        args = (
            0.01,  # A
            0.0,  # B
            0.0,  # C
            1.0,  # D
        )
        img.distort('barrel_inverse', args)
        np_image = np.asarray(img)
        return np_image

    @staticmethod
    def save_image(image_name, capture_device, plc_unavailable=False):
        buffer_images_path = ConfigurationStorageController.get_config_data_value(ConfigurationEnum.TEMP_DATASET_PATH.name)
        image_path = os.path.join(buffer_images_path, image_name)

        if plc_unavailable:
            error_image = np.zeros((1920, 1080, 3), dtype=np.uint8)
            cv2.imwrite(image_path, error_image)
            return True

        else:


            if not os.path.exists(buffer_images_path):
                os.makedirs(buffer_images_path)

            try:
                can_save_image = False
                image = capture_device.get_image()

                if image is not None:
                    can_save_image = True

                if can_save_image:
                    ajusted_image = ImageUtils.get_ajusted_image(image)
                    image_quality = ConfigurationStorageController.get_config_data_value(ConfigurationEnum.CAPTURE_IMAGE_QUALITY.name)
                    ImageUtils.logger.info("Image saving path: {}".format(image_path))
                    cv2.imwrite(image_path, ajusted_image,[cv2.IMWRITE_JPEG_QUALITY, int(image_quality)])
                    return True

                else:
                    error_image = np.zeros((1920, 1080, 3), dtype=np.uint8)
                    cv2.imwrite(image_path, error_image)

                    ImageUtils.logger.error("Exception during image acquisition step: {}".format('Captured Image is None!'))

                    email_body = 'Captured Image is None!'
                    email_title = NotificationEmailEnum.IS_NOT_POSSIBLE_TO_GET_IMAGE_FROM_CAMERA.value
                    email_type = NotificationEmailEnum.IS_NOT_POSSIBLE_TO_GET_IMAGE_FROM_CAMERA.name

                    EmailUtils.send_email(email_body, email_title, email_type)

                    return True
            except:
                ImageUtils.logger.error("Exception during image acquisition step: {}".format(traceback.format_exc()))

                return False



