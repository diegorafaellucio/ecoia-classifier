from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum
import requests
import time
import logging

class MeatClassifierJob():
    logger = logging.getLogger(__name__)

    @staticmethod
    def do():

        MeatClassifierJob.logger.info('Starting job.')
        jobs_wakeup_delay = ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.JOBS_WAKEUP_DELAY.name)

        time.sleep(jobs_wakeup_delay)

        meat_classifier_endpoint = ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.MEAT_CLASSIFIER_MODULE_ENDPOINT.name)

        meat_classifier_interval_delay = ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.MEAT_CLASSIFIER_MODULE_INTERVAL_DELAY.name)

        payload = {}
        headers = {}

        while True:
            meat_classifier_module_is_active = ConfigurationStorageController.get_config_data_value(
                ConfigurationEnum.MEAT_CLASSIFIER_MODULE_IS_ACTIVE.name)

            if meat_classifier_module_is_active:
                MeatClassifierJob.logger.info('Requesting a new batch processing.')
                response = requests.request("POST", meat_classifier_endpoint, headers=headers, data=payload)
                MeatClassifierJob.logger.info(response)

            time.sleep(meat_classifier_interval_delay)