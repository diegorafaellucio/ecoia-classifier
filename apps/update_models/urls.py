import logging
from django.urls import path
from apps.update_models.views import UpdateModelsView

logger = logging.getLogger(__name__)


urlpatterns = [
    path("update-models", UpdateModelsView.as_view()),
]
