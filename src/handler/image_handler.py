import logging
import concurrent.futures
import os.path
import cv2
from datetime import datetime

from src.controller.image_controller import ImageController
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum
from src.enum.classification_error_enum import ClassificationErrorEnum
from src.enum.image_state_enum import ImageStateEnum
from src.enum.meat_enum import MeatEnum
from src.utils.image_utils import ImageUtils
from src.utils.detector_utils import DetectorUtils
from src.handler.skeleton_classifier_handler import SkeletonClassifierHandler
from src.handler.filter_classifier_handler import FilterClassifierHandler
from src.handler.meat_classifier_handler import MeatClassifierHandler



class ImageHandler():

    @staticmethod
    def process_image(image_id, image_path, sequence_number, side_number, roulette_number, slaughter_date, created_at,
                      processing_timestamp, flag_img, state, aux_grading_id, classifier_suite):

        ImageController.update_image_status(ImageStateEnum.PROCESSING.value, image_id)

        classification_id = None

        skeleton_detector, filter_detector, side_detector, meat_detector, bruise_detector, side_a_shape_predictor, side_b_shape_predictor = classifier_suite

        images_main_path = ConfigurationStorageController.get_config_data_value(ConfigurationEnum.IMAGES_MAIN_PATH.name)

        image_absolute_path = os.path.join(images_main_path, image_path)
        masked_image_absolute_path = image_absolute_path.replace('.', '-masked.')


        ImageHandler.logger.info(
            'Checking if there are image to sequence: {} and side: {}'.format(sequence_number, side_number))

        has_image = ImageUtils.has_image(image_absolute_path, flag_img, state)

        if has_image:
            ImageHandler.logger.info(
                'Localized image to sequence: {} and side: {}'.format(sequence_number, side_number))

            image = cv2.imread(image_absolute_path)

            ImageHandler.logger.info(
                f'Checking if a skeleton is present to sequence: {sequence_number} and side: {side_number}')

            skeleton_detection_result = SkeletonClassifierHandler.classify(skeleton_detector, image)

            if skeleton_detection_result is None:
                classification_id = ClassificationErrorEnum.ERRO_92.value

            else:
                filter_detection_result = FilterClassifierHandler.classify(filter_detector, image)

                if filter_detection_result is None:
                    classification_id = ClassificationErrorEnum.ERRO_95.value
                else:

                    ImageController.update_filter_classification_data(filter_detection_result['label'], filter_detection_result['confidence'], image_id)

                    filter_in_black_List = FilterClassifierHandler.predicted_result_is_in_black_list(filter_detection_result)

                    if filter_in_black_List:
                        classification_id = ClassificationErrorEnum.ERRO_97.value
                    else:

                        meat_detection_result = MeatClassifierHandler(meat_detector, image)

                        meat_detection_label = meat_detection_result['label']

                        meat_detataset_id = MeatEnum[meat_detection_label].value['database_id']

                        classification_id = meat_detataset_id

                        # # TODO: inserir erro classificacao no sistema e alterar status para aguardando aguardando classificacao de lesao
                        #
                        # side_detection_results = side_detector.detect(image)
                        # best_side_result = DetectorUtils.get_best_detection(side_detection_results, image_height,
                        #                                                     image_width)
                        #
                        # bruise_detection_results = bruise_detector.detect(image)










        #     TODO: Continuar fluxo

        else:
            ImageHandler.logger.error(
                'File not found to sequence: {} and side: {}'.format(sequence_number, side_number))
            classification_id = ClassificationErrorEnum.ERRO_91.value

        return classification_id, image_id
