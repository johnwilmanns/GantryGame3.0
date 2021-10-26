import time

import odrive
import usb.core
from odrive.enums import *


# Used to make using the ODrive easier Version 0.5.3
# Last update October 6 2021 by John Wilmanns

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


# Reboots a singular odrive. You will need to reconnect to it in your code after rebooting
def reboot_ODrive(od):
    try:
        od.reboot()
    except:
        print('rebooted')


def generic_startup(home=False, home_vel=2,
                    home_dir=1):  # starts an odrive axis, calibrates it etc. Use as a guide, would not reccomend deploying rn as it only does one axis and will receive some functionallity updates in the near future. #todo: add second axis and fix returns

    od = odrive.find_any()
    od.axis1.motor.config.current_lim = 20
    od.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

    time.sleep(10)

    ax = ODrive_Axis(od.axis1)

    print("calibrating")
    ax.calibrate_encoder()

    od.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    od.axis1.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL

    if home:
        ax.home_with_vel(home_vel, home_dir)

    return ax, od


class ODrive_Axis(object):

    def __init__(self, axis, vel_lim=20000):
        self.axis = axis
        self.zero = 0
        self.axis.controller.config.vel_limit = vel_lim
        self.busy_lim = 500

    # enters full calibration sequence
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

    # enters encoder offset calibration
    def calibrate_encoder(self):
        self.axis.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
        start = time.time()
        while self.axis.current_state != AXIS_STATE_IDLE:
            time.sleep(0.1)
            if time.time() - start > 15:
                print("could not calibrate, try rebooting odrive")
                return False

    # checks if the motor is claibrated and the encoder is ready
    def is_calibrated(self):
        return self.axis.motor.is_calibrated and self.axis.encoder.is_ready

    # sets the motor to a specified velocity. Does not go over the velocity limit
    def set_vel(self, vel):
        if self.axis.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
            self.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        if self.axis.controller.config.control_mode != CONTROL_MODE_VELOCITY_CONTROL:
            self.axis.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
        self.axis.controller.input_vel = vel

    # sets the motor's velocity limit. Default is 20000
    def set_vel_limit(self, vel):
        self.axis.controller.config.vel_limit = vel

    # returns the velocity limit
    def get_vel_limit(self):
        return self.axis.controller.config.vel_limit

    # sets the zero (home pos) to the specified position
    def set_zero(self, pos):
        self.zero = pos

    # sets the zero to the current_position
    def set_home(self):
        self.zero = self.get_raw_pos()

    # returns the current position relative to the home
    def get_pos(self):
        return self.axis.encoder.pos_estimate - self.zero

    # returns the current position directly from the encoder
    def get_raw_pos(self):
        return self.axis.encoder.pos_estimate

    # sets the desired position
    def set_pos(self, pos):
        print(f"poopee: {pos}")
        desired_pos = pos + self.zero
        if self.axis.requested_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
            self.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        if self.axis.controller.config.control_mode != CONTROL_MODE_POSITION_CONTROL:
            self.axis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
        self.axis.controller.input_pos = desired_pos

    # TODO: Implement Trajectory Control
    # sets position using the trajectory control mode
    def set_pos_trap(self, pos):
        self.set_pos(pos)

    # sets the current limit
    def set_curr_limit(self, val):
        self.axis.motor.config.current_lim = val

    def set_current_limit(self, val):
        self.axis.motor.config.current_lim = val

    # returns the current limit
    def get_curr_limit(self):
        return self.axis.motor.config.current_lim

    # sets the current sent to the motor
    def set_current(self, curr):  # is now torque control
        if self.axis.requested_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
            self.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        if self.axis.controller.config.control_mode != CONTROL_MODE_TORQUE_CONTROL:
            self.axis.controller.config.control_mode = CONTROL_MODE_TORQUE_CONTROL
        self.axis.controller.input_torque = curr

    # added this for correctness, left old name for legacy support
    def set_torque(self, torque):
        set_current(self, torque)

    # returns the velocity measured from the encoder
    def get_vel(self):
        return self.axis.encoder.vel_estimate

    # Sets the position gain value
    def set_pos_gain(self, val):
        self.axis.controller.config.pos_gain = val

    # returns the position gain value
    def get_pos_gain(self):
        return self.axis.controller.config.pos_gain

    # sets the velocity proportional gain value
    def set_vel_gain(self, val):
        self.axis.controller.config.vel_gain = val

    # returns the velocity proportional gain value
    def get_vel_gain(self):
        return self.axis.controller.config.vel_gain

    # sets the velocity integrator gain value. Usually this is 0
    def set_vel_integrator_gain(self, val):
        self.axis.controller.config.vel_integrator_gain = val

    # returns the velocity integrator gain value. Usually this is 0
    def get_vel_integrator_gain(self):
        return self.axis.controller.config.vel_integrator_gain

    # checks if the motor is moving. Need to use a threshold speed. by default it is 500 counts/second
    # this can be set during initialization of ODrive_Axis object, through later setting of the busy_lim, or through a parameter to the is_busy method
    def is_busy(self, speed=-1):
        if speed == -1:
            speed = self.busy_lim
        if (abs(self.get_vel())) > speed:
            return True
        else:
            return False

    # sets the current allowed during the calibration sequence. Higher currents are needed when the motor encounters more resistence to motion
    def set_calibration_current(self, curr):
        self.axis.motor.config.calibration_current = curr

    # returns the allowed calibraiton current. By default it is 5 amps (3 phase not DC)
    def get_calibration_current(self):
        return self.axis.motor.config.calibration_current

    # method to home ODrive using where the chassis is mechanically stopped
    # length is expected length of the track the ODrive takes
    # set length to -1 if you do not want the ODrive to check its homing
    # direction = 1 or -1 depending on which side of the track you want home to be at
    # use direction = 1 if you want the track to be of only positive location values
    def home(self, current1, current2, length=-1, direction=1):
        self.set_current(current1 * -1 * direction)
        print('here')
        time.sleep(1)
        print('there')
        while self.is_busy():
            pass

        time.sleep(1)

        self.set_zero(self.get_raw_pos())
        print(self.get_pos())

        time.sleep(1)

        if not length == -1:
            self.set_current(current2 * 1 * direction)
            time.sleep(1)
            while self.is_busy():
                pass

            # end pos should be length
            if abs(self.get_pos() - length) > 50:
                print('ODrive could not home correctly')
                # maybe throw a more formal error here
                return False

        self.set_pos(0)
        print('ODrive homed correctly')
        return True

    # homes the motor by having it move towards one side with a constant velocity. Once it can no longer move, it considers this its home
    # The direction can be specified either by the sign of the velocty passed in or through the direction parameter
    # If the length of the track is known, it can be passed in. If this is done, after moving to one side, the motor will move to the other to find if the homing was successful.
    def home_with_vel(self, vel=.5, length=-1, direction=1):
        self.set_vel(vel * -1 * direction)
        print('here')
        time.sleep(1)
        print('there')
        while self.is_busy():
            pass

        time.sleep(1)

        self.set_zero(self.get_raw_pos())
        print(self.get_pos())

        time.sleep(1)

        if not length == -1:
            self.set_vel(vel * 1 * direction)
            time.sleep(1)
            while self.is_busy():
                pass

            print(self.get_pos())

            # end pos should be length
            if abs(self.get_pos() - length) > 50:
                print('ODrive could not home correctly')
                # maybe throw a more formal error here
                return False

        print('ODrive homed correctly')
        return True

    # only use with Wetmelon's endstop firmware
    def home_with_endstops(self, vel):
        self.axis.min_endstop.config.enabled = True
        self.axis.max_endstop.config.enabled = True
        self.set_vel(vel)
        while (self.axis.error == 0):
            pass
        if self.axis.error == 0x800 or self.axis.error == 0x1000:
            self.set_zero(self.get_raw_pos())
            self.axis.error = 0

        self.axis.min_endstop.config.enabled = False
        self.axis.max_endstop.config.enabled = False

    # basically just runs into the wall for a set number of seconds, seems to be the most consistant
    def scuffed_home(self, vel = 1):
        print("homing")
        print(f"Current Limit: {self.get_curr_limit()}")

        self.set_vel(vel)
        time.sleep(3)

        while True:

            time.sleep(.5)
            vel = self.get_vel()

            print(f"Current: {self.get_curr_B()}, {self.get_curr_C()}")
            print(vel)

            if vel < .2:
                break


        self.set_zero(self.get_raw_pos())
        self.set_vel(0)

        print("homed bozo")

    def manual_home(
            self):  # minutes of r&d have allowed me to make something even more scuffed than scuffed_home(). Samir will love this.
        self.axis.requested_state = 1
        time.sleep(3)
        self.set_zero(self.get_raw_pos())

    # returns phase B current going into motor
    def get_curr_B(self):
        return self.axis.motor.current_meas_phB

    # returns phase C current going into motor
    def get_curr_C(self):
        return self.axis.motor.current_meas_phC

    # only use if doing encoder index search calibration and if setup is already done
    def index_and_hold(self, dir=2, good_dir=2):
        if dir != 2:
            self.axis.motor.config.direction = dir
        self.axis.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
        while self.axis.current_state != AXIS_STATE_IDLE:
            time.sleep(0.1)
        if good_dir != 2:
            self.axis.motor.config.direction = good_dir
        self.set_pos(self.get_pos())

    # Clears all the errors on the axis
    def clear_errors(self):
        self.axis.error = 0
        self.axis.encoder.error = 0
        self.axis.motor.error = 0
        self.axis.controller.error = 0
        # There is also sensorless estimator errors but those are super rare and I am not sure what the object field is called to ima just leave it


class double_ODrive(object):

    # ax_X and ax_Y are ODrive_Axis objects
    def __init__(self, ax_X, ax_Y):
        self.y = ax_X
        self.x = ax_Y

    def calibrate(self):
        self.x.axis.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        self.y.axis.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        start = time.time()
        while self.x.axis.current_state != AXIS_STATE_IDLE or self.x.axis.current_state != AXIS_STATE_IDLE:
            time.sleep(0.1)
            if time.time() - start > 15:
                print('could not calibrate, try rebooting odrive')
                return False

    def get_pos(self):
        return [self.x.get_pos, self.y.get_pos()]

    def set_pos(self, pos_x, pos_y):
        self.x.set_pos(pos_x)
        self.y.set_pos(pos_y)

    def home_with_vel(self, vel_x, vel_y):
        self.x.set_vel(vel_x)
        self.y.set_vel(vel_y)
        time.sleep(1)
        while (self.x.is_busy() or self.y.is_busy()):
            time.sleep(0.3)

        time.sleep(1)
        self.x.set_zero(self.x.get_raw_pos())
        self.y.set_zero(self.y.get_raw_pos())
        print("done homing")

    # only use with Wetmelon's endstop firmware
    def home_with_endstops(self, vel_x, vel_y):
        self.x.axis.min_endstop.config.enabled = True
        self.x.axis.max_endstop.config.enabled = True
        self.y.axis.min_endstop.confid.enabled = True
        self.y.axis.max_endstop.config.enabled = True
        self.x.set_vel(vel_x)
        self.y.set_vel(vel_y)
        while (self.x.axis.error == 0 or self.y.axis.error == 0):
            pass
        if self.x.axis.error == 0x800 or self.x.axis.error == 0x1000:
            self.x.set_zero(self.x.get_raw_pos())
            self.x.axis.error = 0

        if self.y.axis.error == 0x800 or self.y.axis.error == 0x1000:
            self.y.set_zero(self.y.get_raw_pos())
            self.y.axis.error = 0

        self.x.axis.min_endstop.config.enabled = False
        self.x.axis.max_endstop.config.enabled = False
        self.y.axis.min_endstop.confid.enabled = False
        self.y.axis.max_endstop.config.enabled = False


