import requests
import time
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.controller.image_controller import ImageController
from src.enum.configuration_enum import ConfigurationEnum


def classification_processor_job():

    image_classifier_endpoint = "http://127.0.0.1:8000/classifier/job-status"

    payload = {}
    headers = {}

    response = requests.request("POST", image_classifier_endpoint, headers=headers, data=payload)

    print(response.text)


def integrator_processor_job():

    url = "http://127.0.0.1:8000/integrator/job-status"

    payload = {}
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)



