from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from src.enum.classifier_api_return_messages_enum import ClassifierApiReturnMessagesEnum
from src.handler.use_model_handler import UseModelHandler
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import traceback
import cv2
import numpy as np
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import uuid

# Create your views here.
class UseModelView(GenericAPIView):


    # 2. Create
    def post(self, request, *args, **kwargs):

        classifier_suite = kwargs['classifier_suite']

        try:
            # Get the image from form data
            if 'image' not in request.FILES:
                return Response({"status": "fail", "message": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Get the model name from form data
            if 'model_name' not in request.data:
                return Response({"status": "fail", "message": "No model name provided"}, status=status.HTTP_400_BAD_REQUEST)
            
            model_name = request.data['model_name']
            image_file = request.FILES['image']
            
            # Save the uploaded image temporarily
            temp_path = f"temp_{uuid.uuid4()}.jpg"
            path = default_storage.save(temp_path, ContentFile(image_file.read()))
            temp_file_path = default_storage.path(path)
            
            # Read the image with OpenCV
            image = cv2.imread(temp_file_path)
            
            if image is None:
                # Clean up the temporary file
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
                return Response({"status": "fail", "message": "Invalid image format"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Process the image with the specified model
            result = UseModelHandler.predict(image, model_name, classifier_suite)
            
            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            
            return Response({"status": "success", "message": ClassifierApiReturnMessagesEnum.SUCCESS.value, "result": result}, status=status.HTTP_200_OK)
        except Exception as e:
            # Clean up any temporary files if they exist
            if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            
            traceback.print_exc()
            return Response({"status": "fail", "message": ClassifierApiReturnMessagesEnum.FAILURE.value + " \n " + traceback.format_exc() }, status=status.HTTP_400_BAD_REQUEST)