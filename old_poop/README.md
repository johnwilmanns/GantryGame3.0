# GantryGame2.0

TL;DR ON RUNNING THE GANTRY GAME:

1) Turn on power.
2) Move to the directory ~/projects/GantryGame2.0. _(cd ~/projects/GantryGame2.0)_
3) Make sure the carriage (what holds the pen) is pushed to the back. Make sure both motors are pushed. Make sure the pen holder is empty.
4) Run main.py with _python3 main.py_.
5) Wait. Process should take about 30 seconds.
6) First, there will be about 12 seconds of silence. Then, the motors should undergo calibration. Each motor should move forward a
certain number of steps and move back. If one of them stops moving or is clicking, stop the program with Ctrl+c and see the Rebooting
the ODrive section.
7) After calibration, all motors should move to the top left corner, with the carriage moving downward.
8) After about 16 seconds, the motors will try to move to a center position. The carriage should be in the center of machine, both 
horizontally and vertically, and the pen holder should be raised up.
9) The tablet screen should be displaying the title "Gantry Game" and two buttons, Freehand and From File.

CONVERTING IMAGES:
Switch to computer branch

RUNNING FROM FILE
1) Click from file to get to a screen displaying four pictures. Should freeze up and take a while, this is normal (about 5 seconds)
2) Click on the two arrows to browse more images, or click an image to select it.
3) After landing on the pre-draw screen, you can click DRAW!. BEFORE YOU CLICK IT, READ THE SECTIONS 4, 5, and 6
4) Drawing can have a multitude of issues, each with different solutions. When the machine goes to retrieve a pen, make sure that the 
pen enters the carriage. Sometimes, it will get caught on the lip of the collet. Watch your hands, but you can manuever the pen into the
collet as the machine descends.
5) When the machine goes to return the pen, sometimes the force of the lid is not enough to stop the pen from being released, meaning after
the carriage moves up it is still holding the pen. In this case, just pull the pen down and into its position.
6) If an error occurs that would cause the breaking of a pen or the horizontal rail to go diagonal, THIS IS NOT INTENTIONAL AND THE PROGRAM
OR PI SHOULD BE STOPPED IMMEDIATELY.
7) Other than that, enjoy your drawing!

RUNNING FREEHAND
1) The right joystick will control the carriage, and the center button will lower the pen.
2) Pressing the white sqaure should take you a switching color screen. These buttons will be disabled for 8 seconds to prevent kids from 
messing with them, because of the problem outlined in next_tasks.txt
3) In short, this mode is a little broken. Please try to fix him!

If you want to add new images, check the branch marked computer.
