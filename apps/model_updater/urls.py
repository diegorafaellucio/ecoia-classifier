import logging
from django.urls import path
from apps.model_updater.views.model_updater_view import UpdateModelsView

logger = logging.getLogger(__name__)


urlpatterns = [
    path("update", UpdateModelsView.as_view()),
]
