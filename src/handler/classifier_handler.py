import logging
import concurrent.futures

from src.controller.image_controller import ImageController
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum
from src.utils.image_utils import ImageUtils
from src.utils.classifier_utils import ClassifierUtils
from src.utils.bruise_utils import BruiseUtils
from src.utils.cuts_utils import CutsUtils
from src.enum.image_state_enum import ImageStateEnum
from src.enum.system_version_enum import SystemVersionEnum
from src.enum.classification_error_enum import ClassificationErrorEnum
import cv2



class ClassifierHandler:
    logger = logging.getLogger(__name__)

    @staticmethod
    def process_images(classifier_suite):

        max_workers = ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.MAX_WORKERS.name)

        execution_pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)

        data = ImageController.get_images_to_classify(max_workers)

        have_data_to_classify = ImageUtils.have_data_to_classify(data)

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
                    execution_pool.submit(ClassifierHandler.process_image, image_id, image_path, sequence_number,
                                          side_number, roulette_number, slaughter_date, created_at,
                                          processing_timestamp, flag_img, state, aux_grading_id, classifier_suite))

            for x in concurrent.futures.as_completed(futures):
                image_id = x.result()
        else:

            ClassifierHandler.logger('Was not images to process...')

    @staticmethod
    def process_image(image_id, image_path, sequence_number, side_number, roulette_number, slaughter_date, created_at,
                      processing_timestamp, flag_img, state, aux_grading_id, classifier_suite):

        classification_id = None
        system_version = ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.SYSTEM_VERSION.name)

        ImageController.update_image_status(ImageStateEnum.PROCESSING.value, image_id)

        skeleton_detector, filter_detector, side_detector, meat_detector, bruise_detector, stamp_detector, side_a_shape_predictor, side_b_shape_predictor = classifier_suite

        images_main_path = ConfigurationStorageController.get_config_data_value(ConfigurationEnum.IMAGES_MAIN_PATH.name)

        image_absolute_path = images_main_path + image_path
        masked_image_absolute_path = image_absolute_path.replace('.', '-masked.')

        # ImageHandler.logger.info(
        #     'Checking if there are image to sequence: {} and side: {}'.format(sequence_number, side_number))

        has_image = ImageUtils.has_image(image_absolute_path, flag_img, state)

        if has_image:
            # ImageHandler.logger.info(
            #     'Localized image to sequence: {} and side: {}'.format(sequence_number, side_number))

            image = cv2.imread(image_absolute_path)

            classification_id = ClassifierUtils.get_classification_id(image_id, image, sequence_number, side_number,
                                                                        skeleton_detector, filter_detector,
                                                                        meat_detector)

            if system_version == SystemVersionEnum.PROFESSIONAL.value and classification_id not in (
                    ClassificationErrorEnum.ERRO_92.value, ClassificationErrorEnum.ERRO_95.value,
                    ClassificationErrorEnum.ERRO_96.value, ClassificationErrorEnum.ERRO_97.value):
                side_detection_result = ClassifierUtils.classify(side_detector, image)
                bruise_detection_results = bruise_detector.detect(image)
                stamp_detection_results = stamp_detector.detect(image)

                sanitized_bruises = BruiseUtils.sanitize_bruises(bruise_detection_results, stamp_detection_results)

                cuts_coords = CutsUtils.get_cuts(image, side_detection_result, side_a_shape_predictor,
                                                 side_b_shape_predictor)

                cut_lines_image, cuts_mask = CutsUtils.get_cuts_mask_and_cut_lines_image(cuts_coords, image)


                CutsUtils.save_cuts_data(image_id, cuts_coords)

                cut_lines_image = BruiseUtils.draw_bruises_on_cut_lines_image(cut_lines_image, side_detection_result, sanitized_bruises)

                cv2.imwrite(masked_image_absolute_path, cut_lines_image)

                BruiseUtils.save_bruises_data(cuts_mask, side_detection_result, sanitized_bruises, image_id)






        # # TODO: inserir erro classificacao no sistema e alterar status para aguardando aguardando classificacao de lesao
        #
        # side_detection_results = side_detector.detect(image)
        # best_side_result = DetectorUtils.get_best_detection(side_detection_results, image_height,
        #                                                     image_width)
        #
        # bruise_detection_results = bruise_detector.detect(image)
        else:
            classification_id = ClassificationErrorEnum.ERRO_91.value

        ImageController.update_image_classification(classification_id, image_id)
        ImageController.update_image_status(ImageStateEnum.PROCESSED.value, image_id)

        return image_id
