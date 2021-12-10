from cv2 import cv2
import numpy as np


"""
How it works:
spirals out, finds all the pixels one away
if there are not two it deletes the original pixel
then it takes the ajacent pixels, and makes sure that there are more pixels outside that are not the other pixels it found
checks to see if the ones one away have another one one away
"""
'''
Key:
white: unprocessed edge
2: one away
4: 
'''

def fill_gaps(input_img):
    for x in range(len(input_img)):
        for y in range(len(input_img[0])):

            try:
                if input_img[x][y-1] == 255:
                    if input_img[x][y+1]==255:
                        input_img[x][y] = 255
            except IndexError:
                pass

            try:
                if input_img[x-1][y] == 255:
                    if input_img[x+1][y]==255:
                        input_img[x][y] = 255
            except IndexError:
                pass

            try:
                if input_img[x-1][y-1] == 255:
                    if input_img[x+1][y+1]==255:
                        input_img[x][y] = 255
            except IndexError:
                pass

            try:
                if input_img[x-1][y+1] == 255:
                    if input_img[x+1][y-1]==255:
                        input_img[x][y] = 255
            except IndexError:
                pass
            print(f"just chekced {x}, {y}")
            # cv2.imshow("dingaling", input_img)
            # cv2.waitKey(1)
    return input_img


def denoise_edges(input_img):
    input_img = input_img.copy()
    img = input_img.copy()
    img.fill(0)

    for x in range(len(img)):
        for y in range(len(img[0])):
            if input_img[x][y] == 255:
                fun_zone = input_img.copy() #declares and initializes fun zone
                fun_zone[x][y] = 10
                potential_points = []

                for xP, yP in spiral_out(x, y, 1):
                    try:
                        if fun_zone[xP][yP] == 255:  # todo, is this right samir?
                            potential_points.append([xP, yP])
                        fun_zone[xP][yP]=100
                    except IndexError:
                        pass
                # cv2.imshow("funzone", fun_zone)
                # cv2.waitKey(0)

                if len(potential_points) < 2:
                    print("found no potential points")
                    print(potential_points)

                    continue
                else:
                    print(f"point good at {x}, {y}")
                    print(potential_points)
                    img[x][y] = 255
                    continue
                pointctr = 0
                lastk = 0
                for k, point in enumerate(potential_points):
                    print(point)
                    px,py = point
                    if k == lastk:
                        continue
                    if pointctr >=2:
                        break
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if (i == 0) and (j == 0):
                                continue
                            try:
                                if fun_zone[px + i][py + j] == 255:
                                    fun_zone[px + i][py + j] == 20
                                    pointctr += 1
                                    lastk = k
                            except IndexError:
                                pass
                if pointctr >= 2:
                    print(f"point good at {x}, {y}")
                    img[x][y] = 255

        cv2.imshow("dingaling", img)
        cv2.waitKey(1)
    return img






def spiral_out(x,y, spiral_radius):
    for j in range(1,spiral_radius+1):
        for i in range(x-j,x+j+1):
            yield (i,y+j)
            yield (i,y-j)
        for i in range(y-j+1, y+j):
            yield (x+j,i)
            yield (x-j,i)
