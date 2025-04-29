from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from src.enum.classifier_api_return_messages_enum import ClassifierApiReturnMessagesEnum
from src.handler.meat_classifier_handler import MeatClassifierHandler
from src.utils.classifier_utils import ClassifierUtils
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import traceback
import threading
import cv2
import numpy as np
import io

# Create your views here.
class EvaluateModelView(GenericAPIView):


    # 2. Create
    def post(self, request, *args, **kwargs):

        classifier_suite_dict = kwargs['classifier_suite']

        try:
            # Extract the image and model name from the form data
            if 'image' not in request.FILES or 'model' not in request.data:
                return Response({"status": "fail", "message": "Both 'image' and 'model' fields are required"}, status=status.HTTP_400_BAD_REQUEST)

            image_file = request.FILES['image']
            model_name = request.data['model']

            # Get the appropriate classifier from the classifier_suite_dict
            if model_name not in classifier_suite_dict:
                return Response({"status": "fail", "message": f"Model '{model_name}' not found"}, status=status.HTTP_400_BAD_REQUEST)

            model = classifier_suite_dict[model_name]

            # Convert the uploaded image to a cv2 image
            image_bytes = image_file.read()
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Call the predict function on the model with the image
            prediction_result = ClassifierUtils.predict(model, image)

            return Response({"status": "success", "message": ClassifierApiReturnMessagesEnum.SUCCESS.value, "result": prediction_result}, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response({"status": "fail", "message": ClassifierApiReturnMessagesEnum.FAILURE.value + " \n " + traceback.format_exc() }, status=status.HTTP_400_BAD_REQUEST)
