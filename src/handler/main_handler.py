import logging
import concurrent.futures
from datetime import datetime

from src.controller.image_controller import ImageController
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum
from src.utils.image_utils import ImageUtils
from src.handler.image_handler import ImageHandler
from src.enum.image_state_enum import ImageStateEnum


class MainHandler:
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
                    execution_pool.submit(ImageHandler.process_image, image_id, image_path, sequence_number,
                                          side_number, roulette_number, slaughter_date, created_at,
                                          processing_timestamp, flag_img, state, aux_grading_id, classifier_suite))

                for x in concurrent.futures.as_completed(futures):
                    classification_id, image_id = x.result()
                    ImageController.update_image_status(ImageStateEnum.PROCESSED.value, image_id)
        else:

            MainHandler.logger('Was not images to process...')
