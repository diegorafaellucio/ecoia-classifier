from src.enum.classification_error_enum import ClassificationErrorEnum
from src.enum.meat_enum import MeatEnum
from src.enum.bruises_enum import BruisesEnum
from src.enum.cut_and_meat_classification_correlation_enum import CutAndMeatClassificationCorrelationEnum
from src.utils.object_detection_utils import ObjectDetectionUtils
from src.utils.image_classification_utils import ImageClassificationUtils

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


        if cut_name in affected_cuts:
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
    def get_classification_id(image, side_detector, meat_detector):

        classification_id = None

        side_detection_result = ClassifierUtils.predict(side_detector, image)

        if side_detection_result is None:
            classification_id = ClassificationErrorEnum.ERRO_102.value

        else:

            meat_detection_result = ClassifierUtils.predict(meat_detector, image)

            if meat_detection_result is None:
                classification_id = ClassificationErrorEnum.ERRO_101.value
            else:
                meat_classification_label = meat_detection_result['label']

                meat_classification_id = MeatEnum[meat_classification_label].value['database_id']

                classification_id = meat_classification_id

        return classification_id, side_detection_result

    @staticmethod
    def get_cut_and_meat_classification_correlation(meat_classification_id, cut_classification_id):



        correlation = None

        if cut_classification_id not in (ClassificationErrorEnum.ERRO_200.value, ClassificationErrorEnum.ERRO_201.value, ClassificationErrorEnum.ERRO_202.value, ClassificationErrorEnum.ERRO_203.value):

            meat_classification_id = int(meat_classification_id)
            cut_classification_id = int(cut_classification_id)

            if meat_classification_id == cut_classification_id:
                correlation = CutAndMeatClassificationCorrelationEnum.IN_COMPLIANCE.value
            elif cut_classification_id > meat_classification_id:
                correlation = CutAndMeatClassificationCorrelationEnum.POSITIVE.value
            elif cut_classification_id < meat_classification_id:
                correlation = CutAndMeatClassificationCorrelationEnum.NEGATIVE.value

        return correlation

