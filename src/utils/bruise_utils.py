from itertools import count

import cv2
import logging
import numpy as np
from shapely import Polygon
from sympy.physics.units import percent

from src.utils.object_detection_utils import ObjectDetectionUtils
from src.enum.bruises_enum import BruisesEnum
from PIL import ImageColor
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.controller.bruise_controller import BruiseController
from src.controller.aux_bruise_controller import AuxBruiseController
from src.controller.aux_cut_controller import AuxCutController
from src.enum.configuration_enum import ConfigurationEnum
from src.enum.level_extension_lesion_enum import LevelExtensionLesionEnum
from src.enum.cuts_enum import CutsEnum
from src.utils.cuts_utils import CutsUtils

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

                    if intersection_score > 0.60:
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
    def draw_bruises_on_cut_lines_image(cut_lines_image, side_detection_result, bruises, cuts_mask, binary_mask):

        bruise_confidence_threshold = ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.BRUISE_CLASSIFICATION_CONFIDENCE_THRESHOLD.name)

        bruise_plot_radius = ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.BRUISE_CLASSIFICATION_PLOT_RADIUS.name)

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


                roi  = BruiseUtils.get_roi(binary_mask, bruise)

                if roi !=-1:
                    bruise_x_min = roi[0][0]
                    bruise_y_min = roi[0][1]
                    bruise_x_max = roi[1][0]
                    bruise_y_max = roi[1][1]

                mid_x_coord = int(bruise_x_min + ((bruise_x_max - bruise_x_min) / 2))
                mid_y_coord = int(bruise_y_min + ((bruise_y_max - bruise_y_min) / 2))

                midpoint_is_inside_detection = ObjectDetectionUtils.coord_is_inside_detection_area([mid_x_coord, mid_y_coord],
                                                                                                   side_detection_result)

                cut_id = cuts_mask[mid_y_coord][mid_x_coord]

                if cut_id != 0:

                    if midpoint_is_inside_detection:

                        if bruise_confidence > bruise_confidence_threshold:

                            bruise_radius = 0
                            bruise_width = bruise_x_max - bruise_x_min
                            bruise_height = bruise_y_max - bruise_y_min

                            if bruise_width > bruise_height:
                                bruise_radius = int(bruise_width * bruise_plot_radius)
                            else:
                                bruise_radius = int(bruise_height * bruise_plot_radius)

                            hex_bruise_color = BruiseController.get_color_by_bruise_id(
                                BruisesEnum[bruise_label.upper()].value)
                            rgb_bruise_color = ImageColor.getrgb(hex_bruise_color)
                            bgr_bruise_color = (rgb_bruise_color[2], rgb_bruise_color[1], rgb_bruise_color[0])

                            cut_lines_image = cv2.rectangle(cut_lines_image, (bruise_x_min, bruise_y_min), (bruise_x_max, bruise_y_max)
                                                         , bgr_bruise_color, 5)
        return cut_lines_image

    @staticmethod
    def get_id_intersection_scores_and_cuts_affected_by_bruises(cuts_coords, bruise, image_shape):

        id_cuts_affeted_by_bruise = []
        threshold_consider_cut_affeted_by_bruise= ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.MODULE_CONSIDER_CUT_AFFETED_BY_BRUISE.name)

        if bruise is not None:

            x_min = bruise['topleft']['x']
            y_min = bruise['topleft']['y']

            x_max = bruise['bottomright']['x']
            y_max = bruise['bottomright']['y']

            mask_bruise = BruiseUtils.get_bruise_mask([x_min, y_max], [x_max, y_min], image_shape)
            for cut_coord_key, cut_coord_data in cuts_coords.items():
                cut_mask = CutsUtils.get_cut_mask(image_shape,cut_coord_data)
                percent_intersection_cut_bruise = BruiseUtils.get_percentage_instersection(cut_mask, mask_bruise)
                if percent_intersection_cut_bruise >=  threshold_consider_cut_affeted_by_bruise:
                    id_cuts_affeted_by_bruise.append([CutsEnum[cut_coord_key.upper()].value, percent_intersection_cut_bruise])
        return id_cuts_affeted_by_bruise


    @staticmethod
    def get_position(bruise_height, reference_height):
        if bruise_height <= reference_height:
            return 'T'
        else:
            return 'D'

    @staticmethod
    def get_region_code_bruise(bruise, reference_height, count_rear_affeted, count_front_affeted):
        center_height = int((bruise['bottomright']['y'] + bruise['topleft']['y'])/2)
        code_region = BruiseUtils.get_position(center_height,reference_height)

        if code_region == 'T':
            count_rear_affeted+=1
            code_region_bruise = code_region+str(count_rear_affeted)
        else:
            count_front_affeted+=1
            code_region_bruise = code_region + str(count_front_affeted)

        return code_region_bruise, count_front_affeted, count_rear_affeted
    @staticmethod
    def save_bruises_data(cuts_mask, binary_mask,side_detection_result, bruises, image_id, cuts_coords, extension_lesion_is_enable=False):

        bruise_confidence_threshold = ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.BRUISE_CLASSIFICATION_CONFIDENCE_THRESHOLD.name)

        pixel_centimeter_ratio = ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.MODULE_SIZE_PREDICTION_PIXEL_CENTIMETER_RATIO.name)


        reference_height = int(binary_mask.shape[1]/2)

        if bruises is not None:
            count_rear_affeted = 0
            count_front_affeted = 0

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

                midpoint_is_inside_detection = ObjectDetectionUtils.coord_is_inside_detection_area([mid_x_coord, mid_y_coord],
                                                                                            side_detection_result)
                if extension_lesion_is_enable and data_lesion !='FALHA':
                    diameter_cm, width, height = BruiseUtils.calculate_extent_bruise(binary_mask, bruise, pixel_centimeter_ratio)
                    bruise_level_id = BruiseUtils.get_level_lesion_id(diameter_cm)

                intersection_scores_and_cuts_affected_by_bruises = BruiseUtils.get_id_intersection_scores_and_cuts_affected_by_bruises(cuts_coords, bruise, binary_mask.shape)

                region_code_bruise, count_front_affeted, count_rear_affeted = BruiseUtils.get_region_code_bruise(bruise,reference_height, count_rear_affeted, count_front_affeted)

                for intersection_scores_and_cuts_affected_by_bruise in intersection_scores_and_cuts_affected_by_bruises:

                    cut_id = intersection_scores_and_cuts_affected_by_bruise[0]
                    intersection_score = intersection_scores_and_cuts_affected_by_bruise[1]

                    if cut_id != 0:
                        if midpoint_is_inside_detection:
                            if bruise_confidence > bruise_confidence_threshold:
                                bruise_id = BruisesEnum[bruise_label].value
                                if extension_lesion_is_enable and data_lesion != 'FALHA':
                                    BruiseController.insert_into_bruise(image_id, bruise_id, cut_id,intersection_score, [mid_x_coord, mid_y_coord], region_code_bruise,width, height, diameter_cm, bruise_level_id)
                                else:
                                    BruiseController.insert_into_bruise(image_id, bruise_id, cut_id,intersection_score,
                                                                        [mid_x_coord, mid_y_coord], region_code_bruise)

    @staticmethod
    def get_bruise_integration_data_minerva(image_id):

        output_data = []

        bruises_in_image = BruiseController.get_only_greatest_intersection_bruises_by_image_id(image_id)

        for bruise_in_image in bruises_in_image:
            bruise_id = bruise_in_image[5]
            region_id = bruise_in_image[1]

            bruise_name = AuxBruiseController.get_name_by_id(bruise_id)
            region_name = AuxCutController.get_name_by_id(region_id)

            bruise_data = {
                "id_lesao": bruise_id,
                "id_regiao": region_id,
                "label_lesao": bruise_name.upper(),
                "label_regiao": region_name.upper()
            }

            output_data.append(bruise_data)


        return output_data
    @staticmethod
    def get_bruise_integration_data(image_id):

        output_data = []

        bruises_in_image = BruiseController.get_by_image_id(image_id)
        blacklist = []



        for bruise_in_image in bruises_in_image:
            bruise_id = bruise_in_image[5]

            region_bruise_code = bruise_in_image[-2]


            if region_bruise_code in blacklist:
                continue

            blacklist.append(region_bruise_code)
            region_name,region_id = BruiseUtils.get_region_affected(image_id, region_bruise_code)


            bruise_name = AuxBruiseController.get_name_by_id(bruise_id)
            #region_name = AuxCutController.get_name_by_id(region_id)

            bruise_data = {
                "id_lesao": bruise_id,
                "id_regiao": region_id,
                "label_lesao": bruise_name.upper(),
                "label_regiao": region_name
            }


            output_data.append(bruise_data)


        return output_data

    @staticmethod
    def get_roi(binary_mask, bruise):

        x_min = bruise['topleft']['x']
        y_min = bruise['topleft']['y']
        x_max = bruise['bottomright']['x']
        y_max = bruise['bottomright']['y']


        mask_bruise = BruiseUtils.get_bruise_mask([x_min, y_max], [x_max, y_min], binary_mask.shape)
        percentage_intersection = BruiseUtils.get_percentage_instersection(binary_mask, mask_bruise)

        roi = ([x_min, y_min], [x_max, y_max])

        if percentage_intersection == 0:
            roi = -1

        elif percentage_intersection < 0.80:
            mask_intersection = BruiseUtils.get_mask_intersection(binary_mask, mask_bruise)
            roi = BruiseUtils.get_region_of_intersection(mask_intersection)

        return roi

    @staticmethod
    def get_region_of_intersection(mask_intersection):

        _, binary_intersection = cv2.threshold(mask_intersection, 127, 255, cv2.THRESH_BINARY)
        contours_intersection, _ = cv2.findContours(mask_intersection, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        points = np.reshape(contours_intersection[0], (-1, 2))
        min = np.min(points, axis=0)
        max = np.max(points, axis=0)
        return (min, max)

    @staticmethod
    def get_mask_intersection(mask_carcass, mask_bruise):
        _, binary_mask_carcass = cv2.threshold(mask_carcass, 127, 255, cv2.THRESH_BINARY)
        _, binary_mask_bruise = cv2.threshold(mask_bruise, 127, 255, cv2.THRESH_BINARY)

        mask_intersection = np.logical_and(binary_mask_carcass, binary_mask_bruise)
        # mask_intersection*=255
        return np.uint8(mask_intersection)

    @staticmethod
    def get_percentage_instersection(mask_carcass, mask_bruise):

        _, binary_mask_carcass = cv2.threshold(mask_carcass, 127, 255, cv2.THRESH_BINARY)
        _, binary_mask_bruise = cv2.threshold(mask_bruise, 127, 255, cv2.THRESH_BINARY)
        area_intersection = np.sum(np.logical_and(binary_mask_carcass, binary_mask_bruise))
        area_bruise = np.sum(binary_mask_bruise / 255)

        percentage_intersection = area_intersection / area_bruise

        return percentage_intersection

    @staticmethod
    def get_bruise_mask(points_min, points_max, img_shape):
        mask_bruise = np.zeros(img_shape, np.uint8)
        mask_bruise = cv2.rectangle(mask_bruise, points_min, points_max, color=255, thickness=cv2.FILLED)

        return mask_bruise

    @staticmethod
    def calculate_extent_bruise(binary_mask,bruise, pixel_centimeter_ratio):

        width = 0
        height = 0
        diameter_cm = 0

        roi = BruiseUtils.get_roi(binary_mask, bruise)
        if roi == -1:
            return width, height, diameter_cm

        x_center = int((roi[0][0] + roi[1][0]) / 2)
        y_center = int((roi[0][1] + roi[1][1]) / 2)

        width = roi[1][0] - roi[0][0]
        height = roi[1][1] - roi[0][1]

        if width < 0:
            width = -1 * width

        if height < 0:
            height = -1 * height

        diameter = (width + height) / 2

        width = round(width * pixel_centimeter_ratio, 2)
        height = round(height * pixel_centimeter_ratio, 2)
        diameter_cm = round(diameter*pixel_centimeter_ratio,2)

        diameter_cm = BruiseUtils.adjust_value_extension_lesion(diameter_cm)
        height = BruiseUtils.adjust_value_extension_lesion(height)
        width = BruiseUtils.adjust_value_extension_lesion(width)


        return diameter_cm, width, height

    @staticmethod
    def adjust_value_extension_lesion(value_extension_lesion):
        decimal = value_extension_lesion - int(value_extension_lesion)
        if decimal >= 0.5:
            value_extension_lesion_adjusted = int(value_extension_lesion) + 1
        else:
            value_extension_lesion_adjusted  = int(value_extension_lesion)

        return value_extension_lesion_adjusted

    @staticmethod
    def get_level_lesion_id(value_extension_lesion):
        if value_extension_lesion <= 10:
            return LevelExtensionLesionEnum.NIVEL_I.value
        elif value_extension_lesion>=11 and value_extension_lesion <=20:
            return LevelExtensionLesionEnum.NIVEL_II.value
        else:
            return LevelExtensionLesionEnum.NIVEL_III.value

    @staticmethod
    def get_bruises_in_cuts(image_id):
        bruise_in_cuts = {}
        bruises_in_image = BruiseController.get_by_image_id(image_id)

        for bruise_in_image in bruises_in_image:
            bruise_id = bruise_in_image[5]
            region_id = bruise_in_image[1]
            region_name = AuxCutController.get_name_by_id(region_id)

            bruise_in_cuts[region_name.upper()] = bruise_in_cuts.setdefault(region_name.upper(),[]) + [bruise_id]

        return bruise_in_cuts

    @staticmethod
    def get_region_affected(image_id, region_bruise_code):
        region_affected_by_name = []
        region_affected_by_id = []
        bruises_in_image = BruiseController.get_cuts_affectd_by_image_id_and_region_code(image_id, region_bruise_code)

        for bruise_in_image in bruises_in_image:
            region_id = bruise_in_image[1]
            region_name = AuxCutController.get_name_by_id(region_id)
            region_affected_by_name.append(region_name.upper())
            region_affected_by_id.append(region_id)

        return region_affected_by_name, region_affected_by_id