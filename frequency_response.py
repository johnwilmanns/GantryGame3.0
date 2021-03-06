import math

from gantry import Gantry
import numpy as np
import time
from bokeh.plotting import figure, show

frequency_low = 1
frequency_high = 30
test_numbers = 10  #the number of different frequencies it tests
sampling_amount = 10 #the number of times it tests each frequency
magnitude = .05
command_frequency = 120

bandwith = 15

gantry = Gantry()
gantry.startup()
axis = gantry.y
axis1 = gantry.y2
#y vals
axis.axis.controller.config.vel_gain = .5
axis.axis.controller.config.pos_gain = 40
axis.axis.controller.config.vel_integrator_gain = axis.axis.controller.config.vel_gain * .5 * bandwith

axis1.axis.controller.config.vel_gain = .5
axis1.axis.controller.config.pos_gain = 40
axis1.axis.controller.config.vel_integrator_gain = axis.axis.controller.config.vel_gain * .5 * bandwith
# #x vals
# axis.axis.controller.config.vel_gain = .15
# axis.axis.controller.config.pos_gain = 75
# axis.axis.controller.config.vel_integrator_gain = .13


axis.set_pos(1, ensure_control_mode= True)
time.sleep(1)
frequencies = np.geomspace(frequency_low, frequency_high, num = test_numbers) #gets a list of frequencies logarithmicly spaced
locations_list = []
for frequency in frequencies:
    locations = []
    positions = np.sin(np.arange(0, np.pi * 2 * sampling_amount, frequency * 1/command_frequency)) * magnitude
    # print(positions)

    # positions = np.repeat(positions, sampling_amount)
    # print(positions)
    # print(min(positions))
    # e = figure(title="heheheheheh")
    # e.line(range(len(positions)), positions)
    # show(e)
    # input("pp")
    # print(max(positions))
    t0 = time.perf_counter()
    axis.set_pos(1 + magnitude)

    for position in positions:
        locations.append([time.perf_counter(), axis.get_pos() - 1 - magnitude, position, axis.axis.motor.current_control.Iq_measured])
        while True:
            
            # print([time.perf_counter(), axis.get_pos(), 1 + magnitude + position])
            if (time.perf_counter() - t0 >= 1/command_frequency):
                
                
                
                break

        axis.set_pos(1 + magnitude + position)
        if axis1 != None:
            axis1.set_pos(1 + magnitude + position)
    locations_list.append(locations)
frequency_responses = []
print(len(locations_list))
for i, locations in enumerate(locations_list):

    # print("locations")
    x = [location[0] for location in locations]
    y = [location[1] for location in locations] #encoder position measurment
    y1 = [location[2] for location in locations] #requested position
    current = [location[3] for location in locations]

    # print(f"{x}, {y}, {y1}")

    p = figure(title=f"{frequencies[i]} hz", x_axis_label="hehe", y_axis_label="hihi")
    p.line(x, y, legend_label="actual locaitons")
    p.line(x,y1, legend_label="setposes", color="red")
    c = figure(title=f"{frequencies[i]} current", x_axis_label="hehe", y_axis_label="hihi")
    c.line(x, current, legend_label="current")

    # frequency_response = np.fft.fft(y)
    show(p)
    show(c)
    # print(frequency_response)
    # find rms of frequency response 
    # frequency_response = abs(frequency_response)
    frequency_response = math.sqrt(np.dot(y, y)) / len(y) / 2
    frequency_response_commanded = math.sqrt(np.dot(y1,y1)) / len(y1) / 2
    print(f"{frequency_response}, {frequency_response_commanded}")
    response = frequency_response / frequency_response_commanded
    print(response)
    frequency_responses.append(response)
    # input("pp???")


e = figure(title = "response", x_axis_type = "log", y_axis_type = "log")
e.line(frequencies, frequency_responses, legend_label = "response")
show(e)
input("hold")