#!/usr/bin/env python

import numpy as np
import dlib
from src.enum.cuts_coords_enum import CutsCoords


class ShapePredictor:

    def __init__(self, shape_predictor_weights):

        self.model_predictor = dlib.shape_predictor(shape_predictor_weights)

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

        for cut_coords in CutsCoords:
            cut_key = cut_coords.name
            cut_points = cut_coords.value
            coords = []
            for cut_point in cut_points:
                coords.append(points[cut_point])

            coords = np.asarray(coords, np.int32)

            all_coords[cut_key] = coords

        return all_coords
