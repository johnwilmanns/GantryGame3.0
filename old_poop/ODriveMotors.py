# coding: utf-8
import odrive
from odrive.enums import *
import ODrive_Ease_Lib
import time
import usb.core
import svg.path
from xml.dom import minidom
from pidev import stepper
import numpy
import math
import pickle
from colormath.color_objects import sRGBColor, LabColor, HSVColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

# for future note: two motor vert serial # 61951538836535
#                  one motor hori serial # 61985896477751

# xavier refers to the x axis, yannie to the y

xavier_serial = 61985896477751
yannie_serial = 61951538836535

'''
Here, I use color math to represent the colors as HSV (Hue, Saturation, Value). I used to compare the 
hues to raw images to attain the closest color to the image, but since I now use paletteing, this is kind
of unnecessary. Make some junior or have you replace these with string comparisons
'''

RED = convert_color(sRGBColor.new_from_rgb_hex('#c40909'), HSVColor).get_value_tuple()[0]
ORANGE = convert_color(sRGBColor.new_from_rgb_hex('#e86f25'), HSVColor).get_value_tuple()[0]
YELLOW = convert_color(sRGBColor.new_from_rgb_hex('#e8d725'), HSVColor).get_value_tuple()[0]
GREEN = convert_color(sRGBColor.new_from_rgb_hex('#075b3a'), HSVColor).get_value_tuple()[0]
BLUE = convert_color(sRGBColor.new_from_rgb_hex('#1505a8'), HSVColor).get_value_tuple()[0]
PURPLE = convert_color(sRGBColor.new_from_rgb_hex('#a500a5'), HSVColor).get_value_tuple()[0]
LIGHT_BLUE = convert_color(sRGBColor.new_from_rgb_hex('#52bfe8'), HSVColor).get_value_tuple()[0]
LIME_GREEN = convert_color(sRGBColor.new_from_rgb_hex('#8df41e'), HSVColor).get_value_tuple()[0] 
RED_ORANGE = convert_color(sRGBColor.new_from_rgb_hex('#ff4800'), HSVColor).get_value_tuple()[0]
PINK = convert_color(sRGBColor.new_from_rgb_hex('#ff00ae'), HSVColor).get_value_tuple()[0]
LILAC = convert_color(sRGBColor.new_from_rgb_hex('#9c00ff'), HSVColor).get_value_tuple()[0]
BLACK = convert_color(sRGBColor.new_from_rgb_hex('#000000'), HSVColor).get_value_tuple()[0]

