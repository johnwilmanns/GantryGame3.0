from matplotlib.pyplot import plot
import numpy as np
# imports full path planning
import full_path_planning
import utilities
import full_face_processing
import math

# imports cv2

try:
    from cv2 import cv2  # 'ery nice
except:
    import cv2


# gets the posturized edges
def get_posterized_edges(im, gaps=[5, 10, 15]):
    n = len(gaps) + 1  # Number of levels of quantization

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
                    im[j, y + j] = 255

                    j += 1


            except IndexError:
                # print("pass")
                pass

            try:
                j = 0
                # print(j)
                while True:
                    # print(f"setting {y}, {y+j}")
                    im[j, y + j] = 255

                    j -= 1
            except IndexError:
                pass
            y += value
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


def slope(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    if x2 != x1:
        return ((y2 - y1) / (x2 - x1))
    else:
        return 'NA'


# draws lines all the way accross
def make_linerinos(image, p1, p2, color=255):
    x1, y1 = p1
    x2, y2 = p2
    ### finding slope
    m = slope(p1, p2)
    ### getting image shape
    h, w = image.shape[:2]

    if m != 'NA':
        ### here we are essentially extending the line to x=0 and x=width
        ### and calculating the y associated with it
        ##starting point
        px = 0
        py = -(x1 - 0) * m + y1
        ##ending point
        qx = w
        qy = -(x2 - w) * m + y2
    else:
        ### if slope is zero, draw a line with x=x1 and y=0 and y=height
        px, py = 0, h
        qx, qy = w, h
    cv2.line(image, (int(px), int(py)), (int(qx), int(qy)), color, 1)
    return image


# should have x and y in the correct order, don't @ me tho...
# this is the least efficient implementation possible, but i'm tired so i'm not gonna do it in a good way...
'''shit method I really should have programmed while I was awake, but being awake is rather cringe'''


def get_spinny(im, line_dist=30, theta=None, thresholds = [30, 50, 80, 85, 90]):

    n = len(thresholds)
    blank = im.copy()
    blank.fill(0)
    imx = im.shape[1]
    imy = im.shape[0]
    if theta is None:
        theta = math.pi / n

    images = []

    for thresh in thresholds:
        out = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 501, thresh)
        images.append(out)
        # cv2.imshow("test", out)
        # cv2.waitKey(0)


    # indices = np.arange(0, 256)  # List of all colors
    #
    # divider = np.linspace(0, 255, n + 1)[1]  # we get a divider
    # divider = 255//n
    #
    # quantiz = np.int0(np.linspace(0, 255, n))  # we get quantization colors
    #
    # color_levels = np.clip(np.int0(indices / divider), 0, n - 1)  # color levels 0,1,2..
    #
    # palette = quantiz[color_levels]  # Creating the palette
    #
    # poster = palette[im]  # Applying palette on image
    #
    # poster = cv2.convertScaleAbs(poster)  # Converting image back to uint8


    # cv2.imshow("poster", poster)
    hatch = im.copy()
    hatch.fill(0)

    # makes an array of the line doohickers, pixel value corrisponds to the depth, has go go opposite direction
    lines = []
    for i in range(n):
        # print("\r" + doin[j % len(doin)])
        hatch = utilities.copy_blank(hatch)
        θ = (i+1) * theta
        # θ = math.pi+ 2
        # yspace = 100
        # xspace = int(yspace * math.tan(θ))
        θ2 = θ + math.pi / 2

        image_center = tuple(i / 2 for i in hatch.shape)
        length = int(max(image_center) * 2)

        for direction in (-1, 1):
            for i in range(0, direction * length, direction * line_dist):
                x, y = image_center[0] + i * math.cos(θ2), image_center[1] + i * math.sin(θ2)

                x1 = math.floor(x - length * math.cos(θ))
                y1 = math.floor(y - length * math.sin(θ))

                x2 = math.floor(x + length * math.cos(θ))
                y2 = math.floor(y + length * math.sin(θ))

                hatch = cv2.line(hatch, (x1, y1), (x2, y2), 255, 1)

                # cv2.imshow("eeouu", hatch)

        # for j in range(imy * -1, imy, density):
        #     # hatch = make_linerinos(hatch, [0,y],[xspace, y + yspace])

        #     x1 = j * math.cos(θ2)
        #     y1 = j * math.sin(θ2)
        #     length = 10000

        #     x2 = int(x1 + length * math.cos(θ))
        #     y2 = int(y1 + length * math.sin(θ))

        #     x1 = int(x1)
        #     y1 = int(y1)

        #     hatch = cv2.line(hatch, (x1,y1), (x2, y2), 255, 1)

        lines.append(hatch)

        # cv2.imshow("hatch", hatch)
        # cv2.waitKey(0)
    edges = []
    for img, line in zip(images, lines):
        edge = blank.copy()
        for x in range(imx):
            for y in range(imy):

                if img[y][x] == 0:
                    if line[y][x] == 255:
                        edge[y][x] = 255
        # cv2.imshow("edges", edge)
        # cv2.waitKey(0)
        edges.append(edge)


    # quantiz = quantiz.tolist()
    # quantiz.reverse()
    # # quantiz[1] = 255  # kills the first layer of hatches
    # # quantiz[2] = 255 # poopoo peee poo
    # # quantiz[3] = 255
    # edges = []
    # for quant in quantiz:
    #     edge = blank.copy()
    #     print(f"checking quant: {quant}")
    #     if quant == 255:
    #         continue
    #     line = lines.pop(0)
    #     for x in range(imx):
    #         for y in range(imy):
    #
    #             if poster[y][x] <= quant:
    #                 if line[y][x] == 255:
    #                     edge[y][x] = 255
    #     # cv2.imshow("edges", edge)
    #     # cv2.waitKey(0)
    #     edges.append(edge)
    #     # cv2.imshow("eouoeuoeu", edge)
    #     # cv2.waitKey(0)

    return edges

    # def get_segments(input_img, gaps = [5, 10, 15]):
    #     gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    #     gray = cv2.GaussianBlur(gray, (3, 3), 0)
    #     edges = get_posterized_edges(gray)
    #     dst = edges
    #     lines = []
    #     arraymax = max(len(gray),len(gray[1]))
    #     for x in range(len(edges)):
    #         for y in range(len(edges[0])):
    #             if edges[x][y] == 255:
    #                 initpoint = [x,y]
    #                 i = x
    #                 k = y
    #                 try:
    #                     while edges[i,k] == 255:
    #                         edges[i,k] = 10
    #                         i +=1
    #                         k +=1
    #                         # print(f"trying {i}, {k}")
    #                 except IndexError:
    #                     pass
    #                 # print(f"added {i}, {k}")
    #                 if (abs(initpoint[0] - i) ** 2  + abs(initpoint[1] - k) ** 2) ** .5 >= 10:
    #                     lines.append([[initpoint[0]/arraymax, initpoint[1]/arraymax],[(i-1)/arraymax,(k-1)/arraymax]])

    return lines


