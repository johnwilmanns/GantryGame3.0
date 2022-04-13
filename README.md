# GantryGame3.0

New code for the gantry game drawing machine. 

For future maintainers:

How to use: 
Connect to Odrive and arduino
Put a file in
put the file name in main.py. run it

Important functions/meathods/classes

Gantry:
Stores everything to do with the x/y motion

Axis: Very simliar to Odrive_ease_lib, look at that

image_processing: Uses cv2.canny and some other hatching algorithms in order to take an image and turn it into lines to give to trajectory planning

trajectory_planning: plannes trajectory based off an image with lines of a single pixel. Also has some stuff to keep track of how much a single pen has drawn

run_gantry: loops through the points from trajectory planning and moves the gantry to the next point

Posturize: uses hatching to create a depth effect, get_spinny needs to be refactored, but this is the current method. It uses angles to add depth.

How the motion works:
it uses odrive's position filtering mode. It feeds the odrive those points at the set frequency. Full path planning ensures that the accelration is constantn throughout the entire movement. 