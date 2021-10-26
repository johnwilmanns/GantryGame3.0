import kivy
# kivy.require('1.0.10')
import os
import json

os.environ['KIVY_WINDOW'] = 'egl_rpi'

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, TransitionBase
from GUI.gallery_screen import GalleryScreen
from GUI.prep_draw_screen import PrepDrawScreen
from GUI.main_screen import MainScreen
from GUI.drawing_screen import DrawingScreen
from GUI.color_screen import ColorScreen
from GUI.joystick_screen import JoystickScreen
from kivy.lang import Builder
from kivy.factory import Factory

from planner import Planner
Builder.load_file("main.kv")
Factory.register('ImageButton', module='GUI.image_button')

Planner.find_motors()
curr_step = 0
with open('poo_poo.json', 'r') as stepper_pos_file:
    curr_step = json.loads(stepper_pos_file.read())
Planner.drawer._holder.go_to_position(-curr_step['step_pos'])
Planner.drawer._holder.set_as_home()

class MyApp(App):
    def build(self):
        TransitionBase.duration = 1
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main screen"))
        sm.add_widget(GalleryScreen(name="gallery screen"))
        sm.add_widget(PrepDrawScreen(name="prep draw screen"))
        sm.add_widget(JoystickScreen(name="joystick screen"))
        sm.add_widget(ColorScreen(name='color screen'))
        sm.add_widget(DrawingScreen(name='drawing screen'))
        sm.current = "main screen"
        return sm

if __name__ == '__main__':
    try:
        MyApp().run()
    finally:
        with open('poo_poo.json', 'w') as stepper_pos_file:
            json.dump({"step_pos": Planner.drawer._holder.getPosition()}, stepper_pos_file)

