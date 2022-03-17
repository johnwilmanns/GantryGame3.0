from gantry import Gantry
import numpy as np
import time
frequency_low = 1
frequency_high = 60
test_numbers = 10
sampling_amount = 10
magnitude = 2
command_frequency = 120



# gantry = Gantry()
# gantry.startup()
# axis = gantry.x
frequencies = np.geomspace(frequency_low, frequency_high, num = test_numbers)
locations = []
for frequency in frequencies:
    positions = np.sin(np.arange(0, np.pi * 2, 1/frequency * command_frequency)) * magnitude
    print(positions)
    location = []
    for i in range(sampling_amount):
        # gantry.set_pos(1, 1)

        pass