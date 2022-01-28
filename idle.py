import gantry
gantry = gantry.Gantry()

for axis in gantry.axes():
    axis.idle()
    
import solenoid
solenoid.pen_down()