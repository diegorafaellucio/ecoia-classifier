from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum
from src.handler.integrator_handler import IntegratorHandler
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


        while True:
            integrator_module_is_active = ConfigurationStorageController.get_config_data_value(
                ConfigurationEnum.INTEGRATOR_MODULE_IS_ACTIVE.name)

            integrator_module_interval_delay = ConfigurationStorageController.get_config_data_value(
                ConfigurationEnum.INTEGRATOR_MODULE_INTERVAL_DELAY.name)

            time.sleep(integrator_module_interval_delay)

            if integrator_module_is_active:
                # IntegratorJob.logger.info('Requesting a new batch processing.')
                IntegratorHandler.process_images()


