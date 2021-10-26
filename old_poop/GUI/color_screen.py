from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.clock import Clock

import time

from GUI.image_button import ImageButton
from planner import Planner

class ColorScreen(Screen):
    back_button = ObjectProperty(None)
    
    red_button = ObjectProperty(None)
    orange_button = ObjectProperty(None)
    yellow_button = ObjectProperty(None)
    green_button = ObjectProperty(None)
    blue_button = ObjectProperty(None)
    purple_button = ObjectProperty(None)
    
    light_blue_button = ObjectProperty(None)
    lime_green_button = ObjectProperty(None)
    red_orange_button = ObjectProperty(None)
    pink_button = ObjectProperty(None)
    lilac_button = ObjectProperty(None)
    black_button = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ColorScreen, self).__init__(**kwargs)

    def on_pre_enter(self):
        self.return_scheduler = Clock.schedule_once(self.timeout, 60)

    def on_enter(self):

        time.sleep(8)

        self.red_button.bind(on_release=self.change_color)
        self.orange_button.bind(on_release=self.change_color)
        self.yellow_button.bind(on_release=self.change_color)
        self.green_button.bind(on_release=self.change_color)
        self.blue_button.bind(on_release=self.change_color)
        self.purple_button.bind(on_release=self.change_color)
        self.light_blue_button.bind(on_release=self.change_color)
        self.lime_green_button.bind(on_release=self.change_color)
        self.red_orange_button.bind(on_release=self.change_color)
        self.pink_button.bind(on_release=self.change_color)
        self.lilac_button.bind(on_release=self.change_color)
        self.black_button.bind(on_release=self.change_color)



    def on_touch_down(self, touch):
        super(ColorScreen, self).on_touch_down(touch)
        Clock.unschedule(self.return_scheduler)
        self.return_scheduler = Clock.schedule_once(self.timeout, 60)

    def on_leave(self, *args):
        Clock.unschedule(self.return_scheduler)
        
    def timeout(self, *args):
        self.manager.transition.direction = 'down'
        self.manager.current = 'main screen'

    def change_color(self, instance):
        Planner.drawer.switch_pen_to_color(instance.col_str)
        self.manager.transition.direction = 'down'
        self.manager.current = 'joystick screen'
