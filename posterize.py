import numpy as np
try:
    from cv2 import cv2
except:
    import cv2

def get_posterized_edges(im, bounds):




def posterize(im, bounds):




if __name__ == "__main__":

    input_img = cv2.imread(filename)

    gray = cv2.cvtColor(input_img,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (blur_radius, blur_radius), 0)
    edges = get_posterized_edges()