import logging
import concurrent.futures

import imutils

from src.controller.image_controller import ImageController
from src.controller.carcass_information_controller import CarcassInformationController
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.conformation_enum import ConformationEnum
from src.enum.configuration_enum import ConfigurationEnum
from src.utils.file_utils import FileUtils
from src.utils.classifier_utils import ClassifierUtils
from src.utils.skeleton_size_utils import SkeletonSizeUtils
from src.utils.bruise_utils import BruiseUtils
from src.utils.cuts_utils import CutsUtils
from src.utils.watermark_utils import WatermarkUtils
from src.utils.grease_color_utils import GreaseColorUtils
from src.enum.image_state_enum import ImageStateEnum
from src.enum.system_version_enum import SystemVersionEnum
from src.enum.classification_error_enum import ClassificationErrorEnum
import cv2



class MeatClassifierHandler:
    logger = logging.getLogger(__name__)


    @staticmethod
    def process_images(classifier_suite):

        max_workers = ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.MEAT_CLASSIFIER_MAX_WORKERS.name)

        execution_pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)

        data = ImageController.get_images_to_classify(max_workers)

        have_data_to_classify = FileUtils.have_files_to_process(data)

        futures = []

        if have_data_to_classify:
            for item in data:
                image_id = item[0]
                image_path = item[1]
                sequence_number = item[2]
                side_number = item[3]
                roulette_number = item[4]
                slaughter_date = item[5]
                created_at = item[6]
                processing_timestamp = item[7]
                flag_img = item[8]
                state = item[9]
                aux_grading_id = item[10]

                futures.append(
                    execution_pool.submit(MeatClassifierHandler.process_image, image_id, image_path, sequence_number,
                                          side_number, roulette_number, slaughter_date, created_at,
                                          processing_timestamp, flag_img, state, aux_grading_id, classifier_suite))

            for x in concurrent.futures.as_completed(futures):
                image_id = x.result()
        else:

            MeatClassifierHandler.logger.info('Was not data to process!')
            # print('Was not images to process...')

    @staticmethod
    def process_image(image_id, image_path, sequence_number, side_number, roulette_number, slaughter_date, created_at,
                      processing_timestamp, flag_img, state, aux_grading_id, classifier_suite):


        MeatClassifierHandler.logger.info('Starting image processing. Image ID: {}.'.format(image_id))
        classification_id = None
        system_version = ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.SYSTEM_VERSION.name)

        MeatClassifierHandler.logger.info('Updating the image state to: {}. Image ID: {}'.format(ImageStateEnum.PROCESSING.name, image_id))
        ImageController.update_image_status(ImageStateEnum.PROCESSING.value, image_id)

        skeleton_detector, filter_detector, side_detector, meat_detector, bruise_detector, stamp_detector, side_a_shape_predictor, side_b_shape_predictor, grease_color_detector, conformation_detector = classifier_suite

        images_main_path = ConfigurationStorageController.get_config_data_value(ConfigurationEnum.IMAGES_MAIN_PATH.name)

        image_absolute_path = images_main_path + image_path
        masked_image_absolute_path = image_absolute_path.replace('.', '-masked.')

        # ImageHandler.logger.info(
        #     'Checking if there are image to sequence: {} and side: {}'.format(sequence_number, side_number))

        MeatClassifierHandler.logger.info('Checking if file exists. Image ID: {}'.format(image_id))
        has_image = FileUtils.has_file(image_absolute_path, flag_img, state)

        if has_image:
            # ImageHandler.logger.info(
            #     'Localized image to sequence: {} and side: {}'.format(sequence_number, side_number))

            image = cv2.imread(image_absolute_path)
            cut_lines_image = image.copy()

            MeatClassifierHandler.logger.info('Classifying carcass. Image ID: {}'.format(image_id))
            classification_id = ClassifierUtils.get_classification_id(image_id, image,
                                                                        skeleton_detector, filter_detector,
                                                                        meat_detector)




            if system_version == SystemVersionEnum.PROFESSIONAL.value and classification_id not in (
                    ClassificationErrorEnum.ERRO_92.value, ClassificationErrorEnum.ERRO_95.value,
                    ClassificationErrorEnum.ERRO_96.value, ClassificationErrorEnum.ERRO_97.value):
                side_detection_result = ClassifierUtils.classify(side_detector, image)

                MeatClassifierHandler.logger.info('Detecting bruises. Image ID: {}'.format(image_id))
                bruise_detection_results = bruise_detector.detect(image)
                MeatClassifierHandler.logger.info('Detecting stamps. Image ID: {}'.format(image_id))
                stamp_detection_results = stamp_detector.detect(image)

                MeatClassifierHandler.logger.info('Sanitizing bruises. Image ID: {}'.format(image_id))
                sanitized_bruises = BruiseUtils.sanitize_bruises(bruise_detection_results, stamp_detection_results)

                MeatClassifierHandler.logger.info('Obtaining cuts maps. Image ID: {}'.format(image_id))
                cuts_coords = CutsUtils.get_cuts(image, side_detection_result, side_a_shape_predictor,
                                                 side_b_shape_predictor)

                MeatClassifierHandler.logger.info('Mapping bruises in cuts. Image ID: {}'.format(image_id))
                cut_lines_image, cuts_mask,binary_mask = CutsUtils.get_cuts_mask_and_cut_lines_image(cuts_coords, image)

                cut_lines_image = BruiseUtils.draw_bruises_on_cut_lines_image(cut_lines_image, side_detection_result,
                                                                              sanitized_bruises, cuts_mask)
                MeatClassifierHandler.logger.info('Saving cuts. Image ID: {}'.format(image_id))
                CutsUtils.save_cuts_data(image_id, cuts_coords)

                MeatClassifierHandler.logger.info('Saving bruises. Image ID: {}'.format(image_id))
                BruiseUtils.save_bruises_data(cuts_mask, side_detection_result, sanitized_bruises, image_id)

                carcass_information_already_exists = CarcassInformationController.carcass_information_already_exists(
                    image_id)

                if not carcass_information_already_exists:
                    CarcassInformationController.initialize_carcass_information(image_id)

                grease_color_classification_is_enabled = ConfigurationStorageController.get_config_data_value(
                    ConfigurationEnum.MODULE_GREASE_PREDICTION.name)

                if grease_color_classification_is_enabled:

                    grease_color_id = GreaseColorUtils.classify(grease_color_detector, image, binary_mask)

                    CarcassInformationController.update_grease_color(image_id, grease_color_id)

                conformation_classification_is_enabled = ConfigurationStorageController.get_config_data_value(
                    ConfigurationEnum.MODULE_CONFORMATION_PREDICTION.name)


                if conformation_classification_is_enabled:
                    conformation_result = ClassifierUtils.classify(conformation_detector, image)

                    if conformation_result is not None:
                        conformation_id = ConformationEnum[conformation_result['label']].value
                        CarcassInformationController.update_conformation(image_id, conformation_id)

                size_prediction_is_enabled = ConfigurationStorageController.get_config_data_value(
                    ConfigurationEnum.MODULE_SIZE_PREDICTION.name)

                width, height, size_descriptor = SkeletonSizeUtils.get_size(binary_mask, cuts_coords)

                if size_prediction_is_enabled:

                    CarcassInformationController.update_width(image_id, width)
                    CarcassInformationController.update_height(image_id, height)
                    CarcassInformationController.update_size_descriptor(image_id, size_descriptor)


            generate_watermark = ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.GENERATE_WATERMARK.name)

            if generate_watermark == 1:

                cut_lines_image = WatermarkUtils.get_image_with_watermarker(cut_lines_image)
                image = WatermarkUtils.get_image_with_watermarker(image)

                cut_lines_image = imutils.resize(cut_lines_image, height=1920)
                image = imutils.resize(image, height=1920)

                cv2.imwrite(masked_image_absolute_path, cut_lines_image)
                FileUtils.copy_file(image_absolute_path)
                cv2.imwrite(image_absolute_path, image)

            else:

                cv2.imwrite(masked_image_absolute_path, cut_lines_image)

        else:
            classification_id = ClassificationErrorEnum.ERRO_91.value

        MeatClassifierHandler.logger.info(
            'Updating the image classification to: {}. Image ID: {}'.format(classification_id, image_id))
        ImageController.update_image_classification(classification_id, image_id)
        MeatClassifierHandler.logger.info(
            'Updating the image state to: {}. Image ID: {}'.format(ImageStateEnum.WAITING_INTEGRATION.name, image_id))
        ImageController.update_image_status(ImageStateEnum.WAITING_INTEGRATION.value, image_id)

        return image_id
