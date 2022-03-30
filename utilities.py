try:           
    from cv2 import cv2
except Exception:
    import cv2
import numpy as np

max_x = 600
max_y = 300


def resize(img, x = 800, y = 800):
    return cv2.resize(img, (x,y), interpolation = cv2.INTER_AREA)


def auto_resize(img):
    if (img.shape[0] / img.shape[1]) > (max_y / max_x):
        return resize(img, max_y * img.shape[1] / img.shape[0], max_y)
    else:
        return resize(img, max_x, max_x * img.shape[0] / img.shape[1])
    return("forbidden poop")


def get_blank_image(rows,cols,color = False):
    if color:
        return np.zeros((rows, cols, 3), np.uint8)
    else:
        return np.zeros((rows, cols, 1), np.uint8)

def copy_blank(image):
    im = image.copy()
    im.fill(0)
    return im