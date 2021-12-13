import numpy as np
import utilities
try:
    from cv2 import cv2
except:
    import cv2

def get_posterized_edges(im, gaps = [3, 9, 18, 24], n = 3):


    n = 4  # Number of levels of quantization

    indices = np.arange(0, 256)  # List of all colors

    divider = np.linspace(0, 255, n + 1)[1]  # we get a divider

    quantiz = np.int0(np.linspace(0, 255, n))  # we get quantization colors

    color_levels = np.clip(np.int0(indices / divider), 0, n - 1)  # color levels 0,1,2..

    palette = quantiz[color_levels]  # Creating the palette

    poster = palette[im]  # Applying palette on image

    poster = cv2.convertScaleAbs(poster)  # Converting image back to uint8

    edges = im.copy()
    edges.fill(0)

    values = [255, 170, 85, 0]
    lines = []
    for i, value in enumerate(gaps):
        im = utilities.copy_blank(im)
        y = 0

        while y < len(im[0]):
            # for y in range(len(im[1])):
            #      if (x % value == 0) & (y % value == 0):
            #          im[x, y] = 255
            print(y)
            try:
                j = 0
                while True:
                    print(f"setting {y}, {y+j}")
                    im[j,y + j] = 255

                    j+=1


            except IndexError:
                print("pass")
                pass

            try:
                j = 0
                print(j)
                while True:
                    # print(f"setting {y}, {y+j}")
                    im[j,y + j] = 255

                    j-=1
            except IndexError:
                pass
            y+= value
            cv2.imshow("line", im)
            cv2.waitKey(1)



        lines.append(im)

    for value in values:
        if value == 255:
            continue
        line = lines.pop(0)
        for x in range(len(poster)):
            for y in range(len(poster[1])):
                if poster[x][y] == value:
                    edges[x][y] = line[x][y]






    cv2.imshow("posterized", edges)
    cv2.waitKey(0)








if __name__ == "__main__":

    input_img = cv2.imread("obama.png")

    gray = cv2.cvtColor(input_img,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = get_posterized_edges(gray)

    cv2.destroyAllWindows()
