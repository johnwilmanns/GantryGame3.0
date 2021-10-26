from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from planner import Planner

import pygame.joystick
import pygame.event
import math
import os

kp = 10.0
ki = 0.0008
kd = 0.0

class Joystick(FloatLayout):

    def __init__(self, **kwargs):
        super(Joystick, self).__init__(**kwargs)
        os.environ['SDL_VIDEODRIVER']="dummy"
        pygame.display.init()
        pygame.joystick.init()
        self.left_joy = pygame.joystick.Joystick(0)
        self.left_joy.init()

    def start_joystick(self):
        Clock.schedule_interval(self.update, 1/30)

    def stop_joystick(self):
        Clock.unschedule(self.update)
        Planner.drawer.return_pen()
        while(Planner.drawer.holding_pen != 0):
            pass
        Planner.drawer.center()

    def update(self, delta_time):
        pygame.event.pump()
        x_tilt = self.left_joy.get_axis(0)
        y_tilt = self.left_joy.get_axis(1)
        if abs(math.sqrt((x_tilt * x_tilt) + (y_tilt * y_tilt))) > 0.15:
            if x_tilt > 0 and Planner.drawer.get_x_pos() < -110000:
                Planner.drawer.set_x_vel_no_pid(0)
            elif x_tilt < 0 and Planner.drawer.get_x_pos() > 0:
                Planner.drawer.set_x_vel_no_pid(0)
            else:
                Planner.drawer.set_x_vel_no_pid(-40000 * x_tilt)

            if y_tilt > 0 and Planner.drawer.get_y_pos() > 70000:
                Planner.drawer.set_y_vel_no_pid(0)
            elif y_tilt < 0 and Planner.drawer.get_y_pos() < 0:
                Planner.drawer.set_y_vel_no_pid(0)
            else:
                curr_diff = Planner.drawer._yannie_axis0.get_pos() - Planner.drawer._yannie_axis1.get_pos()
                targ_vel = 40000 * y_tilt
                Planner.drawer._yannie_axis0.set_vel(targ_vel - curr_diff * kp)
                Planner.drawer._yannie_axis1.set_vel(targ_vel + curr_diff * kp)
        else:
            Planner.drawer.set_x_vel_no_pid(0)
            Planner.drawer.set_y_vel_no_pid(0)

        if self.left_joy.get_button(2) and Planner.drawer.get_z_pos() > Planner.drawer.Z_TOUCH:
            Planner.drawer.set_z_vel_no_pid(-500000)
        elif Planner.drawer.get_z_pos() < Planner.drawer.Z_HOVER and not self.left_joy.get_button(2):
            Planner.drawer.set_z_vel_no_pid(500000)
        else:
            Planner.drawer.set_z_vel_no_pid(0)

        if self.left_joy.get_button(2):
            print('hmmmm')



