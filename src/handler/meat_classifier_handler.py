import logging
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import traceback

import imutils

from src.controller.image_controller import ImageController
from src.controller.carcass_information_controller import CarcassInformationController
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.controller.cuts_grading_controller import CutsGradingController
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
from src.enum.hump_enum import HumpEnum
from src.enum.cuts_enum import CutsEnum
from src.utils.hump_utils import HumpUtils
from src.utils.breed_utils import BreedUtils
import cv2



class MeatClassifierHandler:
    logger = logging.getLogger(__name__)


    @staticmethod
    def process_images(classifier_suite):

        max_workers = ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.MEAT_CLASSIFIER_MAX_WORKERS.name)

        futures = []

        executor = ThreadPoolExecutor(max_workers=max_workers)

        if max_workers > 0:

            data = ImageController.get_images_to_classify(max_workers)

            have_data_to_classify = FileUtils.have_files_to_process(data)



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


                    # MeatClassifierHandler.process_image(image_id, image_path, sequence_number,
                    #                                     side_number, roulette_number, slaughter_date, created_at,
                    #                                     processing_timestamp, flag_img, state, aux_grading_id,
                    #                                     classifier_suite)

                    futures.append(
                        executor.submit(MeatClassifierHandler.process_image, image_id, image_path, sequence_number,
                                                        side_number, roulette_number, slaughter_date, created_at,
                                                        processing_timestamp, flag_img, state, aux_grading_id,
                                                        classifier_suite))

                for _ in concurrent.futures.as_completed(futures):
                    MeatClassifierHandler.logger.info('Register Processed successfully!')


            else:

                MeatClassifierHandler.logger.info('Was not data to process!')

    @staticmethod
    def process_image(image_id, image_path, sequence_number, side_number, roulette_number, slaughter_date, created_at,
                      processing_timestamp, flag_img, state, aux_grading_id, classifier_suite):

        reprocess_retroactive_days = ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.REPROCESS_RETROACTIVE_DAYS.name)

        filter_label = 'NAO_CLASSIFICADO'
        filter_confidence = 0.0
        classification_id = None

        try:

            if aux_grading_id is None:

                MeatClassifierHandler.logger.info('Starting image processing. Image ID: {}.'.format(image_id))

                classification_id = None

                MeatClassifierHandler.logger.info(
                    'Updating the image state to: {}. Image ID: {}'.format(ImageStateEnum.PROCESSING.name, image_id))
                ImageController.update_status(ImageStateEnum.PROCESSING.value, image_id)

                carcass_classification_classifier, skeleton_detector, filter_detector, side_detector, meat_detector, bruise_detector, stamp_detector, side_a_shape_predictor, side_b_shape_predictor, grease_color_detector, conformation_detector, hump_detector, breed_detector, cuts_classification_models = classifier_suite

                images_main_path = ConfigurationStorageController.get_config_data_value(
                    ConfigurationEnum.IMAGES_MAIN_PATH.name)

                image_absolute_path = images_main_path + image_path
                masked_image_absolute_path = image_absolute_path.replace('.', '-masked.')

                MeatClassifierHandler.logger.info(
                    'Checking if there are image to sequence: {} and side: {}'.format(sequence_number, side_number))

                MeatClassifierHandler.logger.info(
                    'Localized image to sequence: {} and side: {}'.format(sequence_number, side_number))

                # image = cv2.imread(image_absolute_path)

                MeatClassifierHandler.logger.info('Classifying carcass. Image ID: {}'.format(image_id))

                image, classification_id, classification_confidence, filter_label, filter_confidence, side_detection_result = ClassifierUtils.get_classification_id(
                    image_absolute_path,
                    side_detector,
                    meat_detector, skeleton_detector, filter_detector, reprocess_retroactive_days, carcass_classification_classifier
                    )


                if classification_id not in (ClassificationErrorEnum.ERRO_91.value, ClassificationErrorEnum.ERRO_92.value,
                        ClassificationErrorEnum.ERRO_93.value, ClassificationErrorEnum.ERRO_94.value, ClassificationErrorEnum.ERRO_95.value, ClassificationErrorEnum.ERRO_96.value, ClassificationErrorEnum.ERRO_97.value, ClassificationErrorEnum.ERRO_100.value,
                        ClassificationErrorEnum.ERRO_101.value, ClassificationErrorEnum.ERRO_102.value)  and image is not None:

                    MeatClassifierHandler.logger.info('Detecting bruises. Image ID: {}'.format(image_id))
                    bruise_detection_results = bruise_detector.predict(image)

                    MeatClassifierHandler.logger.info('Detecting stamps. Image ID: {}'.format(image_id))
                    stamp_detection_results = stamp_detector.predict(image)

                    MeatClassifierHandler.logger.info('Sanitizing bruises. Image ID: {}'.format(image_id))
                    sanitized_bruises = BruiseUtils.sanitize_bruises(bruise_detection_results, stamp_detection_results)

                    MeatClassifierHandler.logger.info('Obtaining cuts maps. Image ID: {}'.format(image_id))
                    cuts_coords = CutsUtils.get_cuts(image, side_detection_result, side_a_shape_predictor,
                                                     side_b_shape_predictor)

                    MeatClassifierHandler.logger.info('Mapping bruises in cuts. Image ID: {}'.format(image_id))
                    cut_lines_image, cuts_mask,binary_mask = CutsUtils.get_cuts_mask_and_cut_lines_image(cuts_coords, image)

                    cut_lines_image = BruiseUtils.draw_bruises_on_cut_lines_image(cut_lines_image, side_detection_result,
                                                                                      sanitized_bruises, cuts_mask, binary_mask)
                    MeatClassifierHandler.logger.info('Saving cuts. Image ID: {}'.format(image_id))
                    CutsUtils.save_cuts_data(image_id, cuts_coords)

                    MeatClassifierHandler.logger.info('Saving bruises. Image ID: {}'.format(image_id))

                    extension_lesion_is_enable = ConfigurationStorageController.get_config_data_value(
                            ConfigurationEnum.MODULE_EXTENSION_LESION.name)
                    BruiseUtils.save_bruises_data(cuts_mask, binary_mask,side_detection_result, sanitized_bruises, image_id, cuts_coords,extension_lesion_is_enable)


                    carcass_information_already_exists = CarcassInformationController.carcass_information_already_exists(
                        image_id)

                    if not carcass_information_already_exists:
                        CarcassInformationController.initialize_carcass_information(image_id)

                    grease_color_classification_is_enabled = ConfigurationStorageController.get_config_data_value(
                        ConfigurationEnum.MODULE_GREASE_PREDICTION.name)

                    if grease_color_classification_is_enabled:
                        grease_color_id = GreaseColorUtils.predict(grease_color_detector, image, binary_mask)
                        CarcassInformationController.update_grease_color(image_id, grease_color_id)

                    conformation_classification_is_enabled = ConfigurationStorageController.get_config_data_value(
                        ConfigurationEnum.MODULE_CONFORMATION_PREDICTION.name)

                    if conformation_classification_is_enabled:
                        conformation_result = ClassifierUtils.predict(conformation_detector, image)

                        if conformation_result is not None:
                            conformation_id = ConformationEnum[conformation_result['label']].value
                            CarcassInformationController.update_conformation(image_id, conformation_id)



                    size_prediction_is_enabled = ConfigurationStorageController.get_config_data_value(
                        ConfigurationEnum.MODULE_SIZE_PREDICTION.name)


                    if size_prediction_is_enabled:
                        width, height, size_descriptor = SkeletonSizeUtils.get_size(binary_mask, cuts_coords)

                        CarcassInformationController.update_width(image_id, width)
                        CarcassInformationController.update_height(image_id, height)
                        CarcassInformationController.update_size_descriptor(image_id, size_descriptor)

                    hump_classification_is_enabled = ConfigurationStorageController.get_config_data_value(
                        ConfigurationEnum.MODULE_HUMP_PREDICTION.name)

                    if hump_classification_is_enabled:
                        if side_detection_result['label'] == 'LADO_B':
                            MeatClassifierHandler.logger.info('Classifying. Image ID: {}'.format(image_id))
                            hump_result = ClassifierUtils.predict(hump_detector, image)
                            hump_id = HumpUtils.get_hump_id(hump_result)
                        else:
                            hump_id = HumpEnum.AUSENTE.value

                        CarcassInformationController.update_hump(image_id, hump_id)

                    breed_classification_is_enabled = ConfigurationStorageController.get_config_data_value(
                        ConfigurationEnum.MODULE_BREED_PREDICTION.name)

                    if breed_classification_is_enabled:
                        breed_result = ClassifierUtils.predict(breed_detector, image)
                        if breed_result:
                            breed_id = BreedUtils.get_breed_id(breed_result)
                            CarcassInformationController.update_breed(image_id, breed_id)

                    generate_watermark_is_enabled = ConfigurationStorageController.get_config_data_value(
                    ConfigurationEnum.MODULE_GENERATE_WATERMARK.name)

                    if generate_watermark_is_enabled:

                        cut_lines_image = WatermarkUtils.get_image_with_watermarker(cut_lines_image)
                        image = WatermarkUtils.get_image_with_watermarker(image)

                        cut_lines_image = imutils.resize(cut_lines_image, height=1920)
                        image = imutils.resize(image, height=1920)

                        cv2.imwrite(masked_image_absolute_path, cut_lines_image)
                        FileUtils.copy_file(image_absolute_path)
                        cv2.imwrite(image_absolute_path, image)

                    else:

                        cv2.imwrite(masked_image_absolute_path, cut_lines_image)

                    module_cut_classification_is_enabled = ConfigurationStorageController.get_config_data_value(
                        ConfigurationEnum.MODULE_CUT_CLASSIFICATION.name)

                    if module_cut_classification_is_enabled:
                        affected_cuts = BruiseUtils.get_bruises_in_cuts(image_id)
                        for cut_name, cut_model in cuts_classification_models.items():


                            cut_image = CutsUtils.get_cut_image_without_background(cuts_coords, image, cut_name)

                            cut_classification_id = ClassifierUtils.get_cut_classification_id(cut_model, cut_image,cut_name, affected_cuts)



                            CutsGradingController.insert(image_id, cut_classification_id, CutsEnum[cut_name].value)

                            cut_and_meat_classification_correlation = ClassifierUtils.get_cut_and_meat_classification_correlation(
                                classification_id, cut_classification_id)

                            if cut_and_meat_classification_correlation is not None:
                                CutsGradingController.update_correlation_information(image_id, cut_and_meat_classification_correlation)








                MeatClassifierHandler.logger.info(
                    'Updating the image classification to: {}. Image ID: {}'.format(classification_id, image_id))
                ImageController.update_classification(classification_id, image_id)



            MeatClassifierHandler.logger.info(
                'Updating the image state to: {}. Image ID: {}'.format(ImageStateEnum.WAITING_INTEGRATION.name,
                                                                       image_id))
            ImageController.update_status(ImageStateEnum.WAITING_INTEGRATION.value, image_id)

            if reprocess_retroactive_days:
                ImageController.update_filter_data(filter_label, filter_confidence, image_id)


        except:
            traceback.print_exc()
            classification_id = ClassificationErrorEnum.ERRO_101.value
            MeatClassifierHandler.logger.info(
                'Updating the image classification to: {}. Image ID: {}'.format(classification_id, image_id))
            ImageController.update_classification(classification_id, image_id)
            MeatClassifierHandler.logger.info(
                'Updating the image state to: {}. Image ID: {}'.format(ImageStateEnum.WAITING_INTEGRATION.name,
                                                                       image_id))
            ImageController.update_status(ImageStateEnum.WAITING_INTEGRATION.value, image_id)

            if reprocess_retroactive_days:
                ImageController.update_filter_data(filter_label, filter_confidence, image_id)

