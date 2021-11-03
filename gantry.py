import ODrive_Ease_Lib
import odrive
import time
from odrive.utils import *
class Gantry:

    def __init__(self):

        self.odrv1_serial = "20793595524B" # Previously Xavier
        self.odrv0_serial = "20673593524B" # Previously Yannie


        self.odrv1 = odrive.find_any(serial_number=self.odrv1_serial)
        self.odrv0 = odrive.find_any(serial_number=self.odrv0_serial)

        self.clear_errors()

        self.x = ODrive_Ease_Lib.Axis(self.odrv0.axis1) # X
        self.y = ODrive_Ease_Lib.Axis(self.odrv1.axis0) # Y
        self.z = ODrive_Ease_Lib.Axis(self.odrv1.axis1) # Z

    def startup(self):
        self.calibrate()
        self.sensorless_home()
        self.print_positions()
        self.dump_errors()


    def __del__(self):
        print("setting all states to idle")
        self.x.idle()
        self.y.idle()
        self.z.idle()

    def axes(self):
        yield self.x
        yield self.y
        yield self.z


    def calibrate(self):
        for motor in self.axes():
            motor.calibrate_no_hold()
        for motor in self.axes():
            motor.hold_until_calibrated()
        print("calibrated")

    def home(self, axis=[True, True, True]):
        print("homing")
        if axis[0]:  # x axis
            self.x.set_vel(-1)
            while True:
                print(self.odrv0.get_gpio_states() & 0b00100)
                if self.odrv0.get_gpio_states() & 0b00100 == 0:  # needs to be changed upon rewire

                    self.x.set_vel(0)
                    self.x.set_home()
                    print("yes")
                    break
                time.sleep(.1)



        print("homed x")

        if axis[1]:  # axis
            self.y.set_vel(1)
            while True:
                print(self.odrv1.get_gpio_states() & 0b00100)
                if self.odrv1.get_gpio_states() & 0b00100 == 0:  # needs to be changed upon rewire

                    self.x.set_vel(0)
                    self.x.set_home()
                    print("yes")
                    break
                time.sleep(.1)

    def sensorless_home(self, home_axes = [True, True, True]):
        for num, axis in enumerate(self.axes()) :
            if home_axes[num]:
                axis.scuffed_home()

    def dump_errors(self):
        print(dump_errors(self.odrv0))
        print(dump_errors(self.odrv1))

    def clear_errors(self):
        self.odrv0.clear_errors()
        self.odrv1.clear_errors()

    def print_positions(self):
        print(f"X = {self.x}")
        print(f"Y = {self.y}")
        print(f"Z = {self.z}")

    def set_pos(self, x = -1, y = -1, z = -1):
        
        if(x != -1):
            self.x.set_pos(x)
        
        if y != -1:
            self.y.set_pos(y)
        
        if z != -1:
            self.z.set_pos(z)

        while True:
            if abs(self.x.get_pos() - x) <= .05 or x == -1:
                if abs(self.x.get_pos() - y) <= .05 or y == -1:
                    if abs(self.x.get_pos() - z) <= .05 or z == -1:
                        return

    def set_pos_noblock(self, x = -1, y = -1, z = -1):

        if(x != -1):
            self.x.set_pos(x)

        if y != -1:
            self.y.set_pos(y)

        if z != -1:
            self.z.set_pos(z)




        
        

