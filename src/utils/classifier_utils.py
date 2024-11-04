from src.utils.object_detection_utils import ObjectDetectionUtils
from src.utils.image_classification_utils import ImageClassificationUtils
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum
from src.enum.classification_error_enum import ClassificationErrorEnum
from src.enum.meat_enum import MeatEnum
from src.enum.bruises_enum import BruisesEnum
from src.enum.cut_and_meat_classification_correlation_enum import CutAndMeatClassificationCorrelationEnum
class ClassifierUtils:


    @staticmethod
    def predict(classifier, image, image_classification = False):

        image_height, image_width = image.shape[:2]
        prediction_results = classifier.predict(image, image_classification)
        if not image_classification:
            best_result = ObjectDetectionUtils.get_best_result(prediction_results, image_height, image_width)
            return best_result
        else:
            best_result = ImageClassificationUtils.get_best_result(prediction_results)
            return best_result


    @staticmethod
    def predicted_result_is_in_black_list(result, filter_black_list):


        filter_label = result['label']

        if filter_label in filter_black_list:
            return True
        else:
            return False

    @staticmethod
    def get_cut_classification_id(classifer, cut_image, affected_cuts, cut_name):


        cut_classification_result = ClassifierUtils.predict(classifer, cut_image, image_classification=True)

        classification_id = ClassificationErrorEnum.ERRO_200.value

        bruises = affected_cuts[cut_name]

        if BruisesEnum.LEVE.key in bruises or BruisesEnum.MODERADA.key in bruises or BruisesEnum.GRAVE.key in bruises:
            classification_id = ClassificationErrorEnum.ERRO_201.value
        elif BruisesEnum.FALHA.key in bruises:
            classification_id = ClassificationErrorEnum.ERRO_202.value
        elif BruisesEnum.LEVE.key in bruises or BruisesEnum.MODERADA.key in bruises or BruisesEnum.GRAVE.key in bruises or BruisesEnum.FALHA.key in bruises:
            classification_id = ClassificationErrorEnum.ERRO_203.value
        else:

            if cut_classification_result is not None:
                cut_classification_label = cut_classification_result['label']

                meat_classification_id = MeatEnum[cut_classification_label].value['database_id']

                classification_id = meat_classification_id

        return classification_id


    @staticmethod
    def get_classification_id(image, skeleton_detector, filter_detector, meat_detector):

        classification_id = None

        # ClassifierHandler.logger.info(
        #     f'Checking if a skeleton is present to sequence: {sequence_number} and side: {side_number}')

        skeleton_detection_result = ClassifierUtils.predict(skeleton_detector, image)

        if skeleton_detection_result is None:
            classification_id = ClassificationErrorEnum.ERRO_92.value
            filter_label = 'NAO_CLASSIFICADO'
            filter_confidence = 0.0

        else:
            filter_detection_result = ClassifierUtils.predict(filter_detector, image)

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

                    meat_detection_result = ClassifierUtils.predict(meat_detector, image)

                    if meat_detection_result is None:
                        classification_id = ClassificationErrorEnum.ERRO_96.value
                    else:
                        meat_classification_label = meat_detection_result['label']

                        meat_classification_id = MeatEnum[meat_classification_label].value['database_id']

                        classification_id = meat_classification_id

        return classification_id, filter_label, filter_confidence

    @staticmethod
    def get_cut_and_meat_classification_correlation(meat_classification_id, cut_classification_id):

        correlation = ""

        if meat_classification_id == cut_classification_id:
            correlation = CutAndMeatClassificationCorrelationEnum.IN_COMPLIANCE.value
        elif cut_classification_id > meat_classification_id:
            correlation = CutAndMeatClassificationCorrelationEnum.POSITIVE.value
        elif cut_classification_id < meat_classification_id:
            correlation = CutAndMeatClassificationCorrelationEnum.NEGATIVE.value

        return correlation

