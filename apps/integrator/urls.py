import logging
from django.urls import path
from apps.integrator.views.integrate_view import IntegrateView

logger = logging.getLogger(__name__)


urlpatterns = [
    path("integrator", IntegrateView.as_view()),
]
