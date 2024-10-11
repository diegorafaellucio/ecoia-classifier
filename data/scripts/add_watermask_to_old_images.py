import os
import cv2
import tqdm
import imutils
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import cv2


def insert_watermark_in_image(img, watermarker, alpha=1, beta=0.8):
    h_img, w_img, _ = img.shape

    logo = cv2.resize(watermarker, (w_img, h_img))
    result = cv2.addWeighted(img, alpha, logo, beta, 0)
    return result


def create_watermark_based_on_image_size(image, watermark_path=None):
    logo_path = watermark_path

    h_target, w_target, _ = image.shape

    logo = cv2.imread(logo_path)

    h_logo, w_logo, _ = logo.shape

    qt_cols = int(w_target / w_logo)
    qt_rows = int(h_target / h_logo)
    logo_copy = logo.copy()
    logo_copy_2 = logo.copy()
    rows = []
    for row in range(0, qt_rows):
        for col in range(0, qt_cols):
            logo_copy_2 = np.hstack([logo_copy_2, logo_copy])
        # mask = np.vstack([logo_copy_2,logo_copy_2])
        rows.append(logo_copy_2)
        logo_copy_2 = logo_copy
    mask_for_watermarker = np.vstack(rows)
    return mask_for_watermarker


def get_image_with_watermarker(image, watermark_path=None):
    watermarker = create_watermark_based_on_image_size(image, watermark_path)
    image_with_watermark = insert_watermark_in_image(image, watermarker)

    return image_with_watermark

images_path = '/home/ecotrace/fotos/2911'

black_list_day_path = ['/home/ecotrace/fotos/2911/2024/04/22']

years = sorted(os.listdir(images_path), reverse=True)


def generate_image(image_path):
    image = cv2.imread(image_path)

    image_with_watermark = get_image_with_watermarker(image,
                                                      watermark_path='../images/watermark_logo.png')

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


