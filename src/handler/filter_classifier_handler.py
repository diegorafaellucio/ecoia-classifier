from src.handler.classifier_handler import ClassifierHandler
from src.utils.detector_utils import DetectorUtils
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum

class FilterClassifierHandler(ClassifierHandler):


    @staticmethod
    def classify(detector, image):

        image_height, image_width = image.shape[:2]
        detection_results = detector.detect(image)
        best_result = DetectorUtils.get_best_detection(detection_results, image_height, image_width)

        return best_result

    @staticmethod
    def predicted_result_is_in_black_list(result):

        filter_black_list = ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.FILTER_BLACK_LIST.name)

        filter_label = result['label']

        if filter_label in filter_black_list:
            return True
        else:
            return False

