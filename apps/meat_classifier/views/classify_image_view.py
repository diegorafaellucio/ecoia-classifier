from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from src.enum.classifier_api_return_messages_enum import ClassifierApiReturnMessagesEnum
from src.handler.meat_classifier_handler import MeatClassifierHandler
from src.utils.classifier_utils import ClassifierUtils
from src.enum.meat_enum import MeatEnum
from src.enum.classification_error_enum import ClassificationErrorEnum
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import traceback
import threading
import cv2
import numpy as np
import io

# Create your views here.
class ClassifyImageView(GenericAPIView):


    # 2. Create
    def post(self, request, *args, **kwargs):

        classifier_suite_dict = kwargs['classifier_suite']

        try:
            # Extract the image path from the form data
            if 'image_path' not in request.data:
                return Response({"status": "fail", "message": "The 'image_path' field is required"}, status=status.HTTP_400_BAD_REQUEST)

            image_path = request.data['image_path']

            # Extract the required models from classifier_suite_dict
            side_detector = classifier_suite_dict['side']
            meat_detector = classifier_suite_dict['meat']
            skeleton_detector = classifier_suite_dict['skeleton']
            filter_detector = classifier_suite_dict['filter']
            carcass_classification_classifier = classifier_suite_dict['carcass']

            # Get the reprocess_retroactive_days configuration parameter
            reprocess_retroactive_days = ConfigurationStorageController.get_config_data_value(
                ConfigurationEnum.REPROCESS_RETROACTIVE_DAYS.name)

            # Call the get_classification_id method with the appropriate parameters
            image, classification_id, classification_confidence, filter_label, filter_confidence, side_detection_result = ClassifierUtils.get_classification_id(
                image_path,
                side_detector,
                meat_detector, 
                skeleton_detector, 
                filter_detector, 
                reprocess_retroactive_days, 
                carcass_classification_classifier
            )

            # Get the classification name from the classification_id
            classification_name = None
            # Check if classification_id is not an error code
            error_codes = [error.value for error in ClassificationErrorEnum]
            if classification_id not in error_codes:
                # Try to find the enum value with matching database_id
                for meat_enum in MeatEnum:
                    if meat_enum.value['database_id'] == classification_id:
                        classification_name = meat_enum.name
                        break

            # Create the response with the classification results
            result = {
                "classification_id": classification_id,
                "classification_name": classification_name,
                "classification_confidence": classification_confidence,
                "filter_label": filter_label,
                "filter_confidence": filter_confidence,
                "side_detection_result": side_detection_result
            }

            return Response({"status": "success", "message": ClassifierApiReturnMessagesEnum.SUCCESS.value, "result": result}, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response({"status": "fail", "message": ClassifierApiReturnMessagesEnum.FAILURE.value + " \n " + traceback.format_exc() }, status=status.HTTP_400_BAD_REQUEST)
