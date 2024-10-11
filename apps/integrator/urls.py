import logging
from django.urls import path
from apps.integrator.views import IntegratorView

logger = logging.getLogger(__name__)


urlpatterns = [
    path("integrator", IntegratorView.as_view()),
]
