import cv2
import numpy as np
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum
from math import sqrt
from src.enum.size_enum import SizeEnum
class SkeletonSizeUtils:

    base_area = 6800

    @staticmethod
    def get_objects(binary_mask):
        mask = cv2.adaptiveThreshold(binary_mask, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 19, 5)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        objects = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 2000:
                objects.append(cnt)

        return objects

    @staticmethod
    def get_points(poly):

        cap_contra = poly['CAPA_CONTRA'][0]
        cost = [int((poly['COSTELA'][3][0] + poly['COSTELA'][3][0]) / 2),
                int((poly['COSTELA'][3][1] + poly['COSTELA'][3][1]) / 2)]

        if cost[0] < cap_contra[0]:
            start_region = cost
            end_region = cap_contra
            return start_region, end_region

        else:
            start_region = cap_contra
            end_region = cost
            return start_region, end_region

    @staticmethod
    def get_size_descriptor(width, height):

        size_descriptor = SizeEnum.P.value

        size_area = width * height

        if size_area <= SkeletonSizeUtils.base_area:
            size_descriptor = SizeEnum.P.value

        elif SkeletonSizeUtils.base_area < size_area <= SkeletonSizeUtils.base_area * 1.2:
            size_descriptor = SizeEnum.M.value

        elif SkeletonSizeUtils.base_area * 1.2 < size_area:
            size_descriptor = SizeEnum.G.value

        return size_descriptor


    @staticmethod
    def get_width(img, start_point, end_point):
        width = np.sqrt((end_point[0] - start_point[0]) ** 2 + (end_point[1] - start_point[1]) ** 2)
        return width



    @staticmethod
    def get_height(extreme_top, extreme_bottom):
        height = np.sqrt((top[0] - bottom[0]) ** 2 + (top[1] - bottom[1]) ** 2)
        return height

    @staticmethod
    def get_extremes_axes_y(binary_mask_carcass):
        contours, _ = cv2.findContours(binary_mask_carcass, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0]
        bottom = tuple(contours[contours[:, :, 1].argmin()][0])
        top = tuple(contours[contours[:, :, 1].argmax()][0])

        return bottom, top

    @staticmethod
    def get_roi(binary_mask_carcass, start_point, end_point):
        mask = np.zeros(binary_mask_carcass.shape, np.uint8)
        cv2.line(mask, start_point, end_point, color=255, thickness=2)
        _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        result = np.logical_and(binary_mask_carcass, mask)
        result = np.uint8(result)

        contours, _ = cv2.findContours(result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0]

        roi_start_point = tuple(contours[contours[:, :, 0].argmin()][0])
        roi_end_point = tuple(contours[contours[:, :, 0].argmax()][0])

        return roi_start_point, roi_end_point

    @staticmethod
    def get_size(binary_mask, cuts_coords):

        pixel_centimeter_ratio = ConfigurationStorageController.get_config_data_value(ConfigurationEnum.PIXEL_CENTIMETER_RATIO.name)

        bottom, top = SkeletonSizeUtils.get_extremes_axes_y(binary_mask)

        start_point, end_point = SkeletonSizeUtils.get_points(cuts_coord)
        roi_start_point, roi_end_point = SkeletonSizeUtils.get_roi(binary_mask, start_point, end_point)

        width = SkeletonSizeUtils.get_width(roi_start_point, roi_end_point)
        height = SkeletonSizeUtils.get_height(bottom, top)

        width = round(width * pixel_centimeter_ratio, 2)
        height = round(height * pixel_centimeter_ratio, 2)

        size_descriptor = SkeletonSizeUtils.get_size_descriptor(width, height)

        return width, height, size_descriptor


