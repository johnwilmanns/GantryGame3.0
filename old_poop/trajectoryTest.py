import odrive
from odrive.enums import *
import ODrive_Ease_Lib
from ODrive_Ease_Lib import ODrive_Axis
import usb.core


xavier_serial = 20793595524
yannie_serial = 20673593524

dev = usb.core.find(find_all=1, idVendor=0x1209, idProduct=0x0d32)  # finds all usb devices
od = []

a = next(dev)
od.append(odrive.find_any('usb:%s:%s' % (a.bus, a.address)))  # looks for an odrive with address
a = next(dev)
od.append(odrive.find_any('usb:%s:%s' % (a.bus, a.address)))

if od[0].serial_number == xavier_serial:
    self._xavier = od[0]
    self._yannie = od[1]
else:
    self._xavier = od[1]
    self._yannie = od[0]

# _xavier_axis0 = ODrive_Ease_Lib.ODrive_Axis(_xavier.axis0)
# _xavier_axis1 = ODrive_Ease_Lib.ODrive_Axis(_xavier.axis1)
#
# _yannie_axis0 = ODrive_Ease_Lib.ODrive_Axis(_yannie.axis0)
# _yannie_axis1 = ODrive_Ease_Lib.ODrive_Axis(_yannie.axis1)
#
# _xavier.axis0.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
# _xavier.axis1.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
# _yannie.axis0.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
# #_yannie.axis1.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
#
# _yannie.clear_errors() #todo  we really should delete this
# _xavier.clear_errors()
#
# _xavier.axis0.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
# _xavier.axis1.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
# _yannie.axis0.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
# # _yannie.axis1.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION

ax = ODrive_Axis(_yannie.axis1)

#put all code into a try catch loop for Samir's enjoyment
while True:
    try:
        ax.calibrate()
        break
    except:
        _yannie.clear_errors() #todo  we really should delete this
        _xavier.clear_errors()
        print("it failed lmao")


while ax.get_pos() < 7:
    ax.set_pos(ax.get_pos() + .1)