class GGMotors(object):

    '''
    Constants for positioning the pen carriage. It's important to realize that much of these rely on the
    sheathes for the pens being at a constant position. This includes how high the lids are positioned.
    '''

    Z_IN = 20000 # Z position for grabbing pen
    Z_RETURN = 10000 # Z position for returning pen (yes they are different on purpose)
    Z_BARELY = 280000 # Z position for... something or other. Delete?
    Z_HIGH = 700000 # Z position for highest I am willing to let pen carriage go
    Z_HOVER = 400000 # Z position for hovering over paper
    Z_TOUCH = 300000 # Z position for drawing on paper

    X_PEN1 = -145100 # X position for first row of pens
    X_PEN2 = -161360 # X position for second row of pens
    
    Y_PEN_BASE = 82500 # Y position for first pen
    Y_PEN_INTERVAL = 16400 # Distance between each pen

    COLOR = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, LIGHT_BLUE, LIME_GREEN, RED_ORANGE, PINK, LILAC, BLACK] # List of colors for drawing function to choose from.

    def __init__(self):
        
        '''
        The following code works and has worked for a while. So if there is an issue, it is most likely
        with the usb connections themselves, rather than a software problem. Test those problems first.
        '''

        dev = usb.core.find(find_all=1, idVendor=0x1209, idProduct=0x0d32) # finds all usb devices
        od = []

        a = next(dev)
        od.append(odrive.find_any('usb:%s:%s' % (a.bus, a.address))) # looks for an odrive with address
        a = next(dev)
        od.append(odrive.find_any('usb:%s:%s' % (a.bus, a.address)))
        
        if od[0].serial_number == xavier_serial:
            self._xavier = od[0]
            self._yannie = od[1]
        else:
            self._xavier = od[1]
            self._yannie = od[0]
        
        self._xavier_axis0 = ODrive_Ease_Lib.ODrive_Axis(self._xavier.axis0)
        self._xavier_axis1 = ODrive_Ease_Lib.ODrive_Axis(self._xavier.axis1)

        self._yannie_axis0 = ODrive_Ease_Lib.ODrive_Axis(self._yannie.axis0)
        self._yannie_axis1 = ODrive_Ease_Lib.ODrive_Axis(self._yannie.axis1)

        '''
        Calibrating motors
        '''

        self._xavier.axis0.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
        self._xavier.axis1.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
        self._yannie.axis0.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
        self._yannie.axis1.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION

        start = time.time()

        while (self._xavier.axis0.current_state != AXIS_STATE_IDLE or
               self._xavier.axis1.current_state != AXIS_STATE_IDLE or
               self._yannie.axis0.current_state != AXIS_STATE_IDLE or
               self._yannie.axis1.current_state != AXIS_STATE_IDLE):
            time.sleep(0.1)
            if time.time() - start > 15:
                print("could not calibrate, try rebooting odrive")
                return
        
        '''
        Pen gripper parameters. Make sure that the pen holder is in the open position before attempting
        this code.
        '''

        self._holder = stepper(port=0, microsteps=64, spd=200)
        self._holder.set_max_speed(300)
        self._holder.set_speed(110)
        self._holder.set_micro_steps(64)

        '''
        Parameters for velocity, acceleration, position, etc. Tune to your heart's content
        '''

        self.set_x_vel_limit(50000)
        self.set_y_vel_limit(50000)
        self.set_x_accel_limit(1000000)
        self.set_y_accel_limit(200000)
        self.set_x_decel_limit(1000000)
        self.set_y_decel_limit(200000)
        self.set_x_A_per_css(0) # Changes how much current is used to achieve a certain acceleration
        self.set_y_A_per_css(0)
        self.set_x_current_limit(15)
        self.set_y_current_limit(15)


       # self._xavier.axis0.controller.config.vel_limit_tolerance = 0
       # self._xavier.axis1.controller.config.vel_limit_tolerance = 0
       # self._yannie.axis0.controller.config.vel_limit_tolerance = 0
       # self._yannie.axis1.controller.config.vel_limit_tolerance = 0


        self.set_z_vel_limit(500000)
        self.set_z_accel_limit(1000000)
        self.set_z_decel_limit(1000000)
        self.set_z_A_per_css(0)
        self.set_z_current_limit(15)

        '''
        The following values affect how exact the motor wants to be, or how much effort it'll spend 
        getting to the exact location. Higher pos_gain means that the motor wants to be more accurate to
        its predicted position. Higher vel_gain means that the motor wants to be more accurate to its 
        predicted velocity. You can change these values in other code by opening odrivetool in terminal
        '''

        self.set_x_pos_gain(100)
        self.set_y_pos_gain(100)
        self.set_x_vel_gain(0.0004)
        self.set_y_vel_gain(0.0004)

        '''
        Homing code.
        '''

        self.set_x_vel_no_pid(50000)
        self.set_y_vel_no_pid(-10000)
        self.set_z_vel_no_pid(-50000)
        time.sleep(8)
        self.set_y_vel_no_pid(-100000)
        time.sleep(8)
        self.set_x_vel_no_pid(0)
        self.set_y_vel_no_pid(0)
        self.set_z_vel_no_pid(0)

        self.set_x_zero()
        self.set_y_zero()
        self.set_z_zero()

        '''
        Is the carriage holding a pen? 0 if nothing, 1-12 if otherwise (marked on the pen panel)
        '''

        self.holding_pen = 0
        
        time.sleep(1)

        self.center()

    def release(self):
        self._holder.go_to_position(0)

    def grab(self):
        self._holder.go_to_position(600)

    def set_z_pos(self, pos):
        self._xavier_axis1.set_pos(pos)

    '''
    '_trap' functions plot a path for the motor to follow before executing. Useful for having the motor
    plot nice lines. Use when moving long distances. The one for the y-axis is currently broken.
    '''

    def set_z_pos_trap(self, pos):
        self._xavier_axis1.set_pos_trap(pos)

    def set_x_vel_no_pid(self, vel):
        self._xavier_axis0.set_vel(vel)

    def set_y_vel_no_pid(self, vel):
        self._yannie_axis0.set_vel(vel)
        self._yannie_axis1.set_vel(vel)

    def set_z_vel_no_pid(self, vel):
        self._xavier_axis1.set_vel(vel)
    
    def get_x_vel(self):
        return self._xavier_axis0.get_vel()

    def get_y_vel(self):
        return (self._yannie_axis0.get_vel() + self._yannie_axis1.get_vel()) / 2

    def set_x_vel_limit(self, limit):
        self._xavier.axis0.controller.config.vel_limit = limit
        self._xavier.axis0.trap_traj.config.vel_limit = limit

    def get_x_vel_limit(self):
        return self._xavier.axis0.controller.config.vel_limit

    def set_y_vel_limit(self, limit):
        self._yannie.axis0.controller.config.vel_limit = int(limit * 1.1)
        self._yannie.axis1.controller.config.vel_limit = int(limit * 1.1)
        self._yannie.axis0.trap_traj.config.vel_limit = limit
        self._yannie.axis1.trap_traj.config.vel_limit = limit

    def get_y_vel_limit(self):
        return self._yannie.axis0.trap_traj.config.vel_limit

    def set_z_vel_limit(self, limit):
        self._xavier.axis1.controller.config.vel_limit = limit
        self._xavier.axis1.trap_traj.config.vel_limit = limit

    def get_z_vel_limit(self):
        return self._xavier.axis1.trap_traj.config.vel_limit

    def set_x_accel_limit(self, limit):
        self._xavier.axis0.trap_traj.config.accel_limit = limit

    def get_x_accel_limit(self):
        return self._xavier.axis0.trap_traj.config.accel_limit
    
    def set_y_accel_limit(self, limit):
        self._yannie.axis0.trap_traj.config.accel_limit = limit
        self._yannie.axis1.trap_traj.config.accel_limit = limit

    def get_y_accel_limit(self):
        return self._yannie.axis0.trap_traj.config.accel_limit

    def set_z_accel_limit(self, limit):
        self._xavier.axis1.trap_traj.config.accel_limit

    def get_z_accel_limit(self):
        return self._xavier.axis1.trap_traj.config.accel_limit

    def set_x_decel_limit(self, limit):
        self._xavier.axis0.trap_traj.config.decel_limit = limit

    def get_x_decel_limit(self):
        return self._xavier.axis0.trap_traj.config.decel_limit

    def set_y_decel_limit(self, limit):
        self._yannie.axis0.trap_traj.config.decel_limit = limit
        self._yannie.axis1.trap_traj.config.decel_limit = limit
    
    def get_y_decel_limit(self):
        return self._yannie.axis0.trap_traj.config.decel_limit

    def set_z_decel_limit(self, limit):
        self._xavier.axis1.trap_traj.config.decel_limit = limit

    def get_z_decel_limit(self):
        return self._xavier.axis1.trap_traj.config.decel_limit

    def set_x_current_limit(self, limit):
        self._xavier.axis0.motor.config.current_lim = limit
    
    def get_x_current_limit(self):
        return self._xavier.axis0.motor.config.current_lim

    def set_y_current_limit(self, limit):
        self._yannie.axis0.motor.config.current_lim = limit
        self._yannie.axis1.motor.config.current_lim = limit
    
    def get_y_current_limit(self):
        return self._yannie.axis0.motor.config.current_lim

    def set_z_current_limit(self, limit):
        self._xavier.axis1.motor.config.current_lim = limit

    def get_z_current_limit(self):
        return self._xavier.axis1.motor.config.current_lim
    
    '''
    A_per_css refers to how much current should be used to achieve a certain acceleration. With luck,
    you will never have to use this.
    '''

    def set_x_A_per_css(self, A):
        self._xavier.axis0.trap_traj.config.A_per_css = A

    def get_x_A_per_css(self):
        return self._xavier.axis0.trap_traj.config.A_per_css

    def set_y_A_per_css(self, A):
        self._yannie.axis0.trap_traj.config.A_per_css = A
        self._yannie.axis1.trap_traj.config.A_per_css = A

    def get_y_A_per_css(self):
        return self._yannie.axis0.trap_traj.config.A_per_css

    def set_z_A_per_css(self, A):
        self._xavier.axis1.trap_traj.config.A_per_css = A

    def get_z_A_per_css(self):
        return self._xavier.axis1.trap_traj.config.A_per_css

    def get_x_vel_gain(self):
        return self._xavier.axis0.controller.config.vel_gain

    def set_x_vel_gain(self, gain):
        self._xavier.axis0.controller.config.vel_gain = gain

    def get_y_vel_gain(self):
        return self._yannie.axis0.controller.config.vel_gain

    def set_y_vel_gain(self, gain):
        self._yannie.axis0.controller.config.vel_gain = gain
        self._yannie.axis1.controller.config.vel_gain = gain

    def set_z_vel_gain(self, gain):
        self._xavier.axis1.controller.config.vel_gain = gain

    def get_z_vel_gain(self):
        return self._xavier.axis1.controller.config.vel_gain

    def get_x_pos_gain(self):
        return self._xavier.axis0.controller.config.pos_gain

    def set_x_pos_gain(self, gain):
        self._xavier.axis0.controller.config.pos_gain = gain

    def get_y_pos_gain(self):
        return self._yannie.axis0.controller.config.pos_gain

    def set_y_pos_gain(self, gain):
        self._yannie.axis0.controller.config.pos_gain = gain
        self._yannie.axis1.controller.config.pos_gain = gain

    def set_z_pos_gain(self, gain):
        self._xavier.axis1.controller.config.pos_gain = gain

    def get_z_pos_gain(self):
        return self._xavier.axis1.controller.config.pos_gain
        
    def get_x_pos(self):
        return self._xavier_axis0.get_pos()
    
    def get_y_pos(self):
        return (self._yannie_axis0.get_pos() + self._yannie_axis1.get_pos()) / 2

    def get_z_pos(self):
        return self._xavier_axis1.get_pos()

    def set_x_pos_no_pid(self, pos):
        self._xavier_axis0.set_pos(pos)
        
    '''
    AVOID USING set_y_pos() and set_x_pos(). You're probably looking for set_x_pos_no_pid() and set_y_pos_no_pid()
    Sorry, this function is a specific case where we don't want the odrive to waste time changing the mode to
    position control. I'm aware this could be named better, but I'm lazy. If you want to see how it's
    used, check out the definition of draw_from_file!
    '''
        
    def set_x_pos(self, pos):
        self._xavier.axis0.controller.pos_setpoint = pos + self._xavier_axis0.zero

    def set_y_pos_no_pid(self, pos):
        self._yannie_axis0.set_pos(pos)
        self._yannie_axis1.set_pos(pos)
    
    def set_y_pos(self, pos):
        self._yannie.axis0.controller.pos_setpoint = pos + self._yannie_axis0.zero
        self._yannie.axis1.controller.pos_setpoint = pos + self._yannie_axis1.zero

    def set_x_pos_trap(self, pos):
        self._xavier_axis0.set_pos_trap(pos)

    def set_y_pos_trap(self, pos):
        #self._yannie_axis0.set_pos_trap(pos)
        #self._yannie_axis1.set_pos_trap(pos)
        self.set_y_pos_no_pid(pos)

    '''
    Ignore set_x_pos_pos_pid.
    Just a test I'm running, in case I forget to delete it by summer.
    '''
    
    def set_x_pos_pos_pid(self, pos, vel, t_kp=200, t_ki=0.0, t_kd=0.0, dt=0.001):
        step = numpy.sign(pos - self.get_x_pos()) * abs(vel) * dt
        targ_pos = self.get_x_pos()

        err = 0
        err_sum = 0
        last_err = 0

        curr_pos = self.get_x_pos()

        mark = time.time()
        while curr_pos < pos - abs(step) or curr_pos > pos + abs(step):

            targ_pos += step
            curr_pos = self.get_x_pos()
            err = curr_pos - targ_pos
            
            err_sum += err
            
            self._xavier_axis0.set_vel(- err * t_kp - err_sum * t_ki - (err - last_err) * t_kd)
            
            while time.time() < mark + dt:
                pass

            mark = time.time()

            last_err = err

        targ_pos = pos

        while abs(self.get_x_vel()) > 1:

            err = self.get_x_pos() - targ_pos
            
            err_sum += err

            self._xavier_axis0.set_vel(- err * t_kp - err_sum * t_ki - (err - last_err) * t_kd)

            while time.time() < mark + dt:
                pass

            mark = time.time()

            last_err = err
            
    '''
    It returns the pen.
    Crazy huh?
    Yeah.
    '''

    def return_pen(self):

        if(self.holding_pen == 0):
            print("No Pen!")
            return False

        self.grab()
        time.sleep(0.25)
        while(self._holder.isBusy()):
            pass

        self.set_z_pos(self.Z_HIGH)
        time.sleep(0.25)
        while(self.is_z_busy()):
            pass

        self.set_y_pos_trap(self.Y_PEN_BASE - self.Y_PEN_INTERVAL * ((self.holding_pen - 1) % 6 - 0.5))
        time.sleep(0.25)
        while(self.is_y_busy()):
            pass

        if(self.holding_pen > 6):
            self.set_x_pos_trap(self.X_PEN2)
        else:
            self.set_x_pos_trap(self.X_PEN1)
        time.sleep(0.25)
        while(self.is_x_busy()):
            pass

        self.set_y_pos_trap(self.Y_PEN_BASE - self.Y_PEN_INTERVAL * ((self.holding_pen - 1) % 6))
        time.sleep(0.25)
        while(self.is_y_busy()):
            pass

        self.set_z_pos(self.Z_RETURN)
        time.sleep(0.25)
        while(self.is_z_busy()):
            pass

        self.release()
        time.sleep(0.25)
        while(self._holder.isBusy()):
            pass

        self.set_z_pos(self.Z_HIGH)
        time.sleep(0.25)
        while(self.is_z_busy()):
            pass

        self.holding_pen = 0
        
    '''
    Guess what this one does
    *it picks up the pen*
    '''
    
    def pick_pen(self, pen, count=4, vari=500):
        
        if(self.holding_pen != 0):
            print("Holding Pen!")
            return False

        if(pen < 1 or pen > 12):
            print("Not A Valid Pen!")
            return False

        self.release()
        time.sleep(0.25)
        while(self._holder.isBusy()):
            pass

        self.set_z_pos(self.Z_HIGH)
        time.sleep(0.25)
        while(self.is_z_busy()):
            pass

        self.set_y_pos_trap(self.Y_PEN_BASE - self.Y_PEN_INTERVAL * ((pen - 1) % 6) - vari)

        targ_x = 0
       
        if(pen > 6):
            self.set_x_pos_trap(self.X_PEN2 - vari)
            targ_x = self.X_PEN2
        else:
            self.set_x_pos_trap(self.X_PEN1 - vari)
            targ_x = self.X_PEN1
        time.sleep(0.25)
        while(self.is_x_busy() or self.is_y_busy()):
            pass

        self.set_z_pos(self.Z_HOVER)
        time.sleep(0.25)
        while(self.is_z_busy()):
            pass
        
        self.set_z_vel_no_pid(-50000)
        
        '''
        This section wiggles the pen carriage around so it can settle onto the pen nicely.
        '''
        
        for x in range(0, count):
            self.set_x_pos_trap(targ_x + vari)
            self.set_y_pos_trap(self.Y_PEN_BASE - self.Y_PEN_INTERVAL * ((pen - 1) % 6))
            time.sleep(0.15)
            while(self.is_x_busy() or self.is_y_busy()):
                pass
            
            self.set_x_pos_trap(targ_x - vari)
            self.set_y_pos_trap(self.Y_PEN_BASE - self.Y_PEN_INTERVAL * ((pen - 1) % 6) + vari)
            time.sleep(0.15) 
            while(self.is_x_busy() or self.is_y_busy()): 
                 pass 
             
            self.set_x_pos_trap(targ_x + vari)
            time.sleep(0.15)
            while(self.is_x_busy()):
                pass
    
            self.set_x_pos_trap(targ_x - vari)
            self.set_y_pos_trap(self.Y_PEN_BASE - self.Y_PEN_INTERVAL * ((pen - 1) % 6))
            while(self.is_x_busy() or self.is_y_busy()):
                pass
    
            self.set_x_pos_trap(targ_x + vari)
            self.set_y_pos_trap(self.Y_PEN_BASE - self.Y_PEN_INTERVAL * ((pen-1) % 6) - vari)
            while(self.is_x_busy() or self.is_y_busy()):
                pass
    
            self.set_x_pos_trap(targ_x - vari)
            while(self.is_x_busy()):
                pass
            
            self.set_x_pos_trap(targ_x)
            self.set_y_pos_trap(self.Y_PEN_BASE - self.Y_PEN_INTERVAL * ((pen - 1) % 6))
            time.sleep(0.15)
            while(self.is_x_busy() or self.is_y_busy()):
                pass
      
        self.set_z_pos(self.Z_IN)
        time.sleep(0.25)
        while(self.is_z_busy()):
            pass

        self.grab()
        time.sleep(0.25)
        while(self._holder.isBusy()):
            pass

        self.set_z_pos(self.Z_HIGH)
        time.sleep(0.25)
        while(self.is_z_busy()):
            pass

        self.holding_pen = pen

        self.set_y_pos_trap(self.Y_PEN_BASE - self.Y_PEN_INTERVAL * ((pen - 1) % 6 - 0.5))
        time.sleep(0.25)
        while(self.is_y_busy()):
            pass

        self.set_x_pos_trap(-50000)
        time.sleep(0.25)
        while(self.is_x_busy()):
            pass

    '''
    A nice test to see if your motors are working properly. Moves the carriage in a circle.
    '''
        
    def circle_pos(self, times, vel, dt=0.001):
        self.set_x_pos_no_pid(-25000)
        self.set_y_pos_trap(30000)
        time.sleep(2)

        targ_x = [1 * 25000 - 50000]
        targ_y = [0 * 25000 + 30000]

        num_pieces = int(50000 * math.pi / (vel * dt))
        piece = vel * dt / 25000

        for x in range(0, num_pieces):
            targ_x.append(numpy.cos(x * piece) * 25000 - 50000)
            targ_y.append(numpy.sin(x * piece) * 25000 + 30000)

        self._xavier_axis0.set_pos_ctrl()
        self._yannie_axis0.set_pos_ctrl()
        self._yannie_axis1.set_pos_ctrl()

        mark = time.time()

        for x in range(0, num_pieces):
            self.set_x_pos(targ_x[x])
            self.set_y_pos(targ_y[x])
            
            print(time.time() - mark)

            while time.time() < mark + dt:
                pass

            mark = time.time()


        self.set_x_vel_no_pid(0)
        self.set_y_vel_no_pid(0)

    '''
    Deprecated. You shouldn't have to run calculations for image conversion on the pi.
    '''

    def calc_draw(file_name, save_name, test_scale=30, vel=20000, dt=0.005):
        doc = minidom.parse("drawings/" + file_name)
        path_data = doc.getElementsByTagName('path')
        path_strings = [path.getAttribute('d') for path in path_data]
        path_colors = [path.getAttribute('style').replace('fill:', '') for path in path_data]
        paths = []
    
        metadata = doc.getElementsByTagName('g')
    
        if len(metadata) != 0 and metadata[0].getAttribute('transform'):
            s = metadata[0].getAttribute('transform')
            trans = s.split(' ', 1)[0].strip("translate()").split(",")
            x_trans = -float(trans[0])
            y_trans = -float(trans[1])
        else:
            x_trans = 0
            y_trans = 0
    
        scale = test_scale
    
    
        path_number = 0
        for p in path_strings:
            paths.append(svg.path.parse_path(p))
            if path_colors[path_number]:
                paths[path_number].color = '#f8fafa'
            else:
                paths[path_number].color = path_colors[path_number]
            path_number += 1
    
        origin_pt = paths[0][0].point(0)
    
        while (origin_pt.real - x_trans) * scale > 110000 or (origin_pt.imag - y_trans) * scale > 70000:
            scale -= 1
        
        print("New scale: " + str(scale))
    
        stp_lng = abs(vel) * dt / scale
        plans = []
        num_paths = len(paths)
        
        for i in range(0, num_paths):
    
            plan = []
            num_segments = len(paths[i])
    
            for x in range(0, num_segments):
                l = paths[i][x].length()
                num_stp = int(l / stp_lng)
                pt = []
    
                for y in range(0, num_stp):
                    pt.append(paths[i][x].point(stp_lng * y / l))
                    if((pt[y].real - x_trans) * scale > 110000 or (pt[y].imag - y_trans) * scale > 70000):
                        print(str(pt[y].real) + " " + str(pt[y].imag))
                        return
    
                plan.append(pt)
                print("Segment " + str(x) + " of " + str(num_segments))
    
            plans.append(plan)
            print("Path " + str(i) + " of " + str(num_paths))

        with open("drawings/" + save_name + "_plans.pickle", "wb") as f:
            pickle.dump(plans, f)

        with open("drawings/" + save_name + "_paths.pickle", "wb") as f:
            pickle.dump(paths, f)
       
        print("translate")
        print(x_trans)
        print(y_trans)

    '''
    Important! The actual drawing code!
    file_name: name of file to draw minus '_plans.pickle'
    scale: how much to scale image up to encoder counts
    x_trans: horizontal offset
    y_trans: vertical offset
    vel: about how quickly motors should travel
    dt: time between commands to odrive
    '''
    
    def draw_from_file(self, file_name, scale=1, x_trans=0, y_trans=0, vel=20000, dt=0.005):
        
        plans = []
        paths = []

        scale = int(scale)
        
        '''
        .pickle files are objects that have been stored into a file
        The plans contain the entirety of the calculated points.
        The paths contain the entirety of the functions used to get those points. They also contain
        some metadata, like color. Paths are made up of segments, which are functions like 'move' 'line' 'bezier curve'
        '''
        with open("drawings/" + file_name + "_plans.pickle", "rb") as f:
            plans = pickle.load(f)

        with open("drawings/" + file_name + "_paths.pickle", "rb") as f:
            paths = pickle.load(f)

        need_move = False

        for i in range(0, len(paths)): # Iterate through paths

            if (paths[i].color == '#ffffff'):
                continue
            self.switch_pen_to_color(paths[i].color)
            for x in range(0, len(paths[i])): # Iterate through segments
                if(isinstance(paths[i][x], svg.path.path.Move)): # If the segment is a move, we mark that.
                    need_move = True
                else:
                    if need_move and len(plans[i][x]) > 0:
                        # If the previous command was a move and we have a point we can jump to, we should
                        # try to move there.
                        self.set_z_pos(self.Z_HOVER)
                        time.sleep(0.2)
                        while(self.is_z_busy()):
                            pass
                        time.sleep(0.05)
                        self.set_x_pos_trap(-110000 + (plans[i][x][0].real - x_trans) * scale)
                        self.set_y_pos_trap((plans[i][x][0].imag - y_trans) * scale)
                        time.sleep(0.2)
                        while self.is_x_busy() or self.is_y_busy() or self.is_z_busy():
                            pass
                        time.sleep(0.05)
                        need_move = False
                    self.set_z_pos(self.Z_TOUCH)
                    mark = time.time() # mark when we started sending commands
                    self._xavier_axis0.set_pos_ctrl()
                    self._yannie_axis0.set_pos_ctrl()
                    self._yannie_axis1.set_pos_ctrl()
                    while self.is_z_busy():
                        pass
                    for stp in plans[i][x]: # Iterate through points
                        self.set_x_pos(-110000 + (stp.real - x_trans) * scale)
                        self.set_y_pos((stp.imag - y_trans) * scale)
                        while time.time() < mark + dt:
                            # Wait until time in step is finished, allowing motors to move.
                            pass
                        mark = time.time()
            self.set_x_vel_no_pid(0)
            self.set_y_vel_no_pid(0)
            self.set_z_pos(self.Z_HOVER)
        
        self.return_pen()
        self.center()

    def switch_pen_to_color(self, color):
        
        # Compares sharpie colors to color of image, in order to pick the best sharpie to represent it.

        col =  convert_color(sRGBColor.new_from_rgb_hex(color), HSVColor).get_value_tuple()

        min_dis = 180
        color = 0


        if col[2] < 0.3:
            color = 12
        else:
            for x in range(0, len(self.COLOR)):
                dis = min((col[0] - self.COLOR[x]) % 360, (self.COLOR[x] - col[0]) % 360)
                if dis < min_dis:
                    min_dis = dis
                    color = x + 1

        if self.holding_pen == color:
            return 
        elif self.holding_pen != 0:
            self.return_pen()
        self.pick_pen(color)
    
    def sign(self, x, y): # Fun stuff
        self.draw_from_file("obama", scale=100, vel=10000, x_trans=x, y_trans=y)

    def center(self): # Important function, resets the carrriage to home
        self.set_x_pos_trap(-50000)
        self.set_y_pos_trap(35000)
        self.set_z_pos(self.Z_HIGH)

    def set_x_zero(self): # Sets zero of encoder
        self._xavier_axis0.set_zero(self._xavier_axis0.get_raw_pos())

    def set_y_zero(self):
        self._yannie_axis0.set_zero(self._yannie_axis0.get_raw_pos())
        self._yannie_axis1.set_zero(self._yannie_axis1.get_raw_pos())

    def set_z_zero(self):
        self._xavier_axis1.set_zero(self._xavier_axis1.get_raw_pos())

    def is_x_busy(self):
        return self._xavier_axis0.is_busy()

    def is_y_busy(self):
        return self._yannie_axis0.is_busy() or self._yannie_axis1.is_busy()

    def is_z_busy(self):
        return self._xavier_axis1.is_busy()