def get_calcd_path(input_img, gaps=[5, 10, 15], max_accel=10, max_lr=.01, turn_vel_multiplier=1, freq=60, john="dumb"):
    return full_path_planning.calc_path(get_segments(input_img, gaps), max_accel, max_lr, turn_vel_multiplier, freq)


if __name__ == "__main__":
    input_img = utilities.resize(cv2.imread("small_obama.jpg"))
    # input_img = cv2.imread("obama.png")

    gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = get_spinny(gray, 5, 10)
    full_face_processing.process_shading(edges, plot_steps=True, segmentSplitDistance=2, minNumPixels=3)

    print('calc\'d path')
    # cv2.imshow("pp", (255-edges))
    # print(parts)
    # full_face_processing.plot_path_full(parts)

    # dst = edges
    #
    # # Copy edges to the images that will display the results in BGR
    # cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    # cdstP = np.copy(cdst)
    # inverted = utilities.copy_blank(edges)
    # for x in range(len(edges)):
    #     for y in range(len(edges[1])):
    #         if edges[x][y] == 255:
    #             inverted[x][y] = 0
    #         else:
    #             inverted[x][y] = 255
    # cv2.imshow("final", inverted)
    # cv2.imshow("the actual lines", edges)

    # linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 1, None, 0, 0)
    #
    # if linesP is not None:
    #     for i in range(0, len(linesP)):
    #         l = linesP[i][0]
    #         cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 2, cv2.LINE_AA)
    #
    # cv2.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)
    #
    # cv2.waitKey()

    cv2.waitKey(0)
    cv2.destroyAllWindows()
