from shapely import Polygon
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum


class DetectorUtils:

    @staticmethod
    def get_best_detection(detections, height, width):

        best_detection = None
        max_condidence_score = 0
        max_intersection_score = 0

        for detection in detections:

            bottom_right = detection['bottomright']
            top_left = detection['topleft']

            x_min = top_left['x']
            x_max = bottom_right['x']

            y_min = top_left['y']
            y_max = bottom_right['y']

            confidence = detection['confidence']

            intersection_score = DetectorUtils.get_intersection_score(height, width, (x_min, y_min, x_max, y_max))

            width = x_max - x_min
            height = y_max - y_min

            if not (width > 0) or not (height > 0):
                pass


            if intersection_score > max_intersection_score and confidence > max_condidence_score:
                max_condidence_score = confidence

                best_detection = detection
                max_intersection_score = intersection_score

        return best_detection

    @staticmethod
    def get_intersection_score(height, width, detection_coords):

        x_min, y_min, x_max, y_max = detection_coords

        padding = ConfigurationStorageController.get_config_data_value(ConfigurationEnum.DETECTION_PADDING.name)

        gt_x_min = padding
        gt_y_min = 0
        gt_x_max = width - padding
        gt_y_max = height

        gt_polygon = Polygon(
            [(gt_x_min, gt_y_min), (gt_x_min, gt_y_max), (gt_x_max, gt_y_max), (gt_x_max, gt_y_min)])

        detection_polygon = Polygon(
            [(x_min, y_min), (x_min, y_max),
             (x_max, y_max),
             (x_max, y_min)])

        intersection = gt_polygon.intersection(detection_polygon)

        intersection_score = intersection.area / gt_polygon.area

        return intersection_score
