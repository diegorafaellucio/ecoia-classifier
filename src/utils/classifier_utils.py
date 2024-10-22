from src.utils.detector_utils import DetectorUtils
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum
from src.enum.classification_error_enum import ClassificationErrorEnum
from src.controller.image_controller import ImageController
from src.enum.meat_enum import MeatEnum
class ClassifierUtils:


    @staticmethod
    def classify(detector, image, get_intersection_score=False):

        image_height, image_width = image.shape[:2]
        detection_results = detector.detect(image)

        if get_intersection_score:
            best_result, intersection_score = DetectorUtils.get_best_detection(detection_results, image_height, image_width, get_intersection_score)
            return best_result, intersection_score
        else:
            best_result = DetectorUtils.get_best_detection(detection_results, image_height, image_width, get_intersection_score)
            return best_result


    @staticmethod
    def predicted_result_is_in_black_list(result, filter_black_list):


        filter_label = result['label']

        if filter_label in filter_black_list:
            return True
        else:
            return False


    @staticmethod
    def get_classification_id(image_id, image, skeleton_detector, filter_detector, meat_detector, side_detector):
        classification_id = None
        filter_label = 'NAO_CLASSIFICADO'
        filter_confidence = 0.0
        side_detection_result = None

        skeleton_detection_result, intersection_score = ClassifierUtils.classify(skeleton_detector, image, get_intersection_score=True)

        if skeleton_detection_result is None:
            classification_id = ClassificationErrorEnum.ERRO_93.value

        else:

            intersection_threshold =ConfigurationStorageController.get_config_data_value(
                ConfigurationEnum.SKELETON_CLASSIFICATION_INTERSECTION_THRESHOLD.name)

            if intersection_score < intersection_threshold:
                classification_id = ClassificationErrorEnum.ERRO_94.value

            else:

                side_detection_result = ClassifierUtils.classify(side_detector, image)

                if side_detection_result is None:
                    classification_id = ClassificationErrorEnum.ERRO_102.value

                else:

                    filter_detection_result = ClassifierUtils.classify(filter_detector, image)

                    if filter_detection_result is None:
                        classification_id = ClassificationErrorEnum.ERRO_100.value

                    else:

                        filter_label = filter_detection_result['label']
                        filter_confidence = filter_detection_result['confidence']

                        filter_black_list = ConfigurationStorageController.get_config_data_value(
                            ConfigurationEnum.FILTER_BLACK_LIST.name)

                        filter_in_black_List = ClassifierUtils.predicted_result_is_in_black_list(
                            filter_detection_result, filter_black_list)

                        if filter_in_black_List:
                            classification_id = ClassificationErrorEnum.ERRO_97.value
                        else:

                            meat_detection_result = ClassifierUtils.classify(meat_detector, image)

                            if meat_detection_result is None:
                                classification_id = ClassificationErrorEnum.ERRO_101.value
                            else:
                                meat_detection_label = meat_detection_result['label']

                                meat_detataset_id = MeatEnum[meat_detection_label].value['database_id']

                                classification_id = meat_detataset_id

        return classification_id, filter_label, filter_confidence, side_detection_result