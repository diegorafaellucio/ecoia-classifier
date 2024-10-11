from src.controller.aux_model_controller import ModelController
from src.controller.model_update_history_controller import ModelUpdateHistoryController
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum
from src.enum.detection_approach_enum import DetectionApproachEnum
from src.utils.git_utils import GitUtils
from git import Repo
import os
from pathlib import Path
import logging

class ModelUtils:
    logger = logging.getLogger(__name__)

    @staticmethod
    def initialize_models():
        client_identifier = ConfigurationStorageController.get_config_data_value(ConfigurationEnum.CLIENT_IDENTIFIER.name)
        plant_identifier = ConfigurationStorageController.get_config_data_value(ConfigurationEnum.PLANT_IDENTIFIER.name)

        plant_models_identifier = '-'.join([client_identifier, plant_identifier])

        base_path = Path(__file__).resolve().parent.parent.parent
        models_path =  os.path.join(base_path, ConfigurationStorageController.get_config_data_value(ConfigurationEnum.MODELS_PATH.name))

        models = os.listdir(models_path)
        counter = 0
        for model in models:
            is_model_in_database = ModelController.is_model_in_database(model)
            

            if not is_model_in_database:

                model_path = os.path.join(models_path, model)
                GitUtils.perform_checkout(model_path, 'main')

                most_recent_branch = GitUtils.get_most_recent_branch_based_into_model_identifier(model_path, plant_models_identifier)
                GitUtils.perform_checkout(model_path, most_recent_branch)

                model_version = GitUtils.get_project_current_version(model_path)
                model_weight_path = "data/models/{}/weight.pt".format(model)
                model_approach = DetectionApproachEnum.ULTRALYTICS.value

                # print(model,model_version)

                ModelController.insert_into_aux_model(model, most_recent_branch, model_weight_path, model_approach)

                ModelUtils.logger.info('{} model: initialized with branch {}'.format(model, most_recent_branch))
            else:
                ModelUtils.logger.info('{} model: was initialized befeore.'.format(model))
    @staticmethod
    def update_models():
        client_identifier = ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.CLIENT_IDENTIFIER.name)
        plant_identifier = ConfigurationStorageController.get_config_data_value(ConfigurationEnum.PLANT_IDENTIFIER.name)

        plant_models_identifier = '-'.join([client_identifier, plant_identifier])

        base_path = Path(__file__).resolve().parent.parent.parent
        models_path = os.path.join(base_path, ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.MODELS_PATH.name))
        # models_without_current_version = AuxModelController.get_models_without_curent_version()

        models = os.listdir(models_path)
        for model in models:



            model_id, model_current_version = ModelController.get_model_id_and_current_version(model)

            model_path = os.path.join(models_path, model)

            most_recent_branch = GitUtils.get_most_recent_branch_based_into_model_identifier(model_path,
                                                                                                 plant_models_identifier)

            # most_recent_branch_version = GitUtils.get_version_from_branch_name(most_recent_branch)

            if model_current_version != most_recent_branch:
                GitUtils.perform_checkout(model_path, most_recent_branch)


                ModelUpdateHistoryController.insert_into_model_update_history(model_id, model_current_version, most_recent_branch)
                ModelController.update_model_version(most_recent_branch, model)

                ModelUtils.logger.info('{} model: updating from {} to {}.'.format(model, model_current_version, most_recent_branch))
            else:
                ModelUtils.logger.info('{} model: No updates available!'.format(model))

