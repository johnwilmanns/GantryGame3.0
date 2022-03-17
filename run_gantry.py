import multiprocessing as mp
import cv2
import numpy as np
from odrive.enums import *

import utilities
# from image_processing import process_combo_raw_multi
from trajectory_planning import calc_path

import servo
from servo import pen_up, pen_down

from gantry import Gantry
import pickle
import time
askswait = 1
behind = 0


scale_factor = 1 #TODO fix
offset = (0,0)

    
# @timeit
def move(point):
    
    x,y = point
    x *= scale_factor
    y *= scale_factor


    x += offset[0]
    y += offset[1]



    gantry.set_pos_noblock(x,y) #todo will this be defined?

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



# segments = None
import os
import sys

# with open("path.pickle", "rb") as file:
#     segments = pickle.load(file)
#     # print(segments)

# segments = process_combo("brian.jpg", 10, .01, 1, freq)


# segments = process_combo(filename, 30, 1, 1, 120)
# plot_path_full(segments)




gantry = Gantry()
gantry.startup()

# servo.set_up()
# servo.set_down()

def main(segments, freq):
    
    
    print("started")


    # while True:
    #     gantry.set_pos_noblock(z=float(input()))

    # pen_up()
    # input("confirm up")
    
    # pen_down()
    # input("confirm down")
    
    # gantry.dump_errors()

    #the only way python will do this (our codebase does not support if statements)


    gantry.enable_motors()
    pen_up()
    input("confirm up")
    
    t0 = time.time()
    gantry.x.axis.controller.config.input_mode = INPUT_MODE_POS_FILTER
    gantry.y.axis.controller.config.input_mode = INPUT_MODE_POS_FILTER
    # gantry.x.axis.controller.config.input_mode = 1
    # gantry.y.axis.controller.config.input_mode = 1
    gantry.x.axis.controller.config.input_filter_bandwidth = freq/2
    gantry.y.axis.controller.config.input_filter_bandwidth = freq/2
    gantry.dump_errors()

    try:
        pass
    except Exception:
        segments.sort(key = lambda x: len(x))
    for i, seg in enumerate(segments):
        print(f"Currently on segment {i}/{len(segments)}")
        t0 = time.perf_counter()
        blocked_move(seg[0])
        print("finsheb dlocking move")
        # print(seg[0])
        pen_down()
        t1 = time.perf_counter()
        for point in seg[1:]:

            # queue1.put(point)
            try:
                time.sleep(1/freq-(time.perf_counter()-t0))

                pass
            except Exception:
                pass
            # while time.time() - t0 < 1/freq:
            #     # t2 = time.perf_counter()
            #     # # queue2.put([gantry.x.get_pos(), gantry.y.get_pos()])
            #     # print(f"serial took {time.perf_counter() - t2} seconds")
            #     pass
            t0 = time.perf_counter()

            move(point)

        time.sleep(1/freq)
        # t3 =
        pen_up()
        # time.sleep(1/freq)
        print(f"segment written at {1 / (time.perf_counter() - t1) * len(seg)} hz")
        

    print("done")
    pen_up()


    

if __name__ == "__main__":
    print('pp')