# calibrates a list of ODrive_Axis objects the minimal amount
def calibrate_list(odrives):
    calibrated = []
    i = 0
    for o in odrives:
        calibrated.append(False)
        if o.axis.motor.is_calibrated:
            if o.axis.encoder.is_ready:
                calibrated[-1] = True
            else:
                o.axis.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
        else:
            o.axis.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
    is_done = False

    while not is_done:
        i = -1
        for o in odrives:
            i += 1
            if o.axis.current_state == AXIS_STATE_IDLE or calibrated[i] == True:
                calibrated[i] = True
                continue
            else:
                time.sleep(0.2)
                break
        else:
            is_done = True


# configures a hoverboard motor. Requires save and reboot
def configure_hoverboard(ax):
    ax.axis.motor.config.pole_pairs = 15
    ax.axis.motor.config.resistance_calib_max_voltage = 4
    ax.axis.motor.config.requested_current_range = 25
    ax.axis.motor.config.current_control_bandwidth = 100
    ax.axis.controller.config.pos_gain = 1
    ax.axis.controller.config.vel_gain = 0.02
    ax.axis.controller.config.vel_integrator_gain = 0.1
    ax.axis.controller.config.vel_limit = 1000
    ax.axis.controller.config.control_mode = CTRL_MODE_VELOCITY_CONTROL


print('ODrive Ease Lib 2.6.2')
'''
odrv0 = odrive.find_any()
print(str(odrv0.vbus_voltage))

ax = ODrive_Axis(odrv0.axis1)
ax.calibrate()
#ax.set_vel(10000)
#ax.home(0.05, -1)

'''
