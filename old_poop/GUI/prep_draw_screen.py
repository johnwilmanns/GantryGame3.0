from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.clock import Clock

from GUI.image_button import ImageButton

class PrepDrawScreen(Screen):

    back_button = ObjectProperty(None)
    draw_button = ObjectProperty(None)

    preview = ObjectProperty(None)

    current_drawing = {}

    def __init__(self, **kwargs):
        super(PrepDrawScreen, self).__init__(**kwargs)
        self.current_drawing = {}

    def on_pre_enter(self):
        print('/drawings/' + self.current_drawing['image_name'])
        self.preview.source = './drawings/images/' + self.current_drawing['image_name']
        self.return_scheduler = Clock.schedule_once(self.timeout, 60)

        self.draw_button.bind(on_release=self.start_draw)

    def on_touch_down(self, touch):
        super(PrepDrawScreen, self).on_touch_down(touch)
        Clock.unschedule(self.return_scheduler)
        print(self.current_drawing)
        self.return_scheduler = Clock.schedule_once(self.timeout, 60)

    def on_leave(self, *args):
        Clock.unschedule(self.return_scheduler)

    def timeout(self, *args):
        self.manager.transition.direction = 'down'
        self.manager.current = "main screen"

    def start_draw(self, instance):
        self.manager.get_screen('drawing screen').curr_draw = self.current_drawing
        self.manager.transition.direction = 'up'
        self.manager.current = 'drawing screen'



