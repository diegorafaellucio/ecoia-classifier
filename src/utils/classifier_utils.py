from src.utils.detector_utils import DetectorUtils
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum
from src.enum.classification_error_enum import ClassificationErrorEnum
from src.controller.image_controller import ImageController
from src.enum.meat_enum import MeatEnum
class ClassifierUtils:


    @staticmethod
    def classify(detector, image):

        image_height, image_width = image.shape[:2]
        detection_results = detector.detect(image)
        best_result = DetectorUtils.get_best_detection(detection_results, image_height, image_width)

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

        # ClassifierHandler.logger.info(
        #     f'Checking if a skeleton is present to sequence: {sequence_number} and side: {side_number}')



        skeleton_detection_result = ClassifierUtils.classify(skeleton_detector, image)

        if skeleton_detection_result is None:
            classification_id = ClassificationErrorEnum.ERRO_92.value
            filter_label = 'NAO_CLASSIFICADO'
            filter_confidence = 0.0

        else:

            side_detection_result = ClassifierUtils.classify(side_detector, image)

            filter_detection_result = ClassifierUtils.classify(filter_detector, image)

            if side_detection_result is None:
                classification_id = ClassificationErrorEnum.ERRO_92.value
                filter_label = 'NAO_CLASSIFICADO'
                filter_confidence = 0.0

            else:

                if filter_detection_result is None:
                    classification_id = ClassificationErrorEnum.ERRO_95.value


                    filter_label = 'NAO_CLASSIFICADO'
                    filter_confidence = 0.0
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
                            classification_id = ClassificationErrorEnum.ERRO_96.value
                        else:
                            meat_detection_label = meat_detection_result['label']

                            meat_detataset_id = MeatEnum[meat_detection_label].value['database_id']

                            classification_id = meat_detataset_id

        return classification_id, filter_label, filter_confidence