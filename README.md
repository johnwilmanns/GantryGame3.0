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

Full face processing: basically feeds cv2.canny and posturize into full path planning

Posturize: uses hatching to create a depth effect, get_spinny needs to be refactored, but this is the current method. It uses angles to add depth.

Full path planning: uses calc_arc, this is very complicated, if this has broken ur screwed, go back to using trap_trajectory ig. 

How the motion works:
it uses odrive's position filtering mode. It feeds the odrive those points at the set frequency. Full path planning ensures that the accelration is constantn throughout the entire movement. 