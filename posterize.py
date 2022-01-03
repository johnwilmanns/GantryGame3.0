import numpy as np

import full_path_planning
import utilities
import face_full_processing
try:
    from cv2 import cv2 #'ery nice
except:
    import cv2

def get_posterized_edges(im, gaps = [5, 10, 15]):


    n = len(gaps) + 1 # Number of levels of quantization

    indices = np.arange(0, 256)  # List of all colors

    divider = np.linspace(0, 255, n + 1)[1]  # we get a divider

    quantiz = np.int0(np.linspace(0, 255, n))  # we get quantization colors

    color_levels = np.clip(np.int0(indices / divider), 0, n - 1)  # color levels 0,1,2..

    palette = quantiz[color_levels]  # Creating the palette

    poster = palette[im]  # Applying palette on image

    poster = cv2.convertScaleAbs(poster)  # Converting image back to uint8
    # cv2.imshow("poster", poster)
    edges = im.copy()
    edges.fill(0)

    values = [255, 170, 85, 0]
    values.reverse()
    lines = []
    for i, value in enumerate(gaps):
        im = utilities.copy_blank(im)
        y = 0

        while y < len(im[0]):
            # for y in range(len(im[1])):
            #      if (x % value == 0) & (y % value == 0):
            #          im[x, y] = 255
            # print(y)
            try:
                j = 0
                while True:
                    # print(f"setting {y}, {y+j}")
                    im[j,y + j] = 255

                    j+=1


            except IndexError:
                # print("pass")
                pass

            try:
                j = 0
                # print(j)
                while True:
                    # print(f"setting {y}, {y+j}")
                    im[j,y + j] = 255

                    j-=1
            except IndexError:
                pass
            y+= value
            # cv2.imshow("line", im)
            # cv2.waitKey(1)



        lines.append(im)

    for value in values:
        if value == 255:
            continue
        line = lines.pop(0)
        for x in range(len(poster)):
            for y in range(len(poster[1])):
                if poster[x][y] == value:
                    edges[x][y] = line[x][y]






    return edges

def get_segments(input_img):
    gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = get_posterized_edges(gray)
    dst = edges
    lines = []
    arraymax = max(len(gray),len(gray[1]))
    for x in range(len(edges)):
        for y in range(len(edges[0])):
            if edges[x][y] == 255:
                initpoint = [x,y]
                i = x
                k = y
                try:
                    while edges[i,k] == 255:
                        edges[i,k] = 10
                        i +=1
                        k +=1
                        # print(f"trying {i}, {k}")
                except IndexError:
                    pass
                # print(f"added {i}, {k}")
                if (abs(initpoint[0] - i) ** 2  + abs(initpoint[1] - k) ** 2) ** .5 >= 10:
                    lines.append([[initpoint[0]/arraymax, initpoint[1]/arraymax],[(i-1)/arraymax,(k-1)/arraymax]])


    return lines

def get_calcd_path(input_img, gaps = [5, 10, 15], max_accel, max_radius, turn_vel_multiplier, john = "dumb"):
    return full_path_planning.calc_path(get_segments(input_img, gaps = [5, 10, 15]), max_accel, max_lr, turn_vel_multiplier, freq)



if __name__ == "__main__":

    input_img = utilities.resize(cv2.imread("img.png"))

    gray = cv2.cvtColor(input_img,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = get_posterized_edges(gray)
    dst = edges

    # Copy edges to the images that will display the results in BGR
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)
    inverted = utilities.copy_blank(edges)
    for x in range(len(edges)):
        for y in range(len(edges[1])):
            if edges[x][y] == 255:
                inverted[x][y] = 0
            else:
                inverted[x][y] = 255
    cv2.imshow("final", inverted)
    cv2.imshow("the actual lines", edges)

    linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 1, None, 0, 0)

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)

    cv2.waitKey()

    cv2.waitKey(0)
    cv2.destroyAllWindows()
