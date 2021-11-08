import time

import odrive
import usb.core
from odrive.enums import *
from odrive.utils import *


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
    def __init__(self, axis, endstop_pin = None):
        self.axis = axis
        self.home = 0
        self.endstop_pin = endstop_pin

    #odrive control methods

    def set_pos(self, pos):
        desired_pos = pos + self.home
        if self.axis.requested_state != 8:
            self.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        if self.axis.controller.config.control_mode != 3:
            self.axis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
        self.axis.controller.input_pos = desired_pos

    def set_relative_pos(self, pos):
        self.set_raw_pos(pos + self.get_raw_pos())

    def get_raw_pos(self):
        return self.axis.encoder.pos_estimate

    def set_raw_pos(self, pos):
        if self.axis.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
            self.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.axis.controller.config.input_mode = INPUT_MODE_PASSTHROUGH
        self.axis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL

        self.axis.controller.input_pos = pos



    def set_pos_traj(self, pos, accel, vel, decel, inertia=0):
        # BUG: trajectory control not working when invoked after a velocity control, this line is used to
        # uselessly revert back to position control

        assert accel >= 0 and vel >= 0 and decel >= 0 and inertia >= 0, "Values must be positive"
        self.set_relative_pos(0)
        self.axis.trap_traj.config.accel_limit = accel
        self.axis.trap_traj.config.vel_limit = vel
        self.axis.trap_traj.config.decel_limit = decel
        if inertia != 0:
            self.axis.controller.config.inertia = inertia

        if self.axis.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
            self.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.axis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
        self.axis.controller.config.input_mode = INPUT_MODE_TRAP_TRAJ
        self.axis.controller.input_pos = pos + self.home

    def set_vel(self, vel):
        if self.axis.requested_state != 8:
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
        return self.axis.encoder.pos_estimate - self.home

    def get_raw_pos(self):
        return self.axis.encoder.pos_estimate

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

    def calibrate_encoder(self):
        if not self.axis.encoder.is_ready:
            self.axis.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION

    def calibrate_no_hold(self):
        self.axis.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

    def mirror_sub(self, axis, ratio):
        self.axis.controller.config.input_mode = INPUT_MODE_MIRROR
        self.axis.controller.config.axis_to_mirror = axis
        self.axis.controller.config.mirror_ratio = ratio


    def hold_until_calibrated(self):  # use with calibrate no hold to do all 3 axis at once
        start = time.time()
        while self.axis.current_state != AXIS_STATE_IDLE:
            time.sleep(0.1)
            if time.time() - start > 15:
                print("could not calibrate, try rebooting odrive")
                return False

    #misc utilities, lots of stuff for homing

    def hold_until_stopped(self, velocity_threshold = .05):
        while self.get_vel() > velocity_threshold:
            pass

    def sensorless_home(self, vel = 1):
        print("homing")
        vel *= -1
        # print(f"Current Limit: {self.get_curr_limit()}")

        self.set_vel(vel)
        time.sleep(3)

        while True:

            time.sleep(.5)
            vel = self.get_vel()

            # print(f"Current: {self.get_curr_B()}, {self.get_curr_C()}")
            # print(vel)

            if vel < .2:
                break
        self.set_home()
        self.set_pos(.2)
        print("homed" + str(type(self.axis)))

    def scuffed_home(self, current = .3, direction = 1):
        assert direction == 1 or direction == -1
        print("homing")
        oldvel = self.get_vel_limit()

        self.set_torque(current * direction * -1)
        print("pee")
        while True:
            print("pooping early")
            self.set_home()
            time.sleep(1)
            print("pooping")


            if abs(self.get_pos()) <= .05:
                print("pooped")
                self.set_torque(0)
                self.set_vel_limit(oldvel)
                return


    def extremely_scuffed_home(self, direction = 1):
        assert direction == 1 or direction == -1
        print("bathroom break!")
        oldvel = self.get_vel_limit()
        self.set_vel_limit(4)
        print("pee")
        while True:
            print("pooping early")
            self.set_home()
            self.set_pos(-10)
            time.sleep(1)
            print("pooping")


            if abs(self.get_pos()) <= .05:
                print("almost done pooping")
                self.set_torque(0)
                self.set_vel_limit(oldvel)
                self.idle()
                print("pooped")
                return
                print("forbidden poop")


    def check_status(self):
        assert self.axis.encoder.is_ready and self.axis.motor.is_calibrated


    def clear_errors(self):
        self.axis.error = 0
        self.axis.encoder.error = 0
        self.axis.motor.error = 0
        self.axis.controller.error = 0

    def sensored_home(self, vel = 1, offset = -.25, dir = 1, endstop_pin = None):

        if endstop_pin == None:
            endstop_pin = self.endstop_pin
        if endstop_pin == None:
            raise Exception("you have to set the gpio pin 4hedius")
        self.axis.controller.config.homing_speed = vel * dir
        self.axis.min_endstop.config.gpio_num = endstop_pin
        self.axis.min_endstop.config.offset = offset
        self.axis.min_endstop.config.enabled = True
        self.axis.requested_state = AXIS_STATE_HOMING
        time.sleep(1)
        self.hold_until_stopped()
        self.set_home()
        self.axis.error = 0
        self.axis.min_endstop.config.enabled = False
        print("homed")


    def is_calibrated(self):
        return self.axis.motor.is_calibrated

    def idle(self):
        self.axis.requested_state = 1

    #liveplotter stuff

    def start_pos_liveplotter(self):
        start_liveplotter(lambda: [self.axis.encoder.pos_estimate, self.axis.controller.pos_setpoint])


    #setting odrive values

    def set_vel_limit(self, vel):
        self.axis.controller.config.vel_limit = vel

    def get_vel_limit(self):
        return self.axis.controller.config.vel_limit


    def get_current_limit(self):
        return self.axis.controller.config.vel_limit

    def set_current_limit(self, val):
        self.axis.motor.config.current_lim = val

    def get_current_limit(self):
        return self.axis.motor.config.current_lim

    def set_trap_vals(self, vel_limit, accel_limit, decel_limit, inertia = -1):

        self.axis.trap_traj.config.vel_limit = vel_limit
        self.axis.trap_traj.config.accel_limit = accel_limit
        self.axis.trap_traj.config.decel_limit = decel_limit
        if inertia != -1:
            self.axis.controller.config.inertia = inertia


    def set_home(self):
        self.home = self.get_raw_pos()

    def set_calibration_current(self, current):
        self.axis.motor.config.calibration_current = current

    def set_endstop_pin(self, pin):
        self.enstop_pin = pin
