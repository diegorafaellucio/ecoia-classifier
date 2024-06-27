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
    def get_boundaries(binary_mask):

        contours = SkeletonSizeUtils.get_objects(binary_mask)

        point_reference_min_width = [10000000, 10000000]
        point_reference_max_width = [0, 0]
        extreme_top = []
        extreme_bottom = []

        for cnt in contours:

            for point in cnt:

                if point[0][0] < point_reference_min_width[0]:
                    point_reference_min_width[0] = point[0][0]
                    # point_reference_min_width[1]=point[0][1]

                if point[0][0] > point_reference_max_width[0]:
                    point_reference_max_width[0] = point[0][0]
                    # point_reference_max_width[1]=point[0][1]

                if point[0][1] < point_reference_min_width[1]:
                    point_reference_min_width[1] = point[0][1]
                    extreme_bottom = point[0]
                if point[0][1] > point_reference_max_width[1]:
                    point_reference_max_width[1] = point[0][1]
                    extreme_top = point[0]

        return point_reference_min_width[0], point_reference_max_width[0], point_reference_min_width[1], \
        point_reference_max_width[1], extreme_bottom, extreme_top

    @staticmethod
    def get_width(img, start_point, end_point):
        start_point_measure = np.array([0, 0])
        end_point_measure = np.array([0, 0])

        flag = True
        for axes_x in range(start_point[0], end_point[0] + 1):
            if (not np.array_equal(img[start_point[1], axes_x], [0, 0, 0])) and (
            not np.sum(img[start_point[1], axes_x]) <= 50):

                if flag:
                    start_point_measure = [axes_x, start_point[1]]
                    flag = False
                elif np.array_equal(img[start_point[1], axes_x + 1], [0, 0, 0]) and not flag:
                    end_point_measure = [axes_x, end_point[1]]
                    break
                else:
                    end_point_measure = [axes_x, end_point[1]]

        # cv2.line(img,start_point_measure,end_point_measure,(0,255,0),5)

        width = sqrt(
            (end_point_measure[0] - start_point_measure[0]) ** 2 + (end_point_measure[1] - start_point_measure[1]) ** 2)
        return width

    @staticmethod
    def get_height(img,extreme_top, extreme_bottom):
        #cv2.line(img, extreme_top, extreme_bottom, (0,255,0),5)
        return sqrt((extreme_top[0]-extreme_bottom[0])**2 + (extreme_top[1]-extreme_bottom[1])**2)

    @staticmethod
    def get_size(binary_mask, cuts_coords):

        pixel_centimeter_ratio = ConfigurationStorageController.get_config_data_value(ConfigurationEnum.PIXEL_CENTIMETER_RATIO.name)

        left, right, bottom, top, extreme_top, extreme_bottom = SkeletonSizeUtils.get_boundaries(binary_mask)

        start_point, end_point = SkeletonSizeUtils.get_points(cuts_coords)

        width = SkeletonSizeUtils.get_width(binary_mask, start_point, end_point)
        height = SkeletonSizeUtils.get_height(binary_mask, extreme_top, extreme_bottom)

        width = round(width * pixel_centimeter_ratio, 2)
        height = round(height * pixel_centimeter_ratio, 2)

        size_descriptor = SkeletonSizeUtils.get_size_descriptor(width, height)

        return width, height, size_descriptor


