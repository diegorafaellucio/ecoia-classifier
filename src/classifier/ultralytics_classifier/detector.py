import os
import shutil
import sys
from pathlib import Path
import numpy as np
import csv
import cv2
import torch
import tqdm
from ultralytics import YOLO


class Detector():

    def __init__(self, weights_path):
        self.model = YOLO(weights_path)


    def detect(self, image):

        # print('detectando lesoes na imagem', image.shape)

        pred = self.model.predict(image, verbose=False)

        boxes = pred[0].boxes.xyxy.tolist()
        class_ids = pred[0].boxes.cls.tolist()
        class_names = pred[0].names
        confidences = pred[0].boxes.conf.tolist()

        results = []

        if len(boxes):

            for i, boxe in enumerate(boxes):


                result = {}

                class_id = int(class_ids[i])  # integer class
                confidence = confidences[i]  # integer class
                detection_label = class_names[class_id]
                # print(class_id, label, p1, p2)

                result['label'] = detection_label
                result['confidence'] = confidence

                top_left_coords = {}
                top_left_coords['x'] = int(boxe[0])
                top_left_coords['y'] = int(boxe[1])

                result['topleft'] = top_left_coords

                bottom_right_coords = {}
                bottom_right_coords['x'] = int(boxe[2])
                bottom_right_coords['y'] = int(boxe[3])

                result['bottomright'] = bottom_right_coords

                results.append(result)

            return results
