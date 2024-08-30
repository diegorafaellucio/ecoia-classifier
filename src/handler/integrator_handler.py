import logging
import concurrent.futures
import os.path
import json
import imutils

from src.controller.image_controller import ImageController
from src.controller.integration_log_controller import IntegrationLogController
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum
from src.enum.image_state_enum import ImageStateEnum
from src.utils.file_utils import FileUtils
from src.utils.bruise_utils import BruiseUtils
from src.utils.integrator_utils import IntegratorUtils
from src.utils.date_utils import DateUtils
from src.controller.aux_grading_controller import AuxGradingController


class IntegratorHandler:
    logger = logging.getLogger(__name__)

    @staticmethod
    def process_images():

        max_workers = ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.INTEGRATOR_MAX_WORKERS.name)

        execution_pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)

        data = ImageController.get_images_to_integrate(max_workers)

        have_data_to_integrate = FileUtils.have_files_to_process(data)

        futures = []

        if have_data_to_integrate:
            for item in data:
                image_id = item[0]
                image_path = item[1]
                sequence_number = item[2]
                side_number = item[3]
                roulette_number = item[4]
                slaughter_date = item[5]
                created_at = item[6]
                processed_at = item[7]
                flag_img = item[8]
                state = item[9]
                aux_grading_id = item[10]

                futures.append(
                    execution_pool.submit(IntegratorHandler.process_image, image_id, image_path, sequence_number,
                                          side_number, roulette_number, slaughter_date, created_at,
                                          processed_at, flag_img, state, aux_grading_id))

            for x in concurrent.futures.as_completed(futures):
                image_id = x.result()
        else:

            IntegratorHandler.logger.info('Was not data to integrate!')

    @staticmethod
    def process_image(image_id, image_path, sequence_number, side_number, roulette_number, slaughter_date, created_at,
                      processed_at, flag_img, state, aux_grading_id):



        IntegratorHandler.logger.info('Starting to integrate data. Image ID: {}.'.format(image_id))
        ImageController.update_image_status(ImageStateEnum.INTEGRATING.value, image_id)


        slaughter_start_interval = DateUtils.get_start_interval_from_created_at()
        slaughter_finish_interval = DateUtils.get_finish_interval_from_created_at()


        integration_endpoint = ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.INTEGRATION_ENDPOINT.name)

        if len(integration_endpoint) != 0:

            if slaughter_start_interval < created_at < slaughter_finish_interval:

                has_integration_to_image = IntegrationLogController.has_integration_to_image(image_id)

                if has_integration_to_image:

                    images_endpoint = ConfigurationStorageController.get_config_data_value(
                        ConfigurationEnum.IMAGES_ENDPOINT.name)

                    image_path = images_endpoint + image_path
                    classification_name = AuxGradingController.get_name_by_id(aux_grading_id)
                    classification_score = AuxGradingController.get_score_by_id(aux_grading_id)

                    IntegratorHandler.logger.info('Collecting bruise and cuts data to integrate. Image ID: {}.'.format(image_id))
                    bruise_data = BruiseUtils.get_bruise_integration_data(image_id)

                    integration_dict = \
                        [{
                            "id_imagem": int(image_id),
                            "imagem": image_path,
                            "nr_sequencial": int(sequence_number),
                            "nr_banda": int(side_number),
                            "nr_carretilha": roulette_number if roulette_number is None else int(roulette_number),
                            "dt_abate": str(slaughter_date),
                            "data_hora_hora_processamento": str(processed_at),
                            "data_hora_registro": str(created_at),
                            "dados": {
                                "id_classificacao": classification_score,
                                "label_classificacao": classification_name,
                                "lesoes": bruise_data
                            }
                        }]

                    integration_string = json.dumps(integration_dict)

                    integration_endpoint = integration_endpoint.format(sequence_number, side_number)

                    IntegratorHandler.logger.info(
                        'Sending data to client endpoint. Image ID: {}.'.format(image_id))
                    return_code, elapsed_time  = IntegratorUtils.integrate_data(integration_endpoint, integration_string)


                    IntegrationLogController.insert_into_integration_log(image_id, return_code, elapsed_time, integration_string)

        IntegratorHandler.logger.info(
            'Updating the image state to: {}. Image ID: {}'.format(ImageStateEnum.PROCESSED.name,
                                                                   image_id))
        ImageController.update_image_status(ImageStateEnum.PROCESSED.value, image_id)

        return image_id




