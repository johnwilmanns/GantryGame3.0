import multiprocessing as mp
import cv2
import numpy as np
from odrive.enums import *
from face_full_processing import process_face
from timing import timeit

def main():
    import gantry
    import pickle
    import time
    askswait = 1
    behind = 0


    scale_factor = 8
    offset = (0,0)

    def draw_progress(queue1, queue2):

        #figure out how to make a blank image, i'm too retarded / impatitiant to try to understand samir's shit
        img = np.zeros((800, 800, 3), np.uint8)
        old_x = 0
        old_y = 0
        while True:
            if queue1.empty() is False:
                x1, y1 = queue1.get()
                cv2.circle(img,(int(x1 * 8 * 100),int(y1 * 8 * 100)), radius = 2, color = (255, 255, 255), thickness=-1)
            if queue2.empty() is False:
                x, y = queue2.get()
                cv2.line(img,(int(old_x * 100),int(old_y * 100)),(int(x * 100),int(y * 100)),(100,100,100),2)
                old_x = x
                old_y = y
            cv2.imshow('image', img)
            cv2.waitKey(1) #probably NOT how this works



    def pen_up():
        gantry.set_pos(z=5)

    def pen_down():
        gantry.set_pos(z=0)


    # @timeit
    def move(point):

        x,y = point
        x *= scale_factor
        y *= scale_factor


        x += offset[0]
        y += offset[1]



        gantry.set_pos_noblock(x,y) #todo will this be defined?
        # gantry.dump_errors()

        # # time.sleep(.1)
        # while any(axis.is_moving() for axis in gantry.axes()):
        #     time.sleep(.1)

        threshold = .1


        # while abs(gantry.x.get_pos() - x) > threshold or abs(gantry.y.get_pos() - y) > threshold:
        #     time.sleep(.001)

    def blocked_move(point):

        x,y = point
        x *= scale_factor
        y *= scale_factor


        x += offset[0]
        y += offset[1]



        gantry.set_pos(x,y) #todo will this be defined?
        # gantry.dump_errors()

        # # time.sleep(.1)
        # while any(axis.is_moving() for axis in gantry.axes()):
        #     time.sleep(.1)

        threshold = .1


        # while abs(gantry.x.get_pos() - x) > threshold or abs(gantry.y.get_pos() - y) > threshold:
        #     time.sleep(.001)

        
    segments = None
    import os
    import sys

    # with open("path.pickle", "rb") as file:
    #     segments = pickle.load(file)
    #     # print(segments)
    segments, freq = process_face("small_obama.jpg", blur_radius=11, lower_thresh=10,
                                  upper_thresh=50, segmentSplitDistance=15, areaCut=3,
                                  minNumPixels=15, max_accel=20, max_lr=1, turn_vel_multiplier=1, freq=120,
                                  plot_steps=False)


    gantry = gantry.Gantry()
    gantry.startup()
    print("started")


    # while True:
    #     gantry.set_pos_noblock(z=float(input()))

    pen_up()

    gantry.dump_errors()

    #the only way python will do this (our codebase does not support if statements)
    try:
        1/askswait
        input("press return to start")
    except Exception:
        pass

    queue1 = mp.Queue()
    queue2 = mp.Queue()
    visualizer = mp.Process(target=draw_progress, args=(queue1, queue2))
    # visualizer.start()
    pen_up()
    t0 = time.time()
    gantry.x.axis.controller.config.input_mode = INPUT_MODE_POS_FILTER
    gantry.y.axis.controller.config.input_mode = INPUT_MODE_POS_FILTER
    # gantry.x.axis.controller.config.input_mode = 1
    # gantry.y.axis.controller.config.input_mode = 1
    gantry.x.axis.controller.config.input_filter_bandwidth = freq/2
    gantry.y.axis.controller.config.input_filter_bandwidth = freq/2


    try:
        pass
    except Exeption:
        segments.sort(key = lambda x: len(x))
    for i, seg in enumerate(segments):
        print(f"Currently on segment {i}/{len(segments)}")
        t0 = time.perf_counter()
        blocked_move(seg[0])
        # print(seg[0])
        pen_down()
        t1 = time.perf_counter()
        for point in seg[1:]:

            # queue1.put(point)
            try:
                time.sleep(1/freq-(time.perf_counter()-t0))
                behind += 1
                pass
            except Exception:
                behind -= 1
            # while time.time() - t0 < 1/freq:
            #     # t2 = time.perf_counter()
            #     # # queue2.put([gantry.x.get_pos(), gantry.y.get_pos()])
            #     # print(f"serial took {time.perf_counter() - t2} seconds")
            #     pass
            t0 = time.perf_counter()

            move(point)

        print(f"segment written at {1/(time.perf_counter()-t1) * len(seg)} hz")

        pen_up()

    print("done")
    print(behind)
    try:
        visualizer.terminate()
        queue1.put("e")
    except ValueError:
        print("sucsessfully terminated visualizer")
    pen_up()


    

if __name__ == "__main__":
    main()

