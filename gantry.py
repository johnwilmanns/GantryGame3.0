import ODrive_Ease_Lib
import odrive
import time
import math
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
        self.x_max_accel = 2
        self.y_max_accel = 2
        self.x_max_decel = 2
        self.y_max_decel = 2
        self.x_max_vel = 3
        self.y_max_vel = 3

    #todo these should really be stored in the ease lib axis, but I really don't feel like fixing that right now
    def set_max_accel(self, xmax, ymax):
        self.x_max_accel = xmax
        self.y_max_accel = ymax
    
    def set_max_decel(self, xmax, ymax):
        self.x_max_decel = xmax
        self.y_max_decel = ymax
    
    def set_max_vel(self, xmax, ymax):
        self.x_max_vel = xmax
        self.y_max_vel = ymax

    #todo, add assert statments
    def startup(self):
        self.clear_errors()
        self.calibrate()
        self.sensorless_home()
        self.print_positions()
        self.dump_errors()


    def __del__(self):
        print("setting all states to idle")
        self.x.idle()
        self.y.idle()
        self.z.idle()
        dump_errors()

    def axes(self):
        yield self.x
        yield self.y
        yield self.z


    def calibrate(self):
        for motor in self.axes():
            motor.calibrate_encoder()
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
        self.requested_pos = [0, 0]

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
            print(f"waiting: {x}, {y}, {z}")
            if abs(self.x.get_pos() - x) <= .1 or x == -1:
                if abs(self.x.get_pos() - y) <= .1 or y == -1:
                    if abs(self.x.get_pos() - z) <= .1 or z == -1:
                        self.requested_pos = [x, y]
                        return

    def mirror_move(self, new_x, new_y):
        ratio = new_x - self.x.get_pos() / new_y - self.y.get_pos()
        print(ratio)
        #y is the dominant axis
        self.x.mirror_sub(self.y.axis, ratio)
        self.y.set_pos(new_y)


    def trap_move(self, new_x, new_y):

        # the ratio is the x to the y movement distance

        ratio = abs(new_x - self.x.get_pos() / new_y - self.y.get_pos())
        print(ratio)
        x_accel = self.x_max_accel
        y_accel = x_accel / ratio

        if y_accel > self.y_max_accel:
            y_accel = self.y_max_accel
            x_accel = y_accel * ratio

        x_decel = self.x_max_decel
        y_decel = x_decel / ratio

        if y_decel > self.y_max_decel:
            y_decel = self.y_max_decel
            x_decel = y_decel * ratio

        x_vel = self.x_max_vel
        y_vel = x_vel / ratio

        if y_vel > self.y_max_vel:
            y_vel = self.y_max_vel
            x_vel = y_vel * ratio

        self.x.set_pos_traj(new_x, x_vel, x_accel, x_decel)
        print(f"x: {x_vel, x_accel, x_decel}")
        self.y.set_pos_traj(new_x, y_vel, y_accel, y_decel)
        print(f"y: {y_vel, y_accel, y_decel}")
























        # compares to see if it should be limited by x or y
        # the reason we have to have this so many times is because we have to compare each one individually, isn't that fun.

        if ratio > self.x_max_vel / self.y_max_vel:
            x_vel = self.y_max_vel / ratio
            y_vel = self.y_max_vel
        else:
            y_vel = self.x_max_vel * ratio
            x_vel = self.x_max_vel

        if ratio > self.x_max_accel / self.y_max_accel:
            x_accel = self.y_max_accel / ratio
            y_accel = self.y_max_accel
        else:
            y_accel = self.x_max_accel * ratio
            x_accel = self.x_max_accel

        if ratio > self.x_max_decel / self.y_max_decel:
            x_decel = self.y_max_decel / ratio
            y_decel = self.y_max_decel
        else:
            y_decel = self.x_max_decel * ratio
            x_decel = self.x_max_decel

        self.x.set_pos_traj(new_x, x_vel, x_accel, x_decel)
        self.y.set_pos_traj(new_x, y_vel, y_accel, y_decel)


    def set_pos_noblock(self, x = -1, y = -1, z = -1):

        if(x != -1):
            self.x.set_pos(x)

        if y != -1:
            self.y.set_pos(y)

        if z != -1:
            self.z.set_pos(z)

        self.requested_pos = [x, y]




        
        

