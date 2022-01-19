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
        upper_thresh = 40, segmentSplitDistance = 20, areaCut = 10,
        minNumPixels = 5, max_accel = 2, max_lr = .02, turn_vel_multiplier = 1, 
        freq = 60, plot_steps = False, q = None):

    splitDistance = 1.5

    def distance(x1, y1, x2, y2):
        return (((x2-x1) ** 2 + (y2 - y1) ** 2) ** .5)

    # def getAngle(a, b, c):
    #     ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    #     return ang + 360 if ang < 0 else ang

    def getArea(a, b, c):
        l1 = distance(*a, *b)
        l2 = distance(*b, *c)
        l3 = distance(*c, *a)

        p = (l1 + l2 + l3)/2
        area = math.sqrt(abs(p * (p - l1) * (p - l2) * (p - l3)))

        # area *= l3

        return area


    def middle_out(a, index):
        
        b = a[:]
        a_len = len(a)
        while b:
            yield b.pop(index * len(b) // len(a))

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

        for x,y in spiral_out(xP,yP, 2):
            if 0 <= x < edges.shape[1] and 0 <= y < edges.shape[0]:
                if edges[y][x] == 255:
                        return(x,y)

        return None

    def check_closes(xP,yP, radius):

        # for y in range(yP-20,yP+20):
        #     for x in range(xP-20, xP+20):
        #         if (x,y) == (xP, yP):
        #             continue
        #         if 0 <= x < edges.shape[1] and 0 <= y < edges.shape[0]:
        #             if edges[y][x] == 255:
        #                 return(x,y)

        count = 0
        for x,y in spiral_out(xP,yP, radius):
            if 0 <= x < edges.shape[1] and 0 <= y < edges.shape[0]:
                if edges[y][x] == 255:
                        count+=1

        return count

    

    gray = cv2.cvtColor(input_img,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (blur_radius, blur_radius), 0)

    edges = cv2.Canny(gray, lower_thresh, upper_thresh)
    # cv2.imshow("edges", edges)
    # cv2.waitKey(0)
    # edges2 = copy.deepcopy(edges)

    # for y in range(len(edges)):
    #     for x in range(len(edges[y])):
    #         if edges[y][x] == 255:
    #             # print(check_closes(x,y,1))
    #             if check_closes(x,y,1) < 2:
    #                 edges2[y][x] = 0

    # edges = edges2

    saved_edges = copy.deepcopy(edges)

    # cv2.imwrite('edges.jpg',edges)

    # combined = np.concatenate((edges, edges2), axis=1)
    # cv2.imshow("images", combined)
    # cv2.waitKey(0)

    tt0 = time.time() 

    points = []
    for y in range(len(edges)):
        for x in range(len(edges[y])):
            if edges[y][x] == 255:
                # print(check_closes(x,y,1))
                if check_closes(x,y,1) == 1:
                    points.append((x,y))
                        
    sortedPoints = [points[0]]

    len_points = len(points)

    
    
    i = 0
    while points:
    # for i in range(len_points-1):
        t0 = time.time()
        targetPoint = sortedPoints[i]

        if i % 50 == 0:

            print('\r', end="")
            print(f"{i/(len(points) + len(sortedPoints)) * 100: .2f}% complete", end = "")
        
        nearby = check_close(*targetPoint)

        if nearby is None:
            mindist = max(edges.shape[0:2])
            for j in points:
                dist = distance(targetPoint[0], targetPoint[1], j[0], j[1])
                if dist < mindist and j not in sortedPoints:
                    mindist = dist
                    nearby = j
                
                    
            
                # nearby = points[0]
            
        try:
            edges[nearby[1]][nearby[0]] = 0
        except TypeError:
            break

        sortedPoints.append(nearby)
        try:
            points.remove(nearby)
        except ValueError:
            pass\
        
        i += 1
        
        
    
    # filtered path = []


    segments = []
    index = 0
    i = 0
    while i < len(sortedPoints)-2:
        i+=1
        if distance(*(sortedPoints[i] + sortedPoints[i+1])) > splitDistance:
            segments.append(sortedPoints[index+1:i])
            index = i
    segments.append(sortedPoints[index+1:])



    i = 0
    while i < len(segments)-2:
        i+=1
        if len(segments[i]) < minNumPixels:
            segments.pop(i)
            i-=1

    i = 0
    while i < len(segments)-2:
        i+=1
        if distance(*segments[i-1][-1], *segments[i][0]) < segmentSplitDistance:
            segments[i-1:i+1] = [segments[i-1] + segments[i]]
            i-=1


    while True:
        # print("running iteration")
        seg_len = sum(len(seg) for seg in segments)

        for seg in segments:
            i = 0
            while i < len(seg)-3:
                i+=1
                if getArea(*seg[i:i+3]) < areaCut:
                    seg.pop(i+1)
                    i-=1
        if sum(len(seg) for seg in segments) == seg_len:
            break





    img = input_img.copy()
    mask = cv2.inRange(img, (0,0,0), (255,255,255))
    img[mask>0] = (255,255,255)
    # img = cv2.imread('shrik2.png')

    for seg in segments:

        # color = tuple(rd.randrange(0,255) for i in range(3))
        color = (0,0,0)

        i = 0
        for i in range(len(seg)-1):

            # print(seg[i])
            if distance(seg[i][0], seg[i][1], seg[i+1][0], seg[i+1][1]) < 2000:
                x1,y1,x2,y2 = seg[i][0], seg[i][1], seg[i+1][0], seg[i+1][1]
                
                cv2.line(img,(x1,y1), (x1,y1), (0,0,0), 4)
                cv2.line(img,(x2,y2), (x2,y2), (0,0,0), 4)
                cv2.line(img,(x1,y1),(x2,y2),color,2)
                
    

    # print(len(points))
    # print(len(lines))

    i = 0
    while i < len(segments):
        if len(segments[i]) <= 1:
            segments.pop(i)
            i-=1
        i+=1
    # for i in range(len(segments)):

    max_size = max(input_img.shape[:2])

    for i, seg in enumerate(segments):
        for j, point in enumerate(seg):
            segments[i][j] = (point[0]/max_size,point[1]/max_size)

    print("")
    print(f"took {time.time()-tt0: .2f} seconds to process all {len(sortedPoints)} points")


    # import os
    # import sys


    # with open(os.path.join(sys.path[0], "path.pickle"), "rb") as file:
    #         segments = pickle.load(file)
    #         print(segments)
        



    # print("{} segments with a total of {} points".format(len(segments), sum(len(seg) for seg in segments)))



    
    display = np.concatenate((input_img, cv2.cvtColor(saved_edges,cv2.COLOR_GRAY2RGB)), axis=1)
    display = np.concatenate((display, img), axis=1)
    
    if plot_steps:
        cv2.imshow("images", display)
        cv2.waitKey(0)

    # new_points = calc_path(segments, max_accel, max_lr, turn_vel_multiplier, freq)
    new_points = segments
    
    print("Finished Edges")
    
    if q is not None:
        q.put(new_points)

    return new_points

def process_shading_raw(input_img, blur_radius = 21, line_dist = 20, theta = None, segmentSplitDistance = 20, areaCut = 5,
                        minNumPixels = 15, max_accel = 2, max_lr = .02, turn_vel_multiplier = 1,
                        freq = 60, plot_steps = False, q = None):

    splitDistance = 1.5
    
    # input_img = utilities.resize(cv2.imread(filename))

    # input_img = cv2.imread("obama.png")
    
    gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (blur_radius, blur_radius), 0)
    shades = posterize.get_spinny(gray, line_dist, theta)
    

    def distance(x1, y1, x2, y2):
        return (((x2-x1) ** 2 + (y2 - y1) ** 2) ** .5)

    # def getAngle(a, b, c):
    #     ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    #     return ang + 360 if ang < 0 else ang

    def getArea(a, b, c):
        l1 = distance(*a, *b)
        l2 = distance(*b, *c)
        l3 = distance(*c, *a)

        p = (l1 + l2 + l3)/2
        area = math.sqrt(abs(p * (p - l1) * (p - l2) * (p - l3)))

        # area *= l3

        return area


    def middle_out(a, index):
        
        b = a[:]
        a_len = len(a)
        while b:
            yield b.pop(index * len(b) // len(a))

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

        for x,y in spiral_out(xP,yP, 2):
            if 0 <= x < edges.shape[1] and 0 <= y < edges.shape[0]:
                if edges[y][x] == 255:
                        return(x,y)

        return None

    def check_closes(xP,yP, radius):

        # for y in range(yP-20,yP+20):
        #     for x in range(xP-20, xP+20):
        #         if (x,y) == (xP, yP):
        #             continue
        #         if 0 <= x < edges.shape[1] and 0 <= y < edges.shape[0]:
        #             if edges[y][x] == 255:
        #                 return(x,y)

        count = 0
        for x,y in spiral_out(xP,yP, radius):
            if 0 <= x < edges.shape[1] and 0 <= y < edges.shape[0]:
                if edges[y][x] == 255:
                        count+=1

        return count

    new_points = []
    max_size = max(shades[0].shape[:2])

    img = shades[0].copy()
    img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    mask = cv2.inRange(img, (0,0,0), (255,255,255))
    img[mask>0] = (255,255,255)
    
    # shades = [shades[3]]
    for edges in shades:
        
        tt0 = time.time() 
        # edges = cv2.Canny(gray, lower_thresh, upper_thresh)
        edges2 = copy.deepcopy(edges)

        points = []
        for y in range(len(edges)):
            for x in range(len(edges[y])):
                if edges[y][x] == 255:
                    # print(check_closes(x,y,1))
                    if check_closes(x,y,1) == 1:
                        points.append((x,y))
                        # edges2[y][x] = 0

        edges = edges2

        # points = []
        # for y in range(len(edges)):
        #     for x in range(len(edges[y])):
        #         if edges[y][x] == 255:
        #             points.append((x,y))
                    
        sortedPoints = [points[0]]


        # tt0 = time.time() 
        i=0
        while points:
            t0 = time.time()
            targetPoint = sortedPoints[i]
            
            # if len_points <= 0:
            #     break


            if i % 50 == 0:

                print('\r', end="")
                print(f"{i/(len(points) + len(sortedPoints)) * 100: .2f}% complete", end = "")
            
            nearby = check_close(*targetPoint)

            if nearby is None:
                mindist = max(edges.shape[0:2])
                for j in points:
                    dist = distance(targetPoint[0], targetPoint[1], j[0], j[1])
                    if dist < mindist and j not in sortedPoints:
                        mindist = dist
                        nearby = j
                
                    
            
                # nearby = points[0]
            
            try:
                edges[nearby[1]][nearby[0]] = 0
            except TypeError:
                break

            sortedPoints.append(nearby)
            try:
                points.remove(nearby)
            except ValueError:
                pass
            
            
            
            i+=1
            
        print("")
        print(f"took {time.time()-tt0: .2f} seconds to sort all {len(sortedPoints)} points")
        # filtered path = []


        segments = []
        index = 0
        i = 0
        while i < len(sortedPoints)-2:
            i+=1
            if distance(*(sortedPoints[i] + sortedPoints[i+1])) > splitDistance:
                segments.append(sortedPoints[index+1:i])
                index = i
        segments.append(sortedPoints[index+1:])



        i = 0
        while i < len(segments)-2:
            i+=1
            if len(segments[i]) < minNumPixels:
                segments.pop(i)
                i-=1

        i = 0
        while i < len(segments)-2:
            i+=1
            if distance(*segments[i-1][-1], *segments[i][0]) < segmentSplitDistance:
                segments[i-1:i+1] = [segments[i-1] + segments[i]]
                i-=1


        while True:
            # print("running iteration")
            seg_len = sum(len(seg) for seg in segments)

            for seg in segments:
                i = 0
                while i < len(seg)-3:
                    i+=1
                    if getArea(*seg[i:i+3]) < areaCut:
                        seg.pop(i+1)
                        i-=1
            if sum(len(seg) for seg in segments) == seg_len:
                break

        # print(len(points))
        # print(len(lines))

        i = 0
        while i < len(segments):
            if len(segments[i]) <= 1:
                segments.pop(i)
                i-=1
            i+=1

        

        






        # import os
        # import sys


        # with open(os.path.join(sys.path[0], "path.pickle"), "rb") as file:
        #         segments = pickle.load(file)
        #         print(segments)
            



        # print("{} segments with a total of {} points".format(len(segments), sum(len(seg) for seg in segments)))


        if plot_steps:

            # raise NotImplementedError

            # img = cv2.imread('shrik2.png')

            for seg in segments:

                # color = tuple(rd.randrange(0,255) for i in range(3))
                color = (0,0,0)

                i = 0
                for i in range(len(seg)-1):

                    # print(seg[i])
                    if distance(seg[i][0], seg[i][1], seg[i+1][0], seg[i+1][1]) < 2000:
                        x1,y1,x2,y2 = seg[i][0], seg[i][1], seg[i+1][0], seg[i+1][1]
                        
                        # cv2.line(img,(x1,y1), (x1,y1), (0,0,0), 4)
                        # cv2.line(img,(x2,y2), (x2,y2), (0,0,0), 4)
                        cv2.line(img,(x1,y1),(x2,y2),color,2)

        for i, seg in enumerate(segments):
            for j, point in enumerate(seg):
                segments[i][j] = (point[0]/max_size,point[1]/max_size)


        # new_points = calc_path(segments, max_accel, max_lr, turn_vel_multiplier, freq)
        # new_points.extend(calc_path(segments, max_accel, max_lr, turn_vel_multiplier, freq))
        new_points.extend(segments)

    

    if plot_steps:

        cv2.imshow("images", img)
        cv2.waitKey(0)
    print("Finished Shading")
    if q is not None:
        q.put(new_points)

    return new_points

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

    filename = "C:/Users/Samir/OneDrive/Documents/Drawing Bot/GantryGame3.0/GantryGame3.0/brian.jpg"
    
    if filename.find(".jpg") == -1:
        # Load .png image
        image = cv2.imread(filename)

        # Save .jpg image
        cv2.imwrite('image.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        input_img = cv2.imread("image.jpg")
    else:
        input_img = cv2.imread(filename)

    # segments = process_combo(filename, 30, 1, 1, 120)
    # plot_path_full(segments)

    segments= process_combo_raw_multi(input_img)
    # segments = process_shading_raw(filename)
    # segments = process_edges_raw(filename, blur_radius=15, lower_thresh=5, upper_thresh=40, areaCut=10, minNumPixels=5, segmentSplitDistance=20)
    plot_segments(segments)

    # segments = process_shading_raw(filename, n=5, theta=math.pi/4)
    # segments =  calc_path(segments,  10, .001, 1, 60)
    # plot_path_full(segments)

