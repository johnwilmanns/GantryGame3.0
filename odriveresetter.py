import ODrive_Ease_Lib
import odrive
import time
from odrive.utils import *
print("imported odrive resetter")

odrv1_serial = "20793595524B"  # Previously Xavier #actually Y
odrv0_serial = "20673593524B"  # Previously Yannie #actually x

odrv1 = odrive.find_any(serial_number=odrv1_serial)
odrv0 = odrive.find_any(serial_number=odrv0_serial)





"""
odrv0.erase_configuration()
odrv1.erase_configuration()
"""


odrv0.axis1.controller.config.vel_gain = .15
odrv0.axis1.controller.config.pos_gain = 75
odrv0.axis1.controller.config.vel_integrator_gain = .13

"""
Y motor thingis
"""

odrv1.axis0.controller.config.vel_gain = .25
odrv1.axis0.controller.config.pos_gain = 35
odrv1.axis0.controller.config.vel_integrator_gain = 1.9

odrv1.axis1.controller.config.vel_gain = .25
odrv1.axis1.controller.config.pos_gain = 35
odrv1.axis1.controller.config.vel_integrator_gain = 1.9




odrv0.axis0.motor.config.current_lim = 0
odrv0.axis1.motor.config.current_lim = 30

odrv0.axis0.controller.config.vel_limit = 2000
odrv0.axis1.controller.config.vel_limit = 2000

odrv1.axis0.controller.config.vel_limit = 2000
odrv1.axis1.controller.config.vel_limit = 2000



odrv0.axis0.controller.config.enable_overspeed_error = False
odrv0.axis1.controller.config.enable_overspeed_error = False
odrv1.axis0.controller.config.enable_overspeed_error = False
odrv1.axis1.controller.config.enable_overspeed_error = False

odrv0.config.enable_brake_resistor = True
odrv1.config.enable_brake_resistor = True

# odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
# odrv0.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

odrv0.axis0.config.startup_encoder_offset_calibration = False
odrv0.axis1.config.startup_encoder_offset_calibration = False

odrv0.axis0.encoder.config.use_index = True
odrv0.axis1.encoder.config.use_index = True
odrv1.axis0.encoder.config.use_index = True
odrv1.axis1.encoder.config.use_index = True


odrv0.axis0.config.startup_closed_loop_control = False
odrv0.axis1.config.startup_closed_loop_control = False

odrv0.axis1.motor.config.current_control_bandwidth = 120
odrv1.axis0.motor.config.current_control_bandwidth = 120
odrv1.axis1.motor.config.current_control_bandwidth = 120

odrv1.axis0.motor.config.requested_current_range = 60
odrv1.axis1.motor.config.requested_current_range = 60

# odrv1.axis0.motor.config.calibration_current = 20
# odrv1.axis1.motor.config.calibration_current = 20

# odrv1.axis0.motor.config.current_lim = 30
# odrv1.axis1.motor.config.current_lim = 30

# odrv1.axis0.controller.config.vel_limit = 200
# odrv1.axis1.controller.config.vel_limit = 200

# odrv1.axis0.controller.config.enable_overspeed_error = False
# odrv1.axis1.controller.config.enable_overspeed_error = False

# odrv1.config.enable_brake_resistor = True

# # odrv1.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
# # odrv1.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

# odrv1.axis0.config.startup_encoder_offset_calibration = False
# odrv1.axis1.config.startup_encoder_offset_calibration = False

# odrv1.axis0.config.startup_closed_loop_control = False
# odrv1.axis1.config.startup_closed_loop_control = False

# time.sleep(1)



# # STARTUP SEQUENCE

# odrv0.axis1.encoder.config.use_index = True
# odrv1.axis0.encoder.config.use_index = True
# odrv1.axis1.encoder.config.use_index = True

# # run full state calibration for all axes
# odrv0.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
# odrv1.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
# time.sleep(20)
# odrv1.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
# time.sleep(20)
# print("finished cal")


# print(odrv0.axis1.encoder.is_ready)
# print(odrv1.axis0.encoder.is_ready)
# print(odrv1.axis1.encoder.is_ready)

# odrv0.axis1.encoder.config.pre_calibrated = True
# odrv1.axis0.encoder.config.pre_calibrated = True
# odrv1.axis1.encoder.config.pre_calibrated = True

# odrv0.axis1.motor.config.pre_calibrated = True
# odrv1.axis0.motor.config.pre_calibrated = True
# odrv1.axis1.motor.config.pre_calibrated = True



# try:
#     odrv0.save_configuration()
# except Exception as e:
#     # pass
#     print(e)

# try:
#     odrv1.save_configuration()
# except Exception as e:
#     # pass
#     print(e)

# print("Done")