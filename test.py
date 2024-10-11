import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")
import cv2

from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum
from src.ml.classifier.detector_loader import DetectorLoader

from src.ml.classifier.yolo_classifier.detector import Detector as YoloDetector
from src.ml.classifier.ultralytics_classifier.detector import Detector as UltralyticsDetector



filter_classification_weights_path = ConfigurationStorageController.get_config_data_value(
    ConfigurationEnum.FILTER_CLASSIFICATION_WEIGHTS_PATH.name)
# filter_classification_approach = ConfigurationStorageController.get_config_data_value(
#     ConfigurationEnum.FILTER_CLASSIFICATION_APPROACH.name)

# filter_detector = DetectorLoader.load_detector(filter_classification_weights_path,filter_classification_approach)

detector_ultralytics = UltralyticsDetector(filter_classification_weights_path)
detector_yolo = YoloDetector(filter_classification_weights_path)

image = cv2.imread('/home/diego/Pictures/2024-03-28_08-49.png')

detector_ultralytics.detect(image)

print()

