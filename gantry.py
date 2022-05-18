import ODrive_Ease_Lib
import odrive
import servo
import time
import math
from odrive.utils import *
from odrive.enums import *

class MoveError(Exception):
    pass

class Gantry:
    def __init__(self):
        print("make sure the gantry is on")
        self.odrv1_serial = "20793595524B" # Previously Xavier
        self.odrv0_serial = "20673593524B" # Previously Yannie


        self.odrv1 = odrive.find_any(serial_number=self.odrv1_serial)
        self.odrv0 = odrive.find_any(serial_number=self.odrv0_serial)
        self.dump_errors()
        self.clear_errors()



        self.y = ODrive_Ease_Lib.Axis(self.odrv1.axis0) # X
        self.y2 = ODrive_Ease_Lib.Axis(self.odrv1.axis1) # X
        self.x = ODrive_Ease_Lib.Axis(self.odrv0.axis1) # Y
        # self.z = ODrive_Ease_Lib.Axis(self.odrv0.axis1) # Z
        self.x_max_accel = 50
        self.y_max_accel = 50
        self.x_max_decel = 50
        self.y_max_decel = 50
        self.x_max_vel = 40
        self.y_max_vel = 40
        self.has_goal = False #for trajectory management
        self.y_goal = 0
        self.x_goal = 0


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
    

    def startup(self):
        print("starting up")
        # self.dump_errors()
        
        self.x.axis.controller.config.vel_limit = 400
        self.x.axis.controller.config.enable_overspeed_error = False

        self.y.axis.controller.config.vel_limit = 400
        self.y.axis.controller.config.enable_overspeed_error = False
        self.y2.axis.controller.config.vel_limit = 400
        self.y2.axis.controller.config.enable_overspeed_error = False
        
        # for axis in self.axes():
        #     axis.motor.set_current_control_bandwidth(60)


        # self.x.start_pos_liveplotter()
        # start_liveplotter(lambda: [self.x.axis.encoder.pos_estimate, self.x.axis.encoder.vel_estimate,
        #                            self.y.axis.encoder.pos_estimate, self.y.axis.encoder.vel_estimaty ])
        # start_liveplotter(lambda: [self.x.axis.encoder.pos_estimate, self.x.axis.controller.pos_setpoint,self.y.axis.encoder.pos_estimate, self.y.axis.controller.pos_setpoint,])
        
        self.calibrate()
        self.dump_errors()
        # while True:
        #     try:
        #         self.clear_errors()
        #         try:
        #             self.x.check_status()
        #             self.y.check_status()
        #             self.y2.check_status()
        #         except AssertionError:
        #             print("gotta crank one out rq")
        #             self.calibrate()

        #         self.x.check_status() #if these throw an assertion error, make sure the gantry is not up against the axis
        #         self.y2.check_status() #if these throw an assertion error, make sure the gantry is not up against the axis
        #         self.y.check_status()
        #         break
        #     except AssertionError:
        #         if input("^w^ oopSie whoopSie, the gantwi is stukky wukki >w<. Pwease pwace it in a new wowcation ^w^ \nThen pwess enter UwU") == "dump":
        #             self.dump_errors()

        for axis in self.axes():
            axis.axis.controller.config.control_mode = AXIS_STATE_ENCODER_INDEX_SEARCH
            axis.axis.controller.config.input_mode = 1
            axis.axis.requested_state = 8

        print("homing")
        self.home()
        
        
        self.print_positions()
        # self.dump_errors()

        
        for axis in self.axes():
            axis.axis.requested_state = AXIS_STATE_IDLE
        # self.y2.axis.config.control_mode = AXIS_STATE_ENCODER_INDEX_SEARCH
        # self.y2.axis.controller.config.input_mode = INPUT_MODE_MIRROR
        #
        #
        #
        # # self.y2.axis.controller.config.input_mode = INPUT_MODE_MIRROR
        # self.y2.axis.controller.config.axis_to_mirror = 0
        # self.y2.axis.controller.config.mirror_ratio = 1

        # for axis in self.axes():
        #     axis.idle()




    def __del__(self):
        # print("setting all states to idle")
        # self.x.idle()
        # self.y.idle()
        # # self.z.idle()
        # print("set all states to idle")
        print("deleted bruh")
        # self.dump_errors()

    def axes(self):
        yield self.x
        yield self.y2
        yield self.y

    def idle(self):
        for axis in self.axes():
            axis.axis.requested_state = AXIS_STATE_IDLE

    def calibrate(self):
        
        self.idle()

        print("warming up sphincter")
        if not self.x.check_status():
            self.x.axis.config.calibration_lockin.accel = 20
            self.x.axis.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
        
        if not (self.y.check_status() and self.y2.check_status()):
            self.y.axis.config.calibration_lockin.accel = 20
            self.y2.axis.config.calibration_lockin.accel = -20
            self.y.axis.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
            self.y2.axis.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
        
        self.x.hold_until_calibrated()
        self.y.hold_until_calibrated()
        self.y2.hold_until_calibrated()
        self.clear_errors()
        
        if not self.x.check_status():
            self.x.axis.config.calibration_lockin.accel = -20
            self.x.axis.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
        
        if not (self.y.check_status() and self.y2.check_status()):
            self.y.axis.config.calibration_lockin.accel = -20
            self.y2.axis.config.calibration_lockin.accel = 20
            self.y.axis.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
            self.y2.axis.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
            
        self.x.hold_until_calibrated()
        self.y.hold_until_calibrated()
        self.y2.hold_until_calibrated()
        
        assert(self.x.check_status())
        assert(self.y.check_status())
        assert(self.y2.check_status())
        print("Calibrated!")

    def home(self):

        self.x.set_vel(-10)
        self.y2.set_vel(-10)
        self.y.set_vel(-10)
        
        
        while True:
            self.x.set_home()
            self.y.set_home()
            self.y2.set_home()
            
            time.sleep(.5)
            
            if abs(self.x.get_pos()) < .05 and abs(self.y.get_pos()) < .05:
                self.x.set_vel(0)
                self.y2.set_vel(0)
                self.y.set_vel(0)
                
                time.sleep(.5)
                
                self.x.set_home()
                self.y.set_home()
                self.y2.set_home()
                
                for axis in self.axes():
                    axis.set_pos(0.1, True)
                
                break   
            
        print(self.x.get_pos(), self.y.get_pos())
        



    def enable_motors(self):
        print("warming up sphincter")
        for motor in self.axes():
            motor.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

    def dump_errors(self):
        print("dumping odrv0 errors (206)")
        print(dump_errors(self.odrv0))
        print("dumping odrv1 errors (207)")
        print(dump_errors(self.odrv1))

    def clear_errors(self):
        self.odrv0.clear_errors()
        self.odrv1.clear_errors()

    def print_positions(self):
        print(f"X = {self.x.get_pos()}")
        print(f"Y = {self.y.get_pos()}")


    def set_pos(self, x = -1, y = -1, y2 = -1, y_mirror = True):
        '''
        The missile knows where it is at all times. It knows this because it knows where it isn't. By subtracting where it is from where it isn't, or where it isn't from where it is (whichever is greater), it obtains a difference, or deviation. The guidance subsystem uses deviations to generate corrective commands to drive the missile from a position where it is to a position where it isn't, and arriving at a position where it wasn't, it now is. Consequently, the position where it is, is now the position that it wasn't, and it follows that the position that it was, is now the position that it isn't.
In the event that the position that it is in is not the position that it wasn't, the system has acquired a variation, the variation being the difference between where the missile is, and where it wasn't. If variation is considered to be a significant factor, it too may be corrected by the GEA. However, the missile must also know where it was.
        '''
        print(f"{x} {y}")
        if(x != -1):
            self.x.set_pos(x)
        
        if y != -1:
            if y_mirror:
                self.y.set_pos(y)
                self.y2.set_pos(y)
            else:
                if y2 != -1:
                    self.y2.set_pos(y2)
                self.y.set_pos(y)


        while True:
            # print("x", x, self.x.get_pos())
            # print("y", y, self.y.get_pos())
            
            if abs(self.x.get_pos() - x) <= .1 or x == -1:
                if abs(self.y.get_pos() - y) <= .1 or y == -1:

                    self.requested_pos = [x, y]
                    return
    def mirror_move(self, new_x, new_y):
        ratio = new_x - self.x.get_pos() / new_y - self.y.get_pos()
        print(ratio)
        #y is the dominant axis
        self.x.mirror_sub(self.y.axis, ratio)
        self.y.set_pos(new_y)


        

    def trap_move(self, new_x, new_y, cords = None, threshold = .1, escape_threshold = .2, vel_threshold = .1, max_time = .5):

        if cords is None:
            x_pos = self.x.get_pos()
            y_pos = self.y.get_pos()
        else:
            x_pos, y_pos = cords



        # the ratio is the x to the y movement distance
        # t0 = time.time()
        # ratio = abs((new_x - x_pos) / (new_y - y_pos))
        # # print(ratio)
        # x_accel = self.x_max_accel
        # y_accel = x_accel / ratio
        # if y_accel > self.y_max_accel:
        #     y_accel = self.y_max_accel
        #     x_accel = y_accel * ratio
        #
        # x_decel = self.x_max_decel
        # y_decel = x_decel / ratio
        #
        # if y_decel > self.y_max_decel:
        #     y_decel = self.y_max_decel
        #     x_decel = y_decel * ratio
        #
        # x_vel = self.x_max_vel
        # y_vel = x_vel / ratio
        #
        # if y_vel > self.y_max_vel:
        #     y_vel = self.y_max_vel
        #     x_vel = y_vel * ratio

        self.x.set_trap_values(self.x_max_accel, self.x_max_vel, self.x_max_decel)
        self.y.set_trap_values(self.y_max_accel, self.y_max_vel, self.y_max_decel)
        self.y2.set_trap_values(self.y_max_accel, self.y_max_vel, self.y_max_decel)

        # self.x.set_trap_values(x_vel, x_accel, x_decel)
        # self.y.set_trap_values(y_vel, y_accel, y_decel)
        # self.y2.set_trap_values(y_vel, y_accel, y_decel)



        # print("time taken to update trap vals")
        # print(time.time() - t0)


        self.x.set_pos(new_x, False)
        self.y.set_pos(new_y, False)
        self.y2.set_pos(new_y, False)

        x_pos = self.x.get_pos()
        y_pos = self.y.get_pos()
        t0 = time.perf_counter()
        x_accelerating = True
        y_accelerating = True
        old_x_vel = self.x.get_vel()
        old_y_vel = self.y.get_vel()
        while True:
            if x_accelerating or y_accelerating:
                if old_x_vel > self.x.get_vel():
                    x_accelerating = False
                if old_y_vel > self.y.get_vel():
                    y_accelerating = False
            else:
                break
            if time.perf_counter() - t0 > max_time:
                print("movement exceeded for acceleration")
                raise MoveError("Movement timed out")
        while self.x.get_vel() > vel_threshold or self.y.get_vel() > vel_threshold:
            if time.perf_counter() > t0 + max_time:
                raise MoveError("movement expired during deceleration")

        while abs(x_pos - new_x) > threshold or abs(y_pos - new_y) > threshold:
            x_pos = self.x.get_pos()
            y_pos = self.y.get_pos()

            if time.perf_counter() - t0 > max_time:
                if abs(x_pos - new_x) < escape_threshold and abs(y_pos - new_y) < escape_threshold:
                    break
                print("movement timed out during positional controll")
                raise MoveError("Movement timed out")





    def set_pos_noblock(self, x = -1, y = -1):

        if(x != -1):
            self.x.set_pos(x, False)

        if y != -1:
            self.y.set_pos(y, False)
            self.y2.set_pos(y, False)



        # self.requested_pos = [x, y]


if __name__ == "__main__":
    print("starting")
    gantry = Gantry()
    gantry.startup()
    print("hello")
    # gantry.enable_motors()
    # while True:

    #     gantry.set_pos(float(input("x")), float(input("y")))

        # gantry.y.set_pos(float(input("y:")), ensure_control_mode=True)
        

