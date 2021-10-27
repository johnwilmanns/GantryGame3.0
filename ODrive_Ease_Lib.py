#import time

import odrive
import usb.core
from odrive.enums import *


def find_ODrives():
    dev = usb.core.find(find_all=1, idVendor=0x1209, idProduct=0x0d32)
    od = []
    try:
        while True:
            a = next(dev)
            od.append(odrive.find_any('usb:%s:%s' % (a.bus, a.address)))
            print('added')
    except:
        pass
    return od


def reboot_ODrive(od):
    try:
        od.reboot()
        print("rebooted")
    except:
        print('it threw an error????')

class Axis(object):
    def __init__(self, axis):
        self.axis = axis
        self.zero = 0

    #odrive control methods

    def set_pos(self, pos):
        desired_pos = pos + self.zero
        if self.axis.current_state != 8:
            self.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        if self.axis.controller.config.control_mode != 3:
            self.axis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
        self.axis.controller.input_pos = desired_pos

    def set_vel(self, vel):
        if self.axis.current_state != 8:
            self.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        if self.axis.controller.config.control_mode != 2:
            self.axis.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
        self.axis.controller.input_vel = vel

    def set_torque(self, torque):
        if self.axis.requested_state != 8:
            self.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        if self.axis.controller.config.control_mode != 1:
            self.axis.controller.config.control_mode = CONTROL_MODE_TORQUE_CONTROL
        self.axis.controller.input_torque = torque

    #get info about current state of odrive

    def get_pos(self):
        return self.axis.encoder.pos_estimate - self.zero

    def get_vel(self):
        return self.axis.encoder.vel_estimate

    #calibration meathods
    def calibrate(self):
        self.axis.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        start = time.time()
        while self.axis.current_state != AXIS_STATE_IDLE:
            time.sleep(0.1)
            if time.time() - start > 15:
                print("could not calibrate, try rebooting odrive")
                return False

    def calibrate_no_hold(self):
        self.axis.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

    def hold_until_calibrated(self):  # use with calibrate no hold to do all 3 axis at once
        start = time.time()
        while self.axis.current_state != AXIS_STATE_IDLE:
            time.sleep(0.1)
            if time.time() - start > 15:
                print("could not calibrate, try rebooting odrive")
                return False

    #misc utilities, lots of stuff for homing

    def hold_until_stopped(self, velocity_threshold = .05):
        while self.get_vel() > threshold:
            pass

    def velocity_home(self, vel = 1, ):
        print("homing")
        print(f"Current Limit: {self.get_curr_limit()}")

        self.set_vel(vel)
        time.sleep(3)

        while True:

            time.sleep(.5)
            vel = self.get_vel()

            # print(f"Current: {self.get_curr_B()}, {self.get_curr_C()}")
            # print(vel)

            if vel < .2:
                break

        def home_with_endstop(self, vel, offset, min_gpio_num):
            self.axis.controller.config.homing_speed = vel  # flip sign to turn CW or CCW
            self.axis.min_endstop.config.gpio_num = min_gpio_num
            self.axis.min_endstop.config.offset = offset
            self.axis.min_endstop.config.enabled = True

    def home_with_endstop(self, min_gpio_num, offset):
        self.axis.error = 0
        self.axis.min_endstop.config.enabled = False

    def is_calibrated(self):
        return self.axis.motor.is_calibrated

    #setting odrive values

    def set_vel_limit(self, vel):
        self.axis.controller.config.vel_limit = vel

    def set_current_limit(self, val):
        self.axis.motor.config.current_lim = val

    def set_home(self):
        self.zero = self.get_raw_pos()

    def set_calibration_current(self, current):
        self.axis.motor.config.calibration_current = current

