from cv2 import cv2
import numpy as np

def denoise_edges(image):


def spiral_out(x,y, spiral_radius):
    for j in range(1,spiral_radius+1):
        for i in range(x-j,x+j+1):
            yield (i,y+j)
            yield (i,y-j)
        for i in range(y-j+1, y+j):
            yield (x+j,i)
            yield (x-j,i)

def check_close(xP,yP):

    # for y in range(yP-20,yP+20):
    #     for x in range(xP-20, xP+20):
    #         if (x,y) == (xP, yP):
    #             continue
    #         if 0 <= x < edges.shape[1] and 0 <= y < edges.shape[0]:
    #             if edges[y][x] == 255:
    #                 return(x,y)

    for x,y in spiral_out(xP,yP, 50):
        if 0 <= x < edges.shape[1] and 0 <= y < edges.shape[0]:
            if edges[y][x] == 255:
                    return(x,y)
