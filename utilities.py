try:
    from cv2 import cv2
except:
    import cv2
import numpy as np

def get_blank_image(rows,cols,color = False):
    if color:
        return np.zeros((rows, cols, 3), np.uint8)
    else:
        y = np.zeros((rows, cols, 1), np.uint8)