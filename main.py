import multiprocessing as mp
import cv2
import numpy as np
from odrive.enums import *
from face_full_processing import process_face

def main():
    import gantry
    import pickle
    import time

    scale_factor = 8
    offset = (0,0)

    def draw_progress(queue1, queue2):

        #figure out how to make a blank image, i'm too retarded / impatitiant to try to understand samir's shit
        img = np.zeros((800, 800, 3), np.uint8)
        old_x = 0
        old_y = 0
        while True:
            if queue1.empty() is False:
                seg = queue1.get()
                color = (255,0,0)
                i = 0
                for i in range(len(seg)-1):

                    # print(seg[i])
                    x1,y1,x2,y2 = seg[i][0], seg[i][1], seg[i+1][0], seg[i+1][1]
                    cv2.line(img,(int(x1 * 8 * 100),int(y1 * 8 * 100)),(int(x2 * 8 * 100),int(y2 * 8 *100)),color,2)
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


    def move(point):

        x,y = point
        x *= scale_factor
        y *= scale_factor


        x += offset[0]
        y += offset[1]

        print(f"moving to: {x}, {y}")

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

        print(f"moving to: {x}, {y}")

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

    segments, freq = segments, freq = process_face("ricardo.jpg", blur_radius = 17, lower_thresh = 0,
    upper_thresh = 40, splitDistance = 10, areaCut = 3,
    minSegmentLen = 15, max_accel = 2, max_lr = 1, turn_vel_multiplier = 1,
    freq = 60)


    gantry = gantry.Gantry()
    gantry.startup()
    print("started")


    # while True:
    #     gantry.set_pos_noblock(z=float(input()))

    pen_up()

    # input("press return to start")
    queue1 = mp.Queue()
    queue2 = mp.Queue()
    visualizer = mp.Process(target=draw_progress, args=(queue1, queue2))
    visualizer.start()
    pen_up()
    t0 = time.time()
    gantry.x.axis.controller.config.input_mode = INPUT_MODE_POS_FILTER
    gantry.y.axis.controller.config.input_mode = INPUT_MODE_POS_FILTER
    # gantry.x.axis.controller.config.input_mode = 1
    # gantry.y.axis.controller.config.input_mode = 1
    gantry.x.axis.controller.config.input_filter_bandwidth = freq/2
    gantry.y.axis.controller.config.input_filter_bandwidth = freq/2

    for i, seg in enumerate(segments):
        print(f"Currently on segment {i}/{len(segments)}")
        queue1.put(seg)
        blocked_move(seg[0])
        # print(seg[0])
        pen_down()
        for point in seg[1:]:
            while time.time() - t0 < 1/freq:
                pass
            t0 = time.time()
            move(point)

        pen_up()

    print("done")
    try:
        visualizer.terminate()
        queue1.put("e")
    except ValueError:
        print("sucsessfully terminated visualizer")
    pen_up()


    

if __name__ == "__main__":
    main()

