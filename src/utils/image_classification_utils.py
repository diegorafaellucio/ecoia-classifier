from shapely import Polygon
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum


class ImageClassificationUtils:

    @staticmethod
    def get_best_result(results):

        best_result = None
        max_confidence_score = 0

        if results is not None:
            for result in results:
                confidence = result['confidence']

                if confidence > max_confidence_score:
                    max_confidence_score = confidence

                    best_result = result

        return best_result
