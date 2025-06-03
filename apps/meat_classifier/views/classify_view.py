from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from src.enum.classifier_api_return_messages_enum import ClassifierApiReturnMessagesEnum
from src.handler.meat_classifier_handler import MeatClassifierHandler
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import traceback
import threading

# Create your views here.
class ClassifyView(GenericAPIView):


    # 2. Create
    def post(self, request, *args, **kwargs):

        classifier_suite = kwargs['classifier_suite']

        try:

            MeatClassifierHandler.process_images(classifier_suite)

            return Response({"status": "success", "message": ClassifierApiReturnMessagesEnum.SUCCESS.value}, status=status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response({"status": "fail", "message": ClassifierApiReturnMessagesEnum.FAILURE.value + " \n " + traceback.format_exc() }, status=status.HTTP_400_BAD_REQUEST)