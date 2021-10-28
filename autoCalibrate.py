import numpy as np
import tuning
import time
import random as rd
import grapher

grapher.init()
start_values = [.16,20,.32]
vel_range = [0, .3]
pos_range = [0, 250]
int_range = [0, 3]

mov_dist = 1
iteration_shift_factor = 1.1
total_trials = 5
odrv_num = 1

# DEFAULTS
# vel_gain = .16
# pos_gain = 20
# vel_integrator_gain = .32






def main(start_values, vel_range, pos_range, int_range):

    tuning.startup(odrv_num)
    absolute_min = 9223372036854775807
    best_values = []
    # tuning.start_liveplotter(lambda:[tuning.axis.controller.config.vel_gain])

    tuning.axis.controller.config.vel_gain = start_values[0]
    tuning.axis.controller.config.pos_gain = start_values[1]
    tuning.axis.controller.config.vel_integrator_gain = start_values[2]

    tuning.start_liveplotter(lambda: [tuning.axis.controller.input_pos, tuning.axis.encoder.pos_estimate])

    tuning.axis.controller.input_pos = 0
    time.sleep(3)


    current_values = start_values[:]

    for i in range(total_trials):

        print(f"\nTrial No: {i} ")

        baseline = tuning.evaluate_values(current_values, mov_dist, print_vals = True)

        shift = rd.choice([1/iteration_shift_factor, iteration_shift_factor])
        index = rd.randrange(0,3)

        test_values = current_values[:]
        test_values[index] *= shift
        cost = tuning.evaluate_values(test_values, mov_dist)
        cost_delta = cost - baseline

        if cost_delta < 0:
            current_values[index] *= shift

            if cost < absolute_min:
                print(f"old absolute_min: {absolute_min}")
                absolute_min = cost
                print(f"new absolute_min: {absolute_min}")
                best_values = current_values
        else:
            current_values[index] /= shift


        # print(f"deltas = {deltas}")
        print(f"current_values = {current_values}")
    print("calibraiton finished")
    #grapher.show_graph()

    print(f"Lowest cost: {absolute_min} \n At Values {best_values}")
    if input("Would you like to keep these values? y/N: ") == "y":
        tuning.save_configuration(odrv_num, best_values)







if __name__ == "__main__":
    main(start_values, vel_range, pos_range, int_range)
