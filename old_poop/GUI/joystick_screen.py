from GUI.image_button import ImageButton
from GUI.joystick import Joystick
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.clock import Clock

class JoystickScreen(Screen):
    title_button = ObjectProperty(None)
    color_button = ObjectProperty(None)

    joystick = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(JoystickScreen, self).__init__(**kwargs)
        
    def on_enter(self):
        self.joystick.start_joystick()

    def on_leave(self, *args):
        self.joystick.stop_joystick()

