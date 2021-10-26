import json

from GUI.gallery import Gallery, DrawingButton
from GUI.image_button import ImageButton
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.clock import Clock

class GalleryScreen(Screen):
    title_button = ObjectProperty(None)
    prev_button = ObjectProperty(None)
    next_button = ObjectProperty(None)

    gallery = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(GalleryScreen, self).__init__(**kwargs)
        self.drawings = []
        with open("./drawings/drawings.json") as d:
            unsorted_drawings = json.loads(d.read())
            self.drawings = sorted(unsorted_drawings, key=lambda kv: kv["title"])
        self.displayed = 0
        self.gallery_length = len(self.drawings)

    def on_pre_enter(self):
        self.prev_button.bind(on_release=self.prev_gallery)
        self.next_button.bind(on_release=self.next_gallery)
        self.gallery.generate_buttons(self.drawings)

        for button in self.gallery.buttons_list:
            button.bind(on_release=self.select_drawing)

        self.gallery.display_buttons(self.displayed)
        self.prev_button.disabled = True
        if self.gallery_length <= 4:
            self.next_button.disabled = True

        self.return_scheduler = Clock.schedule_once(self.timeout, 60)

    def on_touch_down(self, touch):
        super(GalleryScreen, self).on_touch_down(touch)
        Clock.unschedule(self.return_scheduler)
        self.return_scheduler = Clock.schedule_once(self.timeout, 60)

    def on_leave(self, *args):
        Clock.unschedule(self.return_scheduler)
        self.gallery.display_buttons(self.displayed)

    def timeout(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'main screen'
    
    def select_drawing(self, instance):
        self.manager.get_screen('prep draw screen').current_drawing = instance.drawing
        self.manager.transition.direction = 'up'
        self.manager.current = 'prep draw screen'

    def prev_gallery(self, value):
        print('help')
        self.next_button.disabled = True
        self.prev_button.disabled = True
        self.gallery.display_buttons(self.displayed - 1)
        self.displayed -= 1
        self.next_button.disabled = False
        if self.displayed != 0:
            self.prev_button.disabled = False

    def next_gallery(self, value):
        print('help')
        self.next_button.disabled = True
        self.prev_button.disabled = True
        self.gallery.display_buttons(self.displayed + 1)
        self.displayed += 1
        self.prev_button.disabled = False
        if (self.displayed + 1) * 4 < self.gallery_length:
            self.next_button.disabled = False

