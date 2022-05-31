# GantryGame3.0

New code for the gantry game drawing machine. 

For future maintainers:

So you've decided to pick this project up, polish it off, and make it actually good??
Well you have signed yourself up for a helluva challange!

By my own admission this project is under documented and over complicated. I have left this file in the repo as my best hope of explaining it, but if you need anything feel free to contact me at johnwilmanns@gmail.com, I might remember enough to help you.


How the photo booth works (general overview):
It takes a photo, then runs a bunch of code to first make "edges" images containing single pixel white lines where the pen will draw. Most of this code is contained within image_processing.py and posturize.py. To make things harder on you, it also runs with multiprocessing, however that should be failry well figured out. 
After the photo is taken, the edges files are processed into "peices" / segments, which are displayed. These

Important functions/meathods/classes

Gantry:
Stores everything to do with the x/y motion

Axis: Very simliar to Odrive_ease_lib, look at that

image_processing: Uses cv2.canny and some other hatching algorithms in order to take an image and turn it into lines to give to trajectory planning

trajectory_planning: plannes trajectory based off an image with lines of a single pixel. Also has some stuff to keep track of how much a single pen has drawn

run_gantry: loops through the points from trajectory planning and moves the gantry to the next point

Posturize: uses hatching to create a depth effect, get_spinny needs to be refactored, but this is the current method. It uses angles to add depth.

How the motion works:
it uses odrive's position filtering mode. It feeds the odrive those points at the set frequency. Full path planning ensures that the accelration is constantn throughout the entire movement. This exports a list of coordinates that run_gantry uses to set_pos with filtered position control. The travel moves are done with trapazoidal trajectories to make sure that they are nice. 

How 2 run:
