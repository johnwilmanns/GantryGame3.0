from numpy.core.fromnumeric import var
import tuning
import time

start_values = [.16,20,.32]
vel_range = [0, .3]
pos_range = [0, 250]
int_range = [0, 3]

mov_dist = 1
iteration_shift_factor = 1.1
total_trials = 3


# DEFAULTS
# vel_gain = .16
# pos_gain = 20
# vel_integrator_gain = .32






def main(start_values, vel_range, pos_range, int_range):

    tuning.startup()

    tuning.axis.controller.config.vel_gain = start_values[0]
    tuning.axis.controller.config.pos_gain = start_values[1]
    tuning.axis.controller.config.vel_integrator_gain = start_values[2]

    tuning.axis.controller.input_pos = 0
    time.sleep(3)


    current_values = start_values[:]

    for i in range(total_trials):


        baselines = tuning.evaluate_values(current_values, mov_dist)

        deltas = []

        for i in range(3):
            test_values = current_values[:]
            test_values[i] *= iteration_shift_factor
            cost = tuning.evaluate_values(test_values, mov_dist)
            deltas.append(baselines[i] - cost)

        






        # tuning.axis.controller.input_pos = mov_dist
        # base_rmse, base_variance = tuning.analyze_move(2)
        # tuning.axis.controller.input_pos = 0
        # base_rmse, base_variance += tuning.analyze_move(2)
        # base_rmse, base_variance /= 2

        # tuning.axis.controller.config.vel_gain *= iteration_shift_factor





        # for i in range(measure_trials):
        #     tuning.axis.controller.input_pos = 0
        #     time.sleep(1)
        #     tuning.axis.controller.input_pos = mov_dist
        #     Rmse, Variance = tuning.analyze_move(2)

        #     rmse.append(Rmse)
        #     variance.append(Variance)

        #     rmse.append(Rmse)
        #     variance.append(Variance)
            
        # rmse = sum(rmse)/len(rmse)
        # variance = sum(variance)/len(variance)












    #
    



if __name__ == "__main__":
    main(start_values, vel_range, pos_range, int_range)