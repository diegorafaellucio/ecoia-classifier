import logging
from django.urls import path
from src.ml.loader.classifier_loader import ClassifierLoader
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum
from src.enum.job_name_enum import JobNameEnum
from src.enum.cuts_enum import CutsEnum
from apps.meat_classifier.views.classify_view import ClassifyView
from apps.meat_classifier.views.job_status_view import JobStatusView
from src.ml.shape_predictor.shape_predictor import ShapePredictor
from src.job.meat_classifier_job import MeatClassifierJob
import threading
from src.utils.configuration_storage_utils import ConfigurationStorageUtils
from src.utils.model_utils import ModelUtils
import os
from pathlib import Path

logger = logging.getLogger(__name__)

ConfigurationStorageUtils.initialize_configs()
ModelUtils.initialize_models()

skeleton_classification_weights_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.SKELETON_CLASSIFICATION_WEIGHTS_PATH.name)

skeleton_classification_approach = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.SKELETON_CLASSIFICATION_APPROACH.name)
skeleton_detector = ClassifierLoader.load(skeleton_classification_weights_path, skeleton_classification_approach)

filter_classification_weights_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.FILTER_CLASSIFICATION_WEIGHTS_PATH.name)
filter_classification_approach = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.FILTER_CLASSIFICATION_APPROACH.name)
filter_detector = ClassifierLoader.load(filter_classification_weights_path, filter_classification_approach)

side_classification_weights_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.SIDE_CLASSIFICATION_WEIGHTS_PATH.name)
side_classification_approach = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.SIDE_CLASSIFICATION_APPROACH.name)
side_detector = ClassifierLoader.load(side_classification_weights_path, side_classification_approach)

meat_classification_weights_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.MEAT_CLASSIFICATION_WEIGHTS_PATH.name)
meat_classification_approach = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.MEAT_CLASSIFICATION_APPROACH.name)
meat_detector = ClassifierLoader.load(meat_classification_weights_path, meat_classification_approach)

bruise_classification_weights_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.BRUISE_CLASSIFICATION_WEIGHTS_PATH.name)
bruise_classification_approach = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.BRUISE_CLASSIFICATION_APPROACH.name)
bruise_detector = ClassifierLoader.load(bruise_classification_weights_path, bruise_classification_approach)

stamp_classification_weights_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.STAMP_CLASSIFICATION_WEIGHTS_PATH.name)
stamp_classification_approach = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.STAMP_CLASSIFICATION_APPROACH.name)
stamp_detector = ClassifierLoader.load(stamp_classification_weights_path, stamp_classification_approach)


conformation_classification_weights_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.CONFORMATION_CLASSIFICATION_WEIGHTS_PATH.name)
conformation_classification_approach = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.CONFORMATION_CLASSIFICATION_APPROACH.name)
conformation_detector = ClassifierLoader.load(conformation_classification_weights_path, conformation_classification_approach)

side_a_shape_predictor_weights_file_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.SIDE_A_SHAPE_PREDICTOR_WEIGHTS_FILE_PATH.name)
side_a_shape_predictor = ShapePredictor(side_a_shape_predictor_weights_file_path)

side_b_shape_predictor_weights_file_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.SIDE_B_SHAPE_PREDICTOR_WEIGHTS_FILE_PATH.name)
side_b_shape_predictor = ShapePredictor(side_b_shape_predictor_weights_file_path)

grease_color_detector = ClassifierLoader.load(ConfigurationStorageController.get_config_data_value(ConfigurationEnum.GREASE_CLASSIFICATION_WEIGHTS_PATH.name), ConfigurationEnum.GREASE_CLASSIFICATION_APPROACH.value)

hump_classification_weights_path = ConfigurationStorageController.get_config_data_value(ConfigurationEnum.HUMP_CLASSIFICATION_WEIGHTS_PATH.name)
hump_classification_approach = ConfigurationStorageController.get_config_data_value(ConfigurationEnum.HUMP_CLASSIFICATION_APPROACH.name)
hump_detector = ClassifierLoader.load(hump_classification_weights_path, hump_classification_approach)

breed_classification_weights_path = ConfigurationStorageController.get_config_data_value(ConfigurationEnum.BREED_CLASSIFICATION_WEIGHTS_PATH.name)
breed_classification_approach = ConfigurationStorageController.get_config_data_value(ConfigurationEnum.BREED_CLASSIFICATION_APPROACH.name)
breed_detector = ClassifierLoader.load(breed_classification_weights_path, breed_classification_approach)

cut_classifier_models = {}

module_cut_classification_available_models = ConfigurationStorageController.get_config_data_value(ConfigurationEnum.MODULE_CUT_CLASSIFICATION_AVAILABLE_MODELS.name)

base_path = Path(__file__).resolve().parent.parent.parent
models_path = os.path.join(base_path, ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.MODELS_PATH.name))

cuts_classification_models = {}

for module_cut_classification_available_model in module_cut_classification_available_models:
    model_name = CutsEnum[module_cut_classification_available_model].model_name

    cut_classification_model_path = os.path.join(models_path, model_name, 'weight.pt')

    cut_classification_model =  ClassifierLoader.load(cut_classification_model_path)

    cuts_classification_models[module_cut_classification_available_model]  = cut_classification_model


classifier_suite = [skeleton_detector, filter_detector, side_detector, meat_detector, bruise_detector, stamp_detector,
                    side_a_shape_predictor, side_b_shape_predictor, grease_color_detector, conformation_detector, hump_detector, breed_detector, cuts_classification_models]


meat_classifier_job_thread = threading.Thread(target=MeatClassifierJob.do, name=JobNameEnum.CLASSIFIER.value)
meat_classifier_job_thread.start()

urlpatterns = [
    path("classify", ClassifyView.as_view(), {'classifier_suite': classifier_suite}),
    path("job_status", JobStatusView.as_view(), {'meat_classifier_job_thread': meat_classifier_job_thread}),
]
