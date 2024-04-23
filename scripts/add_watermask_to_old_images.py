import os
import cv2
import tqdm

from src.utils.watermark_utils import WatermarkUtils
import imutils

import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

images_path = '/home/ecotrace/fotos/2911'

black_list_day_path = ['/home/ecotrace/fotos/2911/2024/04/22']

years = sorted(os.listdir(images_path), reverse=True)


def generate_image(image_path):
    image = cv2.imread(image_path)

    image_with_watermark = WatermarkUtils.get_image_with_watermarker(image,
                                                                     watermark_path='../data/images/watermark_logo.png')

    resized_image_with_watermark = imutils.resize(image_with_watermark, height=500)

    cv2.imwrite(image_path, resized_image_with_watermark)

    return True

executor = ThreadPoolExecutor(max_workers=1)

for year in years:

    year_path = os.path.join(images_path, year)

    months = sorted(os.listdir(year_path), reverse=True)

    for month in months:
        month_path = os.path.join(year_path, month)

        days = sorted(os.listdir(month_path), reverse=True)

        for day in days:

            day_path = os.path.join(month_path, day)

            if day_path not in black_list_day_path:

                images = sorted(os.listdir(day_path), reverse=True)

                futures = []

                for image in tqdm.tqdm(images):

                    image_path = os.path.join(month_path + '/' + day, image)

                    futures.append(executor.submit(generate_image, image_path))

                processed_counter = 0

                for future in concurrent.futures.as_completed(futures):
                    processed_counter += 1
                    print(day_path + ': {}/{}'.format(processed_counter, len(images)))


