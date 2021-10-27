import odrive
from odrive.enums import *
from odrive.utils import start_liveplotter
import time
import numpy

# print(numpy.array(["poop"]))

import os
print("PYTHONPATH:", os.environ.get('PYTHONPATH'))
print("PATH:", os.environ.get('PATH'))

odrv0_serial = "20793595524B"  # Previously Xavier
odrv1_serial = "20673593524B"  # Previously Yannie



odrv0 = odrive.find_any(serial_number=odrv0_serial)
odrv1 = odrive.find_any(serial_number=odrv1_serial)

axis = odrv1.axis1


start_liveplotter(lambda:[axis.encoder.pos_estimate, axis.controller.pos_setpoint])

while True:
    time.sleep(1)
    print("poop!")
#
# axis.requested_state =  AXIS_STATE_FULL_CALIBRATION_SEQUENCE
#
# while axis.current_state != AXIS_STATE_IDLE:
#     pass

# start_liveplotter(lambda:[odrv0.axis0.encoder.pos_estimate, odrv0.axis0.controller.pos_setpoint])

print("done!")



