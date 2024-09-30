from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from src.enum.classifier_api_return_messages_enum import ClassifierApiReturnMessagesEnum
from src.enum.job_name_enum import JobNameEnum
from src.job.integrator_job import IntegratorJob
import warnings
from src.utils.job_thread_utils import JobThreadUtils
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Create your views here.
class JobStatusView(GenericAPIView):


    # 2. Create
    def get(self, request, *args, **kwargs):

        integrator_job_thread = kwargs['meat_classifier_job_thread']

        integrator_job_thread, message = JobThreadUtils.resurrect_thread(integrator_job_thread, JobNameEnum, IntegratorJob.do)

        return Response({"status": "success", "message": message}, status=status.HTTP_200_OK)
