import json

from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from GUI.image_button import ImageButton
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior

class Gallery(GridLayout):
    
    def __init__(self, **kwargs):
        super(Gallery, self).__init__(**kwargs)
        self.current_display = 0
        self.buttons_list = []
        
    def generate_buttons(self, drawings_list):
        self.clear_widgets()

        self.buttons_list = []

        for drawing in drawings_list:
            button = DrawingButton(drawing)
            self.buttons_list.append(button)

        

    def display_buttons(self, display_index):
        if display_index * 4 > len(self.buttons_list):
            print("Not enough buttons")
            return False

        self.clear_widgets()

        for x in range(display_index * 4, display_index * 4 + 4):
            self.add_widget(self.buttons_list[x])

        self.current_display = display_index




class DrawingButton(Button):

    preview = ObjectProperty(None)

    def __init__(self, drawing, **kwargs):
        super(DrawingButton, self).__init__(**kwargs)
        self.drawing = drawing
        self.preview.source = "./drawings/images/" + drawing["image_name"]
        

