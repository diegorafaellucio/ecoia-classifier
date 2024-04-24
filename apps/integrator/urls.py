import logging
from django.urls import path
from src.classifier.detector_loader import DetectorLoader
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum
from apps.classifier.views import ClassifierView
from src.shape_predictor.shape_predictor import ShapePredictor

logger = logging.getLogger(__name__)




urlpatterns = [
    path("classifier", ClassifierView.as_view(), {'classifier_suite': classifier_suite}),
]
