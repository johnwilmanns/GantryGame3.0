from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty

class ImageButton(ButtonBehavior, Image):
    
    released_src = StringProperty("GUI/images/freehand.png")
    pressed_src = StringProperty("GUI/images/freehand.png")

    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.bind(state=self.image_check)
        self.allow_stretch = True

    def image_check(self, instance, value):
        if value == 'down':
            self.released_src = self.source
            self.source = self.pressed_src
        else:
            self.source = self.released_src
        

