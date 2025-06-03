from src.enum.classification_error_enum import ClassificationErrorEnum
from src.enum.meat_enum import MeatEnum
from src.enum.bruises_enum import BruisesEnum
from src.enum.carcass_classification_enum import CarcassClassificationEnum
from src.enum.configuration_enum import ConfigurationEnum
from src.enum.cut_and_meat_classification_correlation_enum import CutAndMeatClassificationCorrelationEnum
from src.utils.image_classification_utils import ImageClassificationUtils
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.utils.image_utils import ImageUtils
from src.utils.detector_utils import DetectorUtils
import cv2

class ClassifierUtils:


    @staticmethod
    def predict(classifier, image, image_classification = False, get_intersection_score=False, threshold=0.05):

        image_height, image_width = image.shape[:2]
        prediction_results = classifier.predict(image, image_classification)
        if not image_classification:

            if get_intersection_score:
                best_result, intersection_score = DetectorUtils.get_best_detection(prediction_results, image_height,
                                                                                   image_width, get_intersection_score,
                                                                                   threshold)
                return best_result, intersection_score
            else:
                best_result = DetectorUtils.get_best_detection(prediction_results, image_height, image_width,
                                                               get_intersection_score, threshold)
                return best_result
            # best_result = ObjectDetectionUtils.get_best_result(prediction_results, image_height, image_width)
            # return best_result
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
    def get_cut_classification_id(classifer, cut_image, cut_name, affected_cuts):


        cut_classification_result = ClassifierUtils.predict(classifer, cut_image, image_classification=True)

        classification_id = ClassificationErrorEnum.ERRO_200.value

        if cut_name in affected_cuts.keys():
            bruises = affected_cuts[cut_name]

            if (BruisesEnum.LEVE.value in bruises or BruisesEnum.MODERADA.value in bruises or BruisesEnum.GRAVE.value in bruises) and not BruisesEnum.FALHA.value in bruises:
                classification_id = ClassificationErrorEnum.ERRO_201.value
            elif BruisesEnum.FALHA.value in bruises and not (BruisesEnum.LEVE.value in bruises or BruisesEnum.MODERADA.value in bruises or BruisesEnum.GRAVE.value in bruises):
                classification_id = ClassificationErrorEnum.ERRO_202.value
            elif BruisesEnum.FALHA.value in bruises and (BruisesEnum.LEVE.value in bruises or BruisesEnum.MODERADA.value in bruises or BruisesEnum.GRAVE.value in bruises):
                classification_id = ClassificationErrorEnum.ERRO_203.value
        else:

            if cut_classification_result is not None:
                cut_classification_label = cut_classification_result['label']

                meat_classification_id = MeatEnum[cut_classification_label].value['database_id']

                classification_id = meat_classification_id

        return classification_id


    @staticmethod
    def get_classification_id(image_id, image_path, side_detector, meat_detector, skeleton_detector, filter_detector, reprocess_retroactive_days, carcass_classification_classifier):

        classification_id = None
        filter_label = 'NAO_CLASSIFICADO'
        filter_confidence = 0.0
        side_detection_result = None
        image = None

        try:
            image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            original_image = image.copy()

            adjust_image_color_reprocess_retroactive = ConfigurationStorageController.get_config_data_value(
                ConfigurationEnum.ADJUST_IMAGE_COLOR_REPROCESS_RETROACTIVE.name)

            if adjust_image_color_reprocess_retroactive:
                image = cv2.addWeighted(image, 1.2, image, 0, 0)
                image = ImageUtils.adjust_color(image)

                # cv2.imwrite(image_path, image)
        except:
            classification_id = ClassificationErrorEnum.ERRO_92.value

        if reprocess_retroactive_days:




            if image is None:
                classification_id = ClassificationErrorEnum.ERRO_92.value

            # if error_code == ClassificationErrorEnum.ERRO_96.value:
            #     classification_id = ClassificationErrorEnum.ERRO_96.value

            if classification_id not in (ClassificationErrorEnum.ERRO_92.value, ClassificationErrorEnum.ERRO_96.value):

                amount_of_zeros = ImageUtils.get_amount_of_zeros_in_image(original_image)

                if amount_of_zeros > 0.80 :
                    classification_id = ClassificationErrorEnum.ERRO_91.value

                else:


                    carcass_classification_result = ClassifierUtils.predict(carcass_classification_classifier, image, image_classification=True)

                    carcass_classification_id = carcass_classification_result['label']

                    carcass_classification_label = CarcassClassificationEnum.get_value(carcass_classification_id)
                    carcass_classification_score = CarcassClassificationEnum.get_value(carcass_classification_id)



                    skeleton_detection_confidence_threshold = ConfigurationStorageController.get_config_data_value(
                        ConfigurationEnum.SKELETON_DETECTION_CONFIDENCE_THRESHOLD.name)

                    skeleton_detection_result, intersection_score = ClassifierUtils.predict(skeleton_detector, image, get_intersection_score=True, threshold=skeleton_detection_confidence_threshold)



                    if carcass_classification_result is None:
                        classification_id = ClassificationErrorEnum.ERRO_93.value

                    elif carcass_classification_label == CarcassClassificationEnum.WITHOUT_CARCASS.value:
                        classification_id = ClassificationErrorEnum.ERRO_93.value

                    else:

                        intersection_threshold =ConfigurationStorageController.get_config_data_value(
                            ConfigurationEnum.SKELETON_CLASSIFICATION_INTERSECTION_THRESHOLD.name)


                        if intersection_score < intersection_threshold:
                            classification_id = ClassificationErrorEnum.ERRO_94.value

                        else:


                            filter_detection_result = ClassifierUtils.predict(filter_detector, image)

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


        if image is not None and classification_id is None:
            

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

        return image, classification_id, filter_label, filter_confidence, side_detection_result

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

