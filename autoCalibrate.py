import numpy as np
import tuning
import time
import random as rd
import grapher


mov_dist = 1
mov_time = 1
iteration_shift_factor = 1.1
odrv_num = 1
axis_num = 1

rmse_weight = 1
variance_weight = 3



# DEFAULTS
# vel_gain = .16
# pos_gain = 20
# vel_integrator_gain = .32
grapher.init()
start_values = [.16,20,.32]
vel_range = [0, .3]
pos_range = [0, 250]
int_range = [0, 3]

def in_range(val, range):
    return range[0] <= val <= range[1]






def main(start_values, vel_range, pos_range, int_range):

    tuning.startup(odrv_num, axis_num)
    absolute_min = float("inf")
    best_values = []
    # tuning.start_liveplotter(lambda:[tuning.axis.controller.config.vel_gain])

    tuning.axis.controller.config.vel_gain = start_values[0]
    tuning.axis.controller.config.pos_gain = start_values[1]
    tuning.axis.controller.config.vel_integrator_gain = start_values[2]

    tuning.start_liveplotter(lambda: [tuning.axis.controller.input_pos, tuning.axis.encoder.pos_estimate])

    tuning.axis.controller.input_pos = 0
    time.sleep(3)


    current_values = start_values[:]

    print("press ctrl + c to exit")

    try:
        while True:

            print(f"\nTrial No: {i} ")

            try:
                shift = rd.choice([1/iteration_shift_factor, iteration_shift_factor])
                index = rd.randrange(0,3)
                test_values = current_values[:]
                test_values[index] *= shift

                assert in_range(test_values[0], vel_range)
                assert in_range(test_values[1], pos_range)
                assert in_range(test_values[2], int_range)
            except AssertionError as e:
                print(f"attempted to go out of bounds: {e}")
                continue

            baseline = tuning.evaluate_values(current_values, mov_dist, rmse_weight, variance_weight, mov_time, print_vals = True)
            cost = tuning.evaluate_values(test_values, mov_dist, mov_time)


            cost_delta = cost - baseline

            if cost_delta < 0:
                current_values[index] *= shift #TODO: multipy shift by the magnitude of delta

                if cost < absolute_min: #TODO: retry to unsure it truly is abs minimum
                    print(f"old absolute_min: {absolute_min}")
                    absolute_min = cost
                    print(f"new absolute_min: {absolute_min}")
                    best_values = current_values
            else:
                current_values[index] /= shift


            # print(f"deltas = {deltas}")
            print(f"current_values = {current_values}")

    except KeyboardInterrupt:
            
        print("calibraiton finished")
        #grapher.show_graph()

        print(f"Lowest cost: {absolute_min} \n At Values {best_values}")
        if input("Would you like to keep these values? y/N: ") == "y":
            tuning.save_configuration(odrv_num, best_values)







if __name__ == "__main__":
    main(start_values, vel_range, pos_range, int_range)
