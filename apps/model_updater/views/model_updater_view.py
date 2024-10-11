from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from src.enum.updatemodelsapireturnmessagesenum import UpdateModelsApiReturnMessagesEnum
from src.handler.model_updater_handler import ModelUpdaterHandler

# Create your views here.
class UpdateModelsView(GenericAPIView):

    # 2. Create
    def post(self, request, *args, **kwargs):


        ModelUpdaterHandler.update()

        try:

            return Response({"status": "success", "message": UpdateModelsApiReturnMessagesEnum.SUCCESS.value}, status=status.HTTP_200_OK)
        except:
            return Response({"status": "fail", "message": UpdateModelsApiReturnMessagesEnum.FAILURE.value}, status=status.HTTP_400_BAD_REQUEST)