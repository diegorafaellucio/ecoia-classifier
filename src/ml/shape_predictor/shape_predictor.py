#!/usr/bin/env python

import numpy as np
import dlib
from django.conf import settings
import os
from src.enum.cuts_enum import CutsEnum


class ShapePredictor:

    def __init__(self, model_path):

        base_dir = settings.BASE_DIR
        model_path = os.path.join(base_dir, model_path)
        self.model_predictor = dlib.shape_predictor(model_path)

    def get_polygons(self, image, rect, padding_left=0, padding_top=0):

        points = []

        landmarks = self.model_predictor(image, rect)

        for counter, part in enumerate(landmarks.parts()):
            # cv2.putText(image, '{}'.format(counter), (padding_left + part.x, padding_top + part.y),
            #             cv2.FONT_HERSHEY_SIMPLEX, 2,
            #             (0, 0, 255), 2, cv2.LINE_AA)

            points.append((part.x + padding_left, part.y + padding_top))

        # cv2.imshow('image', image)
        # cv2.waitKey(0)
        all_coords = {}
        for item_key, item in CutsEnum.__members__.items():
            cut_key = item.name
            cut_points = item.coords
            temp = item.value
            coords = []
            for cut_point in cut_points:
                coords.append(points[cut_point])

            coords = np.asarray(coords, np.int32)

            all_coords[cut_key] = coords

        return all_coords
