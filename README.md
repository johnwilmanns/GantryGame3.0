# GantryGame3.0

New code for the gantry game drawing machine. 

For future maintainers:

So you've decided to pick this project up, polish it off, and make it actually good??
Well you have signed yourself up for a helluva challange!

By my own admission this project is under documented and over complicated. I have left this file in the repo as my best hope of explaining it, but if you need anything feel free to contact either of the two maintainers at johnwilmanns@gmail.com or if you actually want help samir.beall@gmail.com, I might remember enough to help you. 

How the photo booth works (general overview):
It takes a photo, then runs a bunch of code to first make "edges" images containing single pixel white lines where the pen will draw. Most of this code is contained within image_processing.py and posturize.py. To make things harder on you, it also runs with multiprocessing, however that should be failry well figured out. 
After the photo is taken, the edges files are processed into "peices" / segments, which are displayed. These

Important functions/meathods/classes

Gantry.py:
Stores everything to do with the x/y motion

Axis: Very simliar to Odrive_ease_lib, look at that

image_processing: Uses cv2.canny and some other hatching algorithms in order to take an image and turn it into lines to give to trajectory planning

trajectory_planning: plannes trajectory based off an image with lines of a single pixel. Also has some stuff to keep track of how much a single pen has drawn

run_gantry: loops through the points from trajectory planning and moves the gantry to the next point

Posturize: uses hatching to create a depth effect, get_spinny needs to be refactored, but this is the current method. It uses angles to add depth.

How the motion works:
it uses odrive's position filtering mode. It feeds the odrive those points at the set frequency. Full path planning ensures that the accelration is constantn throughout the entire movement. This exports a list of coordinates that run_gantry uses to set_pos with filtered position control. The travel moves are done with trapazoidal trajectories to make sure that they are nice. 

# Basic Pipeline

1. Image is captured in one of three programs: draw_image.py (for testing), Picasso_Bot_Gui.py (single computer use), 
photo_booth.py/picasso_side_gui.py (Production use case, with camera and drawing machine client).

2. Image is converted into a set of primitive points by process_combo_raw() in image_processing.py. This takes the image, and converts it into edges, and then calculates a quick path between all of those points. Much of this work is done by the precompiled linux binary rust.so (other targets are availible in the binaries folder, but you may need to compile new ones yourself), which is a library that Samir wrote in order to make life harder for you. Much of the time consuming code that was bottlenecking our project was rewritten in rust, which the python code then calls. Points that do not add any information are discarded (tunable). All of these parameters are visible in draw_image.py, which will be very helpful if you need to tune them for any reason. The default values should be very good for a 1080p image.

3. The list of segments (A multidimensional array that represents a group of segments, which are a group of points. Each segments is a continuously drawn line)
is then processed by calc_path in trajectory_planning.py. This calculates the full path in how the gantry should move, by using a max turn radius, acceleration, and max velocity parameter. If you need to make the machine faster or slower, these values are where you should look.

4. The points are fed to the gantry at a constant rate with run_gantry.py, regardless of how you have processed the images. Hopefully it works!
