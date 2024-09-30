import logging
from django.urls import path
from src.ml.classifier.detector_loader import DetectorLoader
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum
from src.enum.job_name_enum import JobNameEnum
from apps.meat_classifier.views.classify_view import ClassifyView
from apps.meat_classifier.views.job_status_view import JobStatusView
from src.ml.shape_predictor.shape_predictor import ShapePredictor
from src.job.meat_classifier_job import MeatClassifierJob
import threading

logger = logging.getLogger(__name__)

ConfigurationStorageController. initialize_configs()

skeleton_classification_weights_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.SKELETON_CLASSIFICATION_WEIGHTS_PATH.name)

skeleton_classification_approach = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.SKELETON_CLASSIFICATION_APPROACH.name)
skeleton_detector = DetectorLoader.load_detector(skeleton_classification_weights_path, skeleton_classification_approach)

filter_classification_weights_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.FILTER_CLASSIFICATION_WEIGHTS_PATH.name)
filter_classification_approach = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.FILTER_CLASSIFICATION_APPROACH.name)
filter_detector = DetectorLoader.load_detector(filter_classification_weights_path,filter_classification_approach)

side_classification_weights_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.SIDE_CLASSIFICATION_WEIGHTS_PATH.name)
side_classification_approach = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.SIDE_CLASSIFICATION_APPROACH.name)
side_detector = DetectorLoader.load_detector(side_classification_weights_path,side_classification_approach)

meat_classification_weights_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.MEAT_CLASSIFICATION_WEIGHTS_PATH.name)
meat_classification_approach = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.MEAT_CLASSIFICATION_APPROACH.name)
meat_detector = DetectorLoader.load_detector(meat_classification_weights_path, meat_classification_approach)

bruise_classification_weights_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.BRUISE_CLASSIFICATION_WEIGHTS_PATH.name)
bruise_classification_approach = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.BRUISE_CLASSIFICATION_APPROACH.name)
bruise_detector = DetectorLoader.load_detector(bruise_classification_weights_path, bruise_classification_approach)

stamp_classification_weights_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.STAMP_CLASSIFICATION_WEIGHTS_PATH.name)
stamp_classification_approach = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.STAMP_CLASSIFICATION_APPROACH.name)
stamp_detector = DetectorLoader.load_detector(stamp_classification_weights_path, stamp_classification_approach)


conformation_classification_weights_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.CONFORMATION_CLASSIFICATION_WEIGHTS_PATH.name)
conformation_classification_approach = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.CONFORMATION_CLASSIFICATION_APPROACH.name)
conformation_detector = DetectorLoader.load_detector(conformation_classification_weights_path, conformation_classification_approach)

side_a_shape_predictor_weights_file_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.SIDE_A_SHAPE_PREDICTOR_WEIGHTS_FILE_PATH.name)
side_a_shape_predictor = ShapePredictor(side_a_shape_predictor_weights_file_path)

side_b_shape_predictor_weights_file_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.SIDE_B_SHAPE_PREDICTOR_WEIGHTS_FILE_PATH.name)
side_b_shape_predictor = ShapePredictor(side_b_shape_predictor_weights_file_path)

grease_color_detector = DetectorLoader.load_detector(ConfigurationStorageController.get_config_data_value(ConfigurationEnum.GREASE_CLASSIFICATION_WEIGHTS_PATH.name), ConfigurationEnum.GREASE_CLASSIFICATION_APPROACH.value)

hump_classification_weights_path = ConfigurationStorageController.get_config_data_value(ConfigurationEnum.HUMP_CLASSIFICATION_WEIGHTS_PATH.name)
hump_classification_approach = ConfigurationStorageController.get_config_data_value(ConfigurationEnum.HUMP_CLASSIFICATION_APPROACH.name)
hump_detector = DetectorLoader.load_detector(hump_classification_weights_path, hump_classification_approach)

breed_classification_weights_path = ConfigurationStorageController.get_config_data_value(ConfigurationEnum.BREED_CLASSIFICATION_WEIGHTS_PATH.name)
breed_classification_approach = ConfigurationStorageController.get_config_data_value(ConfigurationEnum.BREED_CLASSIFICATION_APPROACH.name)
breed_detector = DetectorLoader.load_detector(breed_classification_weights_path, breed_classification_approach)

classifier_suite = [skeleton_detector, filter_detector, side_detector, meat_detector, bruise_detector, stamp_detector,
                    side_a_shape_predictor, side_b_shape_predictor, grease_color_detector, conformation_detector, hump_detector, breed_detector]


meat_classifier_job_thread = threading.Thread(target=MeatClassifierJob.do, name=JobNameEnum.CLASSIFIER.value)
meat_classifier_job_thread.start()

urlpatterns = [
    path("classify", ClassifyView.as_view(), {'classifier_suite': classifier_suite}),
    path("job_status", JobStatusView.as_view(), {'meat_classifier_job_thread': meat_classifier_job_thread}),
]
