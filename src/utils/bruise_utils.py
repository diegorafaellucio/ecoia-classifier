import cv2
import logging
from shapely import Polygon
from src.utils.detector_utils import DetectorUtils
from src.enum.bruises_enum import BruisesEnum
from PIL import ImageColor
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.controller.bruise_controller import BruiseController
from src.enum.configuration_enum import ConfigurationEnum

class BruiseUtils:
    logger = logging.getLogger(__name__)


    @staticmethod
    def sanitize_bruises(bruises, stamps):

        if bruises is not None:
            bruises = BruiseUtils.remove_intersections_with_another_bruises(bruises)
        if bruises is not None and stamps is not None:
            bruises = BruiseUtils.remove_intersections_with_stamps(bruises, stamps)

        return bruises

    @staticmethod
    def get_intersection_score(gt_coords, side_coords):
        gt_x_min, gt_y_min, gt_x_max, gt_y_max = gt_coords

        padding_polygon = Polygon(
            [(gt_x_min, gt_y_min), (gt_x_min, gt_y_max), (gt_x_max, gt_y_max), (gt_x_max, gt_y_min)])

        side_x_min, side_y_min, side_x_max, side_y_max = side_coords

        side_polygon = Polygon(
            [(side_x_min, side_y_min), (side_x_min, side_y_max), (side_x_max, side_y_max),
             (side_x_max, side_y_min)])

        intersection = padding_polygon.intersection(side_polygon)

        if intersection.area == 0:
            intersection_score = 0
        else:
            intersection_score = intersection.area / padding_polygon.area

        return intersection_score

    @staticmethod
    def remove_intersections_with_another_bruises(detections):
        black_list = []
        for first_counter, first_detection in enumerate(detections):
            for second_counter, second_detection in enumerate(detections):
                if (first_counter != second_counter):
                    first_detection_x_min = first_detection['topleft']['x']
                    first_detection_y_min = first_detection['topleft']['y']
                    first_detection_x_max = first_detection['bottomright']['x']
                    first_detection_y_max = first_detection['bottomright']['y']
                    first_detection_condidence = first_detection['confidence']

                    gt_coords = [first_detection_x_min, first_detection_y_min, first_detection_x_max,
                                 first_detection_y_max]

                    second_detection_x_min = second_detection['topleft']['x']
                    second_detection_y_min = second_detection['topleft']['y']
                    second_detection_x_max = second_detection['bottomright']['x']
                    second_detection_y_max = second_detection['bottomright']['y']
                    second_detection_condidence = second_detection['confidence']

                    detection_coords = [second_detection_x_min, second_detection_y_min, second_detection_x_max,
                                        second_detection_y_max]

                    intersection_score = BruiseUtils.get_intersection_score(gt_coords, detection_coords)

                    if intersection_score > 0.80:
                        if first_detection_condidence > second_detection_condidence:
                            if second_counter not in black_list:
                                black_list.append(second_counter)
                        else:
                            if first_counter not in black_list:
                                black_list.append(first_counter)

        black_list = sorted(black_list, reverse=True)

        for index_to_remove in black_list:
            del detections[index_to_remove]

        return detections

    @staticmethod
    def remove_intersections_with_stamps(bruise_detections, stamp_detections):
        black_list = []
        for first_counter, first_detection in enumerate(bruise_detections):
            for second_counter, second_detection in enumerate(stamp_detections):
                first_detection_x_min = first_detection['topleft']['x']
                first_detection_y_min = first_detection['topleft']['y']
                first_detection_x_max = first_detection['bottomright']['x']
                first_detection_y_max = first_detection['bottomright']['y']

                gt_coords = [first_detection_x_min, first_detection_y_min, first_detection_x_max, first_detection_y_max]

                second_detection_x_min = second_detection['topleft']['x']
                second_detection_y_min = second_detection['topleft']['y']
                second_detection_x_max = second_detection['bottomright']['x']
                second_detection_y_max = second_detection['bottomright']['y']

                detection_coords = [second_detection_x_min, second_detection_y_min, second_detection_x_max,
                                    second_detection_y_max]

                intersection_score = BruiseUtils.get_intersection_score(gt_coords, detection_coords)

                if intersection_score > 0.50:
                    black_list.append(first_counter)

        black_list = sorted(black_list, reverse=True)

        for index_to_remove in black_list:
            try:
                del bruise_detections[index_to_remove]
            except:
                pass

        return bruise_detections

    @staticmethod
    def draw_bruises_on_cut_lines_image(cut_lines_image, side_detection_result, bruises):

        bruise_confidence_threshold = ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.BRUISE_CONFIDENCE_THRESHOLD.name)

        bruise_plot_radius = ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.BRUISE_PLOT_RADIUS.name)

        if bruises is not None:

            for bruise in bruises:
                data_lesion = bruise['label']
                data_lesion_items = data_lesion.split('-')

                bruise_label = data_lesion_items[-1]

                bruise_confidence = bruise['confidence']
                bruise_x_min = bruise['topleft']['x']
                bruise_y_min = bruise['topleft']['y']

                bruise_x_max = bruise['bottomright']['x']
                bruise_y_max = bruise['bottomright']['y']

                mid_x_coord = int(bruise_x_min + ((bruise_x_max - bruise_x_min)/2))
                mid_y_coord = int(bruise_y_min + ((bruise_y_max - bruise_y_min)/2))

                midpoint_is_inside_detection = DetectorUtils.coord_is_inside_detection_area([mid_x_coord, mid_y_coord], side_detection_result)



                if midpoint_is_inside_detection:

                    if bruise_confidence > bruise_confidence_threshold:

                        bruise_radius = 0
                        bruise_width = bruise_x_max - bruise_x_min
                        bruise_height = bruise_y_max - bruise_y_min

                        if bruise_width > bruise_height:
                            bruise_radius = int(bruise_width * bruise_plot_radius)
                        else:
                            bruise_radius = int(bruise_height * bruise_plot_radius)

                        hex_bruise_color = BruiseController.get_color_by_bruise_id(BruisesEnum[bruise_label.upper()].value)
                        rgb_bruise_color = ImageColor.getrgb(hex_bruise_color)

                        cut_lines_image = cv2.circle(cut_lines_image, (mid_x_coord, mid_y_coord), bruise_radius
                                                  , rgb_bruise_color, 5)
        return cut_lines_image

    @staticmethod
    def save_bruises_data(cuts_mask, side_detection_result, bruises, image_id):

        bruise_confidence_threshold = ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.BRUISE_CONFIDENCE_THRESHOLD.name)

        if bruises is not None:
            for bruise in bruises:
                data_lesion = bruise['label']
                data_lesion_items = data_lesion.split('-')

                bruise_label = data_lesion_items[-1]

                bruise_confidence = bruise['confidence']
                bruise_x_min = bruise['topleft']['x']
                bruise_y_min = bruise['topleft']['y']

                bruise_x_max = bruise['bottomright']['x']
                bruise_y_max = bruise['bottomright']['y']

                mid_x_coord = int(bruise_x_min + ((bruise_x_max - bruise_x_min) / 2))
                mid_y_coord = int(bruise_y_min + ((bruise_y_max - bruise_y_min) / 2))

                midpoint_is_inside_detection = DetectorUtils.coord_is_inside_detection_area([mid_x_coord, mid_y_coord],
                                                                                            side_detection_result)

                if midpoint_is_inside_detection:

                    if bruise_confidence > bruise_confidence_threshold:
                        cut_id = cuts_mask[mid_y_coord][mid_x_coord]
                        bruise_id = BruisesEnum[bruise_label].value

                        BruiseController.insert_into_bruise(image_id, bruise_id, cut_id, [mid_x_coord, mid_y_coord])




