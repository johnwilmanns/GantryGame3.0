import ODrive_Ease_Lib
import odrive
import time
from odrive.utils import *

odrv1_serial = "20793595524B"  # Previously Xavier
odrv0_serial = "20673593524B"  # Previously Yannie

odrv1 = odrive.find_any(serial_number=odrv1_serial)
odrv0 = odrive.find_any(serial_number=odrv0_serial)

"""
odrv0.erase_configuration()
odrv1.erase_configuration()
"""
odrv0.axis0.motor.config.current_lim = 30
odrv0.axis1.motor.config.current_lim = 30

odrv0.axis0.controller.config.vel_limit = 20
odrv0.axis1.controller.config.vel_limit = 20


odrv0.axis0.controller.config.enable_overspeed_error = False
odrv0.axis1.controller.config.enable_overspeed_error = False

odrv0.config.enable_brake_resistor = True

odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
odrv0.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

odrv0.axis0.config.startup_encoder_offset_calibration = True
odrv0.axis1.config.startup_encoder_offset_calibration = True

odrv0.axis0.config.startup_closed_loop_control = True
odrv0.axis1.config.startup_closed_loop_control = True



odrv1.axis0.motor.config.current_lim = 30
odrv1.axis1.motor.config.current_lim = 30

odrv1.axis0.controller.config.vel_limit = 20
odrv1.axis1.controller.config.vel_limit = 20

odrv1.config.enable_brake_resistor = True

odrv1.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
odrv1.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

odrv1.axis0.config.startup_encoder_offset_calibration = True
odrv1.axis1.config.startup_encoder_offset_calibration = True

odrv1.axis0.config.startup_closed_loop_control = True
odrv1.axis1.config.startup_closed_loop_control = True

time.sleep(30)

try:
    odrv0.save_configuration()
except:
    pass

try:
    odrv1.save_configuration()
except:
    pass

