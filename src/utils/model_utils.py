from src.controller.model_controller import ModelController
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

        main_branch = 'main'
        for model in models:
            is_model_in_database = ModelController.is_model_in_database(model)
            

            if not is_model_in_database:

                model_path = os.path.join(models_path, model)

                GitUtils.perform_checkout(model_path, main_branch)

                GitUtils.remove_all_not_active_branchs(main_branch,model_path)

                most_recent_branch = GitUtils.get_most_recent_branch_based_into_model_identifier(model_path, plant_models_identifier)
                GitUtils.perform_checkout(model_path, most_recent_branch)

                GitUtils.remove_all_not_active_branchs(most_recent_branch, model_path)

                model_weight_path = "data/models/{}/weight.pt".format(model)
                model_approach = DetectionApproachEnum.ULTRALYTICS.value

                ModelController.insert(model, most_recent_branch, model_weight_path, model_approach)

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

        models = os.listdir(models_path)
        for model in models:
            model_path = os.path.join(models_path, model)

            model_current_version = 'main'#GitUtils.get_current_version(model_path)

            GitUtils.remove_all_not_active_branchs(model_current_version, model_path)

            model_id = ModelController.get_id(model)


            model_most_recent_version = GitUtils.get_most_recent_branch_based_into_model_identifier(model_path,
                                                                                                 plant_models_identifier)

            if model_current_version != model_most_recent_version:
                GitUtils.perform_checkout(model_path, model_most_recent_version)

                GitUtils.remove_all_not_active_branchs(model_most_recent_version, model_path)


                ModelUpdateHistoryController.insert_into_model_update_history(model_id, model_current_version, model_most_recent_version)
                ModelController.update_version(model_most_recent_version, model)

                ModelUtils.logger.info('{} model: updating from {} to {}.'.format(model, model_current_version, model_most_recent_version))
            else:
                ModelUtils.logger.info('{} model: No updates available!'.format(model))

