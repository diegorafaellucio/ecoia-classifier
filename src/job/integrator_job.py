from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum
import requests
import time
import logging


class IntegratorJob():
    logger = logging.getLogger(__name__)

    @staticmethod
    def do():

        IntegratorJob.logger.info('Starting job.')
        jobs_wakeup_delay = ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.JOBS_WAKEUP_DELAY.name)

        time.sleep(jobs_wakeup_delay)

        integrator_module_endpoint = ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.INTEGRATOR_MODULE_ENDPOINT.name)



        payload = {}
        headers = {}

        while True:
            integrator_module_is_active = ConfigurationStorageController.get_config_data_value(
                ConfigurationEnum.INTEGRATOR_MODULE_IS_ACTIVE.name)

            integrator_module_interval_delay = ConfigurationStorageController.get_config_data_value(
                ConfigurationEnum.INTEGRATOR_MODULE_INTERVAL_DELAY.name)

            if integrator_module_is_active:

                IntegratorJob.logger.info('Requesting a new batch processing.')
                response = requests.request("POST", integrator_module_endpoint, headers=headers, data=payload)
                IntegratorJob.logger.info(response)


            time.sleep(integrator_module_interval_delay)