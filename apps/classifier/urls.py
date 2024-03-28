import logging
from django.urls import path
from src.detector import Detector
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum
from apps.classifier.views import ClassifierView
from src.shape_predictor.shape_predictor import ShapePredictor

logger = logging.getLogger(__name__)

ConfigurationStorageController.initialize_configs()

skeleton_classification_weights_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.SKELETON_CLASSIFICATION_WEIGHTS_PATH.name)
skeleton_detector = Detector(skeleton_classification_weights_path)

filter_classification_weights_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.FILTER_CLASSIFICATION_WEIGHTS_PATH.name)
filter_detector = Detector(filter_classification_weights_path)

side_classification_weights_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.SIDE_CLASSIFICATION_WEIGHTS_PATH.name)
side_detector = Detector(side_classification_weights_path)

meat_classification_weights_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.MEAT_CLASSIFICATION_WEIGHTS_PATH.name)
meat_detector = Detector(meat_classification_weights_path)

bruise_classification_weights_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.MEAT_CLASSIFICATION_WEIGHTS_PATH.name)
bruise_detector = Detector(bruise_classification_weights_path)

side_a_shape_predictor_weights_file_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.SIDE_A_SHAPE_PREDICTOR_WEIGHTS_FILE_PATH.name)
side_a_shape_predictor = ShapePredictor(side_a_shape_predictor_weights_file_path)

side_b_shape_predictor_weights_file_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.SIDE_B_SHAPE_PREDICTOR_WEIGHTS_FILE_PATH.name)
side_b_shape_predictor = ShapePredictor(side_b_shape_predictor_weights_file_path)

classifier_suite = [skeleton_detector, filter_detector, side_detector, meat_detector, bruise_detector,
                    side_a_shape_predictor, side_b_shape_predictor]

urlpatterns = [
    path("classifier", ClassifierView.as_view(), {'classifier_suite': classifier_suite}),
]
