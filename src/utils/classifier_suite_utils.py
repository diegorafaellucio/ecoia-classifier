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

class ClassifierSuiteUtils:


    @staticmethod
    def unpack(classifier_suite):

        carcass_classification_classifier = classifier_suite['carcass_classifier']
        skeleton_detector = classifier_suite['skeleton_detector']
        filter_detector = classifier_suite['filter_detector']
        side_detector = classifier_suite['side_detector']
        meat_detector = classifier_suite['meat_detector']
        bruise_detector = classifier_suite['bruise_detector']
        stamp_detector = classifier_suite['stamp_detector']
        side_a_shape_predictor = classifier_suite['side_a_shape_predictor']
        side_b_shape_predictor = classifier_suite['side_b_shape_predictor']
        grease_color_detector = classifier_suite['grease_color_detector']
        conformation_detector = classifier_suite['conformation_detector']
        hump_detector = classifier_suite['hump_detector']
        breed_detector = classifier_suite['breed_detector']
        cuts_classification_models = classifier_suite['cuts_classification_models']

        return carcass_classification_classifier, skeleton_detector, filter_detector, side_detector, meat_detector, bruise_detector, stamp_detector, \
               side_a_shape_predictor, side_b_shape_predictor, grease_color_detector, conformation_detector, hump_detector, breed_detector, cuts_classification_models