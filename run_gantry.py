import multiprocessing as mp
import cv2
import numpy as np
from odrive.enums import *

import utilities
# from image_processing import process_combo_raw_multi
from trajectory_planning import calc_path
import trajectory_planning
import servo
from servo import pen_up, pen_down

from gantry import Gantry, MoveError
import pickle
import time



Y_MAX = 8
X_MAX = 16

X_RES = 1920
Y_RES = 1080

if X_RES > Y_RES:
    scale_factor = min(Y_MAX/(Y_RES/X_RES), X_MAX)
else :
    scale_factor = min(X_MAX/(X_RES/Y_RES), Y_MAX)

# scale_factor = 8

# offset = (1,.5)


def distance(x1, y1, x2, y2):
    return (((x2-x1) ** 2 + (y2 - y1) ** 2) ** .5) 
# @timeit
def move(point):


    x,y = point
    x *= scale_factor
    y *= scale_factor






    gantry.set_pos_noblock(x,y) 

def blocked_move(point):

    x,y = point
    x *= scale_factor
    y *= scale_factor





    # gantry.set_po-s(x,y) #
    gantry.trap_move(x,y, threshold=.05) #todo tune thresh
    
    gantry.x.axis.controller.config.input_mode = INPUT_MODE_POS_FILTER
    gantry.y.axis.controller.config.input_mode = INPUT_MODE_POS_FILTER
    gantry.y2.axis.controller.config.input_mode = INPUT_MODE_POS_FILTER
    
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
    failed_move = False
    
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
    # input("confirm up")
    
    t0 = time.time()
    gantry.x.axis.controller.config.input_mode = INPUT_MODE_POS_FILTER
    gantry.y.axis.controller.config.input_mode = INPUT_MODE_POS_FILTER
    gantry.y2.axis.controller.config.input_mode = INPUT_MODE_POS_FILTER
    
    
    # gantry.x.axis.controller.config.input_mode = 1
    # gantry.y.axis.controller.config.input_mode = 1
    gantry.x.axis.controller.config.input_filter_bandwidth = freq/2
    gantry.y.axis.controller.config.input_filter_bandwidth = freq/2
    gantry.y2.axis.controller.config.input_filter_bandwidth = freq/2
    gantry.dump_errors()

    # print(trajectory_planning.calc_distance(segments))
    # trajectory_planning.update_path_distance(segments)

    deltas = []

    try:
        pass
    except Exception:
        segments.sort(key = lambda x: len(x))
    for i, seg in enumerate(segments):
        print(f"Currently on segment {i}/{len(segments)}")
        t0 = time.perf_counter()

        try:
            blocked_move(seg[0])
        except MoveError:
            if not failed_move:
                print("failed move")
                failed_move = True
                continue
            else:
                print("failed move again")
                # log here!
                # gantry.dump_errors()
                # gantry.clear_errors()
                servo.pen_high_up()
                gantry.startup()
                gantry.enable_motors()
                failed_move = False

                try:
                    blocked_move(seg[0])
                except MoveError:
                    print("failed for 3rd time, exiting")
                    break




        print("finsheb dlocking move")
        # print(seg[0])
        pen_down()
        t1 = time.perf_counter()
        for i, point in enumerate(seg[1:]):

            # queue1.put(point)
            # try:

                # time.sleep(1/freq-(time.perf_counter()-t0))
            
            t0 = time.perf_counter()  
            move(point)        
        
            # x_targ = gantry.x.axis.controller.pos_setpoint
            # y_targ = gantry.y.axis.controller.pos_setpoint
            x_targ = point[0]
            y_targ = point[1]
            
            

            # while(time.perf_counter()-t0 < (1/freq)):
            #     deltas.append((abs(gantry.x.get_pos() - x_targ), abs(gantry.y.get_pos() - y_targ), distance(*seg[i-1], *point)))
            #     pass

            while time.perf_counter() - t0 < 1/freq:
                # print("poop")
            #     # t2 = time.perf_counter()
            #     # # queue2.put([gantry.x.get_pos(), gantry.y.get_pos()])
            #     # print(f"serial took {time.perf_counter() - t2} seconds")
                pass


            

        time.sleep(1/freq)
        print(f"segment written at {1 / (time.perf_counter() - t1) * len(seg)} hz")
        # t3 =
        pen_up()
        # time.sleep(1/freq)
        
        

    print("done")
    pen_up()
    
    def plot_deltas():
        import matplotlib.pyplot as plt
        plt.plot(deltas)
        plt.show()
        
    # plot_deltas()
    servo.pen_high_up()

    

if __name__ == "__main__":
    # path = [[[1,1], [16,1], [16,8], [1,8]]]
    path = [[(0,0), (1,0), (1,1)]]
    
    segments = calc_path(path, 10, .001, 0, 60)
    print(segments)
    
    main(segments, 60)
    
    