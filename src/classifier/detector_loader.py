from src.classifier.yolo_classifier.detector import Detector as YoloDetector
from src.classifier.ultralytics_detector.detector import Detector as UltralyticsDetector
from src.enum.detection_approach_enum import DetectionApproachEnum


class DetectorLoader():

    @staticmethod
    def load_detector(model_path, detection_framework):

        detector = None

        if detection_framework == DetectionApproachEnum.ULTRALYTICS.value:
            detector = UltralyticsDetector(model_path)

        elif detection_framework == DetectionApproachEnum.YOLO.value:
            detector = YoloDetector(model_path)

        return detector





