import logging
from django.urls import path
from apps.integrator.views.integrate_view import IntegrateView
from apps.integrator.views.job_status_view import JobStatusView
from src.job.integrator_job import IntegratorJob
from src.enum.job_name_enum import JobNameEnum
import threading

logger = logging.getLogger(__name__)


integrator_job_thread = threading.Thread(target=IntegratorJob.do, name=JobNameEnum.INTEGRATOR.value)
integrator_job_thread.start()


urlpatterns = [
    path("integrate", IntegrateView.as_view()),
    path("job_status", JobStatusView.as_view(), {JobNameEnum.INTEGRATOR.value: integrator_job_thread}),
]
