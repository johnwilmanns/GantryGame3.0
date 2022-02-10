import gantry
gantry = gantry.Gantry()

for axis in gantry.axes():
    axis.idle()
    
import servo
# solenoid.pen_down()