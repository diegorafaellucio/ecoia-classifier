from src.ml.classifier.yolo_classifier.detector import Detector as YoloDetector
from src.ml.classifier.ultralytics_classifier.detector import Detector as UltralyticsDetector
from src.enum.detection_approach_enum import DetectionApproachEnum
from django.conf import settings
import os


class DetectorLoader():

    @staticmethod
    def load_detector(model_path, detection_framework):

        base_dir = settings.BASE_DIR

        detector = None

        if detection_framework == DetectionApproachEnum.ULTRALYTICS.value:

            model_path = os.path.join(base_dir, model_path )
            detector = UltralyticsDetector(model_path)
        elif detection_framework == DetectionApproachEnum.YOLO.value:
            model_path = os.path.join(base_dir, model_path )
            detector = YoloDetector(model_path)

        return detector





