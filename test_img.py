import cv2
import numpy as np

black_color_lab = np.array([0, 128, 128], dtype=np.uint8)
white_color_lab = np.array([205, 128, 128], dtype=np.uint8)

def adjust_color(img):
    img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
    black_luminance = img_lab[..., 0].min()
    white_luminance = img_lab[..., 0].max()

    targetBlackLuminance = black_color_lab[0]
    targetWhiteLuminance = white_color_lab[0]

    img_lab[..., 0] = np.interp(img_lab[..., 0], (black_luminance, white_luminance),
                               (targetBlackLuminance, targetWhiteLuminance))

    imgAdjusted = cv2.cvtColor(img_lab, cv2.COLOR_Lab2BGR)

    return imgAdjusted


image_path = '/home/diego-rafael-lucio/Downloads/20241216-0001-2-0110-0889.jpg'

image = cv2.imread(image_path)

image = cv2.addWeighted(image, 1.2, image, 0, 0)
image = adjust_color(image)


cv2.imwrite('/home/diego-rafael-lucio/Downloads/new_20241216-0001-2-0110-0889.jpg', image)