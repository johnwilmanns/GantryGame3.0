from gantry import Gantry
import numpy as np
import time
import matplotlib.pyplot as plt

frequency_low = 1
frequency_high = 60
test_numbers = 2 #the number of different frequencies it tests
sampling_amount = 2 #the number of times it tests each frequency
magnitude = 2
command_frequency = 120



gantry = Gantry()
gantry.startup()
axis = gantry.x
axis.set_pos(1, ensure_control_mode= True)
frequencies = np.geomspace(frequency_low, frequency_high, num = test_numbers)
locations_list = []
for frequency in frequencies:
    locations = []
    positions = np.sin(np.arange(0, np.pi * 2, frequency * 1/command_frequency)) * magnitude
    print(positions)
    positions = positions * sampling_amount
    t0 = time.perf_counter()
    for position in positions:
        while True:
            if (time.perf_counter() - t0 >= 1/command_frequency):
                break
            locations.append([time.perf_counter(), axis.get_pos(), position])
        axis.set_pos(1 + magnitude + position)
    locations_list.append(locations)

for locations in locations_list:
    print("locations")
    x = locations[0]
    y = locations[1]
    y1 = locations[2]
    plt.plot(x, y, label="actual")
    plt.plot(x, y1, label="posaion")
    plt.show()
    input("pp???")
