import random as rd
import tuning

def optimize(cost_func, starting_values, value_ranges, recurse = True):

    shift_ratio = 1.1
    
    if recurse:
        optimize(cost_func, starting_values, value_ranges, False)
    else:
        current_values = starting_values
        test_values = starting_values

        deltas = []

        for value in

