import odrive
from odrive.enums import *
from odrive.utils import start_liveplotter
import time
import numpy


odrv0_serial = "20793595524B"  # Previously Xavier
odrv1_serial = "20673593524B"  # Previously Yannie


odrv0 = odrive.find_any(serial_number=odrv0_serial)
odrv1 = odrive.find_any(serial_number=odrv1_serial)

axis = odrv1.axis1

def move(dist = 5):
    axis.controller.input_pos = 0
    time.sleep(5)

    axis.controller.input_po = dist
    time.sleep(5)

start_liveplotter(lambda:[axis.encoder.pos_estimate, axis.controller.pos_setpoint])


axis.requested_state =  AXIS_STATE_FULL_CALIBRATION_SEQUENCE

while axis.current_state != AXIS_STATE_IDLE:
    pass

axis.controller.config.vel_limit = 20
axis.controller.config.enable_overspeed_error = False

axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
axis.controller.control_mode = CONTROL_MODE_POSITION_CONTROL

while True:
    print(f"""
    vel_gain (vg) = {axis.controller.config.vel_gain}\n
    pos_gain (pg) = {axis.controller.config.pos_gain}\n
    vel_integrator_gain (vig) = {axis.controller.config.vel_integrator_gain}\n""")

    text = input()

    try:

        if text == "default":
            axis.controller.config.vel_gain = 20
            axis.controller.config.pos_gain = .16
            axis.controller.config.vel_integrator_gain = .32

        elif text == "move":
            move()
            
        else:
            target, val = text.split("=")
            val = int(val)

            if target == "vg":
                axis.controller.config.vel_gain = val
            elif target == "pg":
                axis.controller.config.pos_gain = val
            elif target == "vig":
                axis.controller.config.vel_integrator_gain = val
            

        
    except Exception as e:
        print(f"ERROR: {e}")

    

# odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
# odrv0.axis0.motor.config.pre_calibrated = True
# odrv0.axis0.config.startup_encoder_offset_calibration = True
# odrv0.axis0.config.startup_closed_loop_control = True
# odrv0.save_configuration()
# odrv0.reboot()





# start_liveplotter(lambda:[odrv0.axis0.encoder.pos_estimate, odrv0.axis0.controller.pos_setpoint])

print("done!")



