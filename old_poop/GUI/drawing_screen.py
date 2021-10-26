from kivy.uix.screenmanager import Screen

from planner import Planner
from GUI.image_button import ImageButton

class DrawingScreen(Screen):

    curr_draw = {}

    def __init__(self, **kwargs):
        super(DrawingScreen, self).__init__(**kwargs)
        self.curr_draw = {}

    def on_enter(self):
        Planner.drawer.draw_from_file(self.curr_draw['file_name'], vel=20000, dt=0.005)
        self.manager.transition.direction = 'down'
        self.manager.current = 'gallery screen'
