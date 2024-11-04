from shapely import Polygon
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum


class DetectorUtils:

    @staticmethod
    def get_best_result(results, height=0, width=0):

        best_detection = None
        max_confidence_score = 0
        max_intersection_score = 0

        if results is not None:
            for result in results:

                bottom_right = result['bottomright']
                top_left = result['topleft']

                x_min = top_left['x']
                x_max = bottom_right['x']

                y_min = top_left['y']
                y_max = bottom_right['y']

                confidence = result['confidence']

                intersection_score = ObjectDetectionUtils.get_intersection_score(height, width, (x_min, y_min, x_max, y_max))

                detection_width = x_max - x_min
                detection_height = y_max - y_min

                if not (detection_width > 0) or not (detection_height > 0):
                    pass

                if intersection_score > max_intersection_score and confidence > max_confidence_score:
                    max_confidence_score = confidence

                    best_detection = result
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




    @staticmethod
    def coord_is_inside_detection_area(coord, detection):

        x_point, y_point = coord

        bottom_right = detection['bottomright']
        top_left = detection['topleft']

        x_min = top_left['x']
        x_max = bottom_right['x']

        y_min = top_left['y']
        y_max = bottom_right['y']

        if x_min <= x_point <= x_max and y_min <= y_point <= y_max:
            return True
        else:
            return False

