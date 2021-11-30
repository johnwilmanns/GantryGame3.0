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


        self.x = ODrive_Ease_Lib.Axis(self.odrv1.axis1) # X
        self.y = ODrive_Ease_Lib.Axis(self.odrv1.axis0) # Y
        self.z = ODrive_Ease_Lib.Axis(self.odrv0.axis1) # Z
        self.x_max_accel = 50
        self.y_max_accel = 50
        self.x_max_decel = 100
        self.y_max_decel = 100
        self.x_max_vel = 20
        self.y_max_vel = 20
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

    #todo, add assert statments
    def startup(self):
        print("starting up")

        self.x.axis.controller.config.vel_limit = 20
        self.x.axis.controller.config.enable_overspeed_error = False

        self.y.axis.controller.config.vel_limit = 20
        self.y.axis.controller.config.enable_overspeed_error = False

        self.clear_errors()
        # self.x.start_pos_liveplotter()
        # start_liveplotter(lambda: [self.x.axis.encoder.pos_estimate, self.x.axis.encoder.vel_estimate,
        #                            self.y.axis.encoder.pos_estimate, self.y.axis.encoder.vel_estimaty ])
        # start_liveplotter(lambda: [self.x.axis.encoder.pos_estimate, self.x.axis.controller.pos_setpoint,self.y.axis.encoder.pos_estimate, self.y.axis.controller.pos_setpoint,])

        try:
            self.x.check_status()
            self.y.check_status()
        except:
            print("gotta crank one out rq")
            self.calibrate()

        self.x.check_status() #if these throw an assertion error, make sure the gantry is not up against the axis
        self.y.check_status()

        self.sensorless_home()
        self.print_positions()
        self.dump_errors()
        for axis in self.axes():
            axis.axis.requested_state = 8
            axis.axis.controller.config.control_mode = 3
            axis.axis.controller.config.input_mode = 1


    def __del__(self):
        print("setting all states to idle")
        self.x.idle()
        self.y.idle()
        self.z.idle()
        self.dump_errors()

    def axes(self):
        yield self.x
        yield self.y
        yield self.z


    def calibrate(self):
        print("warming up sphincter")
        for motor in self.axes():
            motor.calibrate_no_hold()
        for motor in self.axes():
            motor.hold_until_calibrated()
        print("anus initialized")

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
                axis.extremely_scuffed_home()
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
            if abs(self.x.get_pos() - x) <= .1 or x == -1:
                if abs(self.y.get_pos() - y) <= .1 or y == -1:
                    if abs(self.z.get_pos() - z) <= .1 or z == -1:
                        self.requested_pos = [x, y]
                        return

    def mirror_move(self, new_x, new_y):
        ratio = new_x - self.x.get_pos() / new_y - self.y.get_pos()
        print(ratio)
        #y is the dominant axis
        self.x.mirror_sub(self.y.axis, ratio)
        self.y.set_pos(new_y)


    def trap_move(self, new_x, new_y, cords = None, threshold = .2, visualizer = None):

        if cords is None:
            x_pos = self.x.get_pos()
            y_pos = self.y.get_pos()
        else:
            x_pos, y_pos = cords



        # the ratio is the x to the y movement distance
        t0 = time.time()
        ratio = abs((new_x - x_pos) / (new_y - y_pos))
        # print(ratio)
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
        # print("Time taken to calculate ratios:")
        # print(time.time() - t0)
        # t0 = time.time()
        self.x.set_trap_values(x_vel, x_accel, x_decel)
        # print(f"x: {x_vel, x_accel, x_decel}")
        self.y.set_trap_values(y_vel, y_accel, y_decel)
        # print(f"y: {y_vel, y_accel, y_decel}")


        # print("time taken to update trap vals")
        # print(time.time() - t0)


        self.x.set_pos(new_x, False)
        self.y.set_pos(new_y, False)

        x_pos = self.x.get_pos()
        y_pos = self.y.get_pos()

        if visualizer == None:
            while abs(x_pos - new_x) > threshold or abs(y_pos - new_y) > threshold:
                x_pos = self.x.get_pos()
                y_pos = self.y.get_pos()
        else:
            while abs(x_pos - new_x) > threshold or abs(y_pos - new_y) > threshold:
                x_pos = self.x.get_pos()
                y_pos = self.y.get_pos()
            visualizer.put([x_pos,y_pos])

        return x_pos, y_pos


    def set_pos_noblock(self, x = -1, y = -1, z = -1):

        if(x != -1):
            self.x.set_pos(x, False)

        if y != -1:
            self.y.set_pos(y, False)

        if z != -1:
            self.z.set_pos(z, False)

        # self.requested_pos = [x, y]




        
        

