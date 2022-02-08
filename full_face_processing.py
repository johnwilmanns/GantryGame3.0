import multiprocessing
from os import unlink
try:
    from cv2 import cv2
except:
    import cv2
import numpy as np
import random as rd
import copy
import time
import math
import sys
import pickle
from auto_edge import auto_canny
import posterize
import utilities


# from test import *

from full_path_planning import calc_path, plot_path, plot_path_full, distance

def plot_segments(segments, shape = (512 *2, 512 * 2)):
    
    
    # img = in_img.copy()
    # mask = cv2.inRange(img, (0,0,0), (255,255,255))
    # img[mask>0] = (255,255,255)
    
    img = 255 * np.ones(shape=[*shape, 3], dtype=np.uint8)

    for seg in segments:

        color = tuple(rd.randrange(0,255) for i in range(3))
        # color = (0,0,0)

        i = 0
        for i in range(len(seg)-1):

            # print(seg[i])
            x1,y1,x2,y2 = int(seg[i][0]*shape[0]), int(seg[i][1]*shape[0]), int(seg[i+1][0]*shape[1]), int(seg[i+1][1]*shape[1])
            
            cv2.line(img,(x1,y1), (x1,y1), (0,0,0), 4)
            cv2.line(img,(x2,y2), (x2,y2), (0,0,0), 4)
            cv2.line(img,(x1,y1),(x2,y2),color,2)
            
            
    color = (0,0,255)
    # for i in range(len(segments)-1):
        
    #     x1,y1,x2,y2 = int(segments[i][-1][0]*shape[0]), int(segments[i][-1][1]*shape[0]), int(segments[i+1][0][0]*shape[1]), int(segments[i+1][0][1]*shape[1])
    #     cv2.line(img,(x1,y1),(x2,y2),color,2)
                
    cv2.imwrite("test.jpg", img)
    cv2.imshow("images", img)
    cv2.waitKey(0)

def process_edges_raw(input_img, blur_radius = 15, lower_thresh = 5,
        upper_thresh = 40, bind_dist = 4, area_cut = 3,
        min_len = 3, q = None):

    t0 = time.time()
    
    gray = cv2.cvtColor(input_img,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (blur_radius, blur_radius), 0)

    edges = cv2.Canny(gray, lower_thresh, upper_thresh)
    edges = edges.astype(bool)
    edges = edges.tolist()


    max_size = max(input_img.shape[:2])


    #TODO add rust method here
    #segments = rust.process_image(edges, area_cut, 3, min_ler, bind_dist)

    for i, seg in enumerate(segments):
        for j, point in enumerate(seg):
            segments[i][j] = (point[0]/max_size,point[1]/max_size)

    print(f"took {time.time()-t0: .2f} seconds to process edges")


    
    print("Finished Edges")
    
    if q is not None:
        q.put(segments)

    return segments

def process_shading_raw(input_img, blur_radius = 21, line_dist = 10, theta = None, bind_dist = 4, area_cut = 3,
        min_len = 3, q = None):

    splitDistance = 1.5
    
    # input_img = utilities.resize(cv2.imread(filename))

    # input_img = cv2.imread("obama.png")
    
    gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (blur_radius, blur_radius), 0)
    shades = posterize.get_spinny(gray, line_dist, theta)
    all_segments = []
    
    max_size = max(input_img.shape[:2])

    t0 = time.time()

    for edges in shades:
        
        edges = edges.astype(bool)
        edges = edges.tolist()
        
        


        #TODO add rust method here
        #segments = rust.process_image(edges, area_cut, 3, min_ler, bind_dist)



        for i, seg in enumerate(segments):
            for j, point in enumerate(seg):
                segments[i][j] = (point[0]/max_size,point[1]/max_size)



        all_segments.extend(segments)
        
    print(f"took {time.time()-t0: .2f} seconds to process edges")
    
    if q is not None:
        q.put(segments)

    return segments

def process_combo_raw(input_img):

    print("starting edge processing")
    segments = process_edges_raw(input_img)
    print("starting shading processing")
    segments.extend(process_shading_raw(input_img))
    print("finished pre processing")
    return segments

def process_combo_raw_multi(input_img):
    from multiprocessing import Process
    
    q = multiprocessing.Queue()
    edges = Process(target=process_edges_raw, args=(input_img,), kwargs={"q": q})
    shading = Process(target=process_shading_raw, args=(input_img,), kwargs={"q": q})
    
    edges.start()
    shading.start()
    
    segments = q.get() + q.get()
    
    return segments
    
    


def process_combo(input_img, max_accel, max_radius, turn_vel_multiplier, freq):

    return calc_path(process_combo_raw(input_img), max_accel, max_radius, turn_vel_multiplier, freq)


if __name__ == "__main__":


    filename = "s1.jpg"
    filename = "C:/Users/Samir/OneDrive/Documents/Drawing Bot/GantryGame3.0/GantryGame3.0/lowres.jpg"
    
    if filename.find(".jpg") == -1:
        # Load .png image
        image = cv2.imread(filename)

        # Save .jpg image
        cv2.imwrite('image.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        input_img = cv2.imread("image.jpg")
    else:
        input_img = cv2.imread(filename)

    input_img = utilities.resize(input_img, 800, int(800 * input_img.shape[0]/input_img.shape[1]))

    # segments = process_combo(filename, 30, 1, 1, 120)
    # plot_path_full(segments)

    # segments= process_combo_raw_multi(input_img)
    # # segments = process_shading_raw(filename)
    # # segments = process_edges_raw(filename, blur_radius=15, lower_thresh=5, upper_thresh=40, areaCut=10, minNumPixels=5, segmentSplitDistance=20)
    # plot_segments(segments)

    t0 = time.perf_counter()
    segments = process_combo_raw_multi(input_img)
    print("face processing took: ", time.perf_counter()-t0) #Raw: 11.6, Raw_multi: 6.9

    t0 = time.perf_counter()    
    segments =  calc_path(segments, 40, .001, 1, 1020)
    print("calc processing took ", time.perf_counter() - t0) #1 thread: 4s, 4 threads: 1.65s, 8 threads 1.4s, 16 threads: 2.1s
    
    # plot_path_full(segments)
