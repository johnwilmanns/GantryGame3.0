from gantry import Gantry
import numpy as np
import time
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show

frequency_low = 3
frequency_high = 60
test_numbers = 3  #the number of different frequencies it tests
sampling_amount = 10 #the number of times it tests each frequency
magnitude = 4
command_frequency = 60



gantry = Gantry()
gantry.startup()
axis = gantry.x
axis.set_pos(1, ensure_control_mode= True)
time.sleep(1)
frequencies = np.geomspace(frequency_low, frequency_high, num = test_numbers)
locations_list = []
for frequency in frequencies:
    locations = []
    positions = np.sin(np.arange(0, np.pi * 2, frequency * 1/command_frequency)) * magnitude
    # print(positions)
    # positions = positions * sampling_amount
    positions = np.repeat(positions, sampling_amount)
    print(positions)
    print(min(positions))
    print(max(positions))
    t0 = time.perf_counter()
    axis.set_pos(1 + magnitude)
    for position in positions:
        while True:
            locations.append([time.perf_counter(), axis.get_pos(), 1 + magnitude + position])
            # print([time.perf_counter(), axis.get_pos(), 1 + magnitude + position])
            if (time.perf_counter() - t0 >= 1/command_frequency):
                break

        axis.set_pos(1 + magnitude + position)
    locations_list.append(locations)

for locations in locations_list:
    print("locations")
    # x = locations[0]
    x = [location[0] for location in locations]
    y = [location[1] for location in locations]
    y1 = [location[2] for location in locations]

    print(f"{x}, {y}, {y1}")

    p = figure(title="Frequency reponse", x_axis_label="hehe", y_axis_label="hihi")
    p.line(x, y, legend_label="actual locaitons")
    p.line(x,y1, legend_label="setposes")
    show(p)
    input("pp???")
