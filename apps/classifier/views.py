from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from src.enum.classifier_api_return_messages_enum import ClassifierApiReturnMessagesEnum
from src.handler.main_handler import MainHandler

# Create your views here.
class ClassifierView(GenericAPIView):

    # 2. Create
    def post(self, request, *args, **kwargs):

        classifier_suite = kwargs['classifier_suite']

        MainHandler.process_images(classifier_suite)

        try:

            return Response({"status": "success", "message": ClassifierApiReturnMessagesEnum.SUCCESS.value}, status=status.HTTP_200_OK)
        except:
            return Response({"status": "fail", "message": ClassifierApiReturnMessagesEnum.FAILURE.value}, status=status.HTTP_400_BAD_REQUEST)