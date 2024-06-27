import logging
import dlib
import cv2
import numpy as np

from src.enum.cuts_enum import CutsEnum
from src.controller.cut_controller import CutController
class CutsUtils:
    logger = logging.getLogger(__name__)


    @staticmethod
    def get_cuts(image, side_detection_result, side_a_shape_predictor, side_b_shape_predictor):

        side_detection_label = side_detection_result['label']

        cuts_coords = {}

        x_min = side_detection_result['topleft']['x']
        y_min = side_detection_result['topleft']['y']
        x_max = side_detection_result['bottomright']['x']
        y_max = side_detection_result['bottomright']['y']

        roi = image[y_min:y_max, x_min:x_max]

        rect = dlib.rectangle(left=0, top=0, right=roi.shape[1], bottom=roi.shape[0])

        if 'LADO_A' in side_detection_label:
            cuts_coords = side_a_shape_predictor.get_polygons(
                roi, rect, x_min, y_min)
        elif 'LADO_B' in side_detection_label:
            cuts_coords = side_b_shape_predictor.get_polygons(
                roi, rect, x_min, y_min)

        return cuts_coords

    @staticmethod
    def get_cuts_mask_and_cut_lines_image(cuts_coords, image):

        cut_lines_image = image.copy()
        cuts_mask = np.zeros(image.shape[:2], dtype=np.uint8)

        for cut_coord_key, cut_coord_data in cuts_coords.items():
            coords_polygon = cut_coord_data.reshape((-1, 1, 2))
            cv2.polylines(cut_lines_image, [coords_polygon], True, (255, 0, 255), 5)
            color = CutsEnum[cut_coord_key.upper()].value
            cv2.fillPoly(cuts_mask, pts=[coords_polygon], color=(color, color, color))

        _, binary_mask = cv2.threshold(cuts_mask, 0, 255, cv2.THRESH_BINARY)

        return cut_lines_image, cuts_mask, binary_mask

    @staticmethod
    def save_cuts_data(image_id, cuts_coords):
        for cut_coord_key, cut_coord_data in cuts_coords.items():
            CutController.insert_into_cut(CutsEnum[cut_coord_key.upper()].value, image_id, cut_coord_data)


