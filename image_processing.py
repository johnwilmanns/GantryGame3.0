
import cv2
import numpy as np
import time
import math


import posterize
import utilities
import rust
import auto_edge


# from test import *


def plot_segments(segments, shape = (540*2, 960*2)):
    
    
    # img = in_img.copy()
    # mask = cv2.inRange(img, (0,0,0), (255,255,255))
    # img[mask>0] = (255,255,255)
    
    img = 255 * np.ones(shape=[*shape, 3], dtype=np.uint8)

    for seg in segments:

        # color = tuple(rd.randrange(0,255) for i in range(3))
        color = (0,0,0)

        i = 0
        for i in range(len(seg)-1):

            # print(seg[i])
            x1,y1,x2,y2 = int(seg[i][0]*shape[1]), int(seg[i][1]*shape[1]), int(seg[i+1][0]*shape[1]), int(seg[i+1][1]*shape[1])
            
            
            cv2.line(img,(x1,y1),(x2,y2),color,1)
            cv2.line(img,(x1,y1), (x1,y1), (0,0,255), 4)
            cv2.line(img,(x2,y2), (x2,y2), (0,0,255), 4)
            
    color = (0,0,255)
    # for i in range(len(segments)-1):
        
    #     x1,y1,x2,y2 = int(segments[i][-1][0]*shape[0]), int(segments[i][-1][1]*shape[0]), int(segments[i+1][0][0]*shape[1]), int(segments[i+1][0][1]*shape[1])
    #     cv2.line(img,(x1,y1),(x2,y2),color,2)
                
                
    
    return img
    
    cv2.imwrite("test.jpg", img)

    cv2.imshow("images", img)
    cv2.waitKey(0)

    

def process_edges_raw(input_img, blur_radius = 11, lower_thresh = 0, upper_thresh = 20, aperture_size = 3, bind_dist = 10, area_cut = 3,
        min_len = 20, calc_rogues = False):

    t0 = time.time()
    
    gray = cv2.cvtColor(input_img,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (blur_radius, blur_radius), 0)

    edges = cv2.Canny(gray, lower_thresh, upper_thresh, apertureSize=aperture_size)
    # edges = auto_edge.auto_canny(gray, sigma)
    
    # cv2.imshow("edges", edges)
    cv2.imwrite("edges.png", edges)
    # cv2.waitKey(0)

    # exit(0)
    # return
    
    
    # cv2.imshow("edges", edges)
    # cv2.imwrite("thisdontwork.png", edges)
    # cv2.waitKey(0)

    edges = edges.astype(bool)
    edges = edges.tolist()


    max_size = max(input_img.shape[:2])


 
    segments = rust.process_image(edges, area_cut, 3, min_len, bind_dist, calc_rogues)

    for i, seg in enumerate(segments):
        for j, point in enumerate(seg):
            segments[i][j] = (point[0]/max_size,point[1]/max_size)

    print(f"took {time.time()-t0: .2f} seconds to process edges")


    
    # print("Finished Edges")
    

    return segments

def process_shading_raw(input_img, blur_radius = 21, line_dist = 5, theta = None, bind_dist = 10, area_cut = 10,
        min_len = 15, thresholds = [10, 30, 50, 80]):

    splitDistance = 1.5
    
    # input_img = utilities.resize(cv2.imread(filename))

    # input_img = cv2.imread("obama.png")
    
    gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (blur_radius, blur_radius), 0)
    shades = posterize.get_spinny(gray, line_dist, theta, thresholds)
    
    all_segments = []
    
    max_size = max(input_img.shape[:2])

    t0 = time.time()

    for edges in shades:
        
        # cv2.imshow("edges", edges)
        # cv2.imwrite("thisdontwork.png", edges)
        # cv2.waitKey(0)
        edges = edges.astype(bool)
        edges = edges.tolist()
        
        


        #TODO add rust method here
        segments = rust.process_image(edges, area_cut, 3, min_len, bind_dist, False)
        if not segments:
            print("warning, empty segments list")
            continue;

        # print(segments)
        # print(len(segments))

        for i, seg in enumerate(segments):
            for j, point in enumerate(seg):
                segments[i][j] = (point[0]/max_size,point[1]/max_size)



        all_segments.extend(segments)
        
    print(f"took {time.time()-t0: .2f} seconds to process shading")
    
    

    return all_segments

def process_shading_raw_wave(input_img, blur_radius = 21, line_dist = 10, theta = None, bind_dist = 20, area_cut = 10,
        min_len = 0, q = None, render = False):

    splitDistance = 1.5

    # input_img = utilities.resize(cv2.imread(filename))

    # input_img = cv2.imread("obama.png")

    gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (blur_radius, blur_radius), 0)
    shades = posterize.wave_function(gray, line_dist = 10, wave_int = 4)
    # return shades
    if render:
        return shades

    all_segments = []

    max_size = max(input_img.shape[:2])

    t0 = time.time()

    for edges in shades:

        # cv2.imshow("edges", edges)
        # cv2.imwrite("thisdontwork.png", edges)
        # cv2.waitKey(0)
        edges = edges.astype(bool)
        edges = edges.tolist()




        #TODO add rust method here
        segments = rust.process_image(edges, area_cut, 3, min_len, bind_dist)
        if not segments:
            print("warning, empty segments list")
            continue;

        # print(segments)
        # print(len(segments))

        for i, seg in enumerate(segments):
            for j, point in enumerate(seg):
                segments[i][j] = (point[0]/max_size,point[1]/max_size)



        all_segments.extend(segments)

    print(f"took {time.time()-t0: .2f} seconds to process edges")

    if q is not None:
        q.put(all_segments)

    return all_segments

def process_combo_raw(input_img, blur_radius = 11, lower_thresh = 0, upper_thresh = 20, aperture_size = 3, bind_dist = 10, area_cut = 3,
        min_len = 20, calc_rogues = False, blur_radius_shade = 21, line_dist = 5, theta = None, bind_dist_shade = 10, area_cut_shade = 10,
        min_len_shade = 15, thresholds = [10, 30, 50, 80]):

    print("starting edge processing")
    segments = process_edges_raw(input_img, blur_radius, lower_thresh, upper_thresh, aperture_size, bind_dist, area_cut,
        min_len, calc_rogues)
    print("starting shading processing")
    segments.extend(process_shading_raw(input_img, blur_radius_shade, line_dist, theta, bind_dist_shade, area_cut_shade,
        min_len_shade, thresholds))
    print("finished pre processing")
    
    

    
    return segments

def render_combo(input_img):
    img = process_edges_raw(input_img, render=True)
    for edges in process_shading_raw(input_img, render=True):
        img |= edges

    return np.invert(img)
    # edges.extend()
    
    return img
    



if __name__ == "__main__":


    # filename = "s1.jpg"
    filename = "picassopicture.png"
    
    input_img = cv2.imread(filename)
    # print(input_img)
    t0 = time.time()
    render = process_combo_raw(input_img)
    # img = plot_segments(render)
    print("time: ", time.time()-t0)
    

    # t0 = time.perf_counter()
    # segments = process_combo_raw(input_img)
    # print("combo took", time.perf_counter()-t0)
    
    # img = plot_segments(segments)
    # # img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    # img = np.fliplr(img)
    # cv2.imshow("picasso pic", img)
    # cv2.waitKey(0)