import numpy as np
import utilities
try:
    from cv2 import cv2
except:
    import cv2

def get_posterized_edges(im, gaps = [6, 10, 16], n = 3):


    n = 4  # Number of levels of quantization

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
    lines = cv2.HoughLinesP(dst, 1, np.pi / 180, 1, None, 0, 0)
    newlines = []
    arraymax = max(len(gray),len(gray[1]))
    for line in lines:
        for seg in line:
            segment = []
            for point in seg:
                segment.append(point / arraymax)
        if max(segment) >=1:
            raise ValueError("more than one")
        newlines.append(segment)
    return newlines

if __name__ == "__main__":

    input_img = cv2.imread("obama.png")

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
