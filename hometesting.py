import odrive
from odrive.enums import *
from odrive.utils import *
import time
import ODrive_Ease_Lib
from ODrive_Ease_Lib import Axis

odrv0_serial = "20793595524B"  # Previously Xavier
odrv1_serial = "20673593524B"  # Previously Yannie


print("e")
odrv0 = odrive.find_any(serial_number=odrv0_serial)
odrv1 = odrive.find_any(serial_number=odrv1_serial)
print("r")
y = Axis(odrv1.axis1, 1)
y.clear_errors()
odrv1.clear_errors()
print("du hek")
y.calibrate_encoder()
y.hold_until_calibrated()
dump_errors(odrv1)
# y.set_vel(1)
dump_errors(odrv1)
# time.sleep(4)
y.sensored_home()
dump_errors(odrv1)
y.set_pos(-1)
dump_errors(odrv1)
y.idle()
