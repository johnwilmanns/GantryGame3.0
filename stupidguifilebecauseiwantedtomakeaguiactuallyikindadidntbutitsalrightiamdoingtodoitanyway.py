import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import controller


class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        self.controller = controller.Controller

        super(MyGrid, self).__init__(**kwargs)
        self.cols = 1

        self.x = GridLayout()
        self.x.cols = 2

        self.x.add_widget(Label(text="x: "))
        self.y = TextInput(multiline=False)
        self.x.add_widget(self.y)

        self.x.add_widget(Label(text="Y: "))
        self.lastName = TextInput(multiline=False)
        self.x.add_widget(self.lastName)

        self.x.add_widget(Label(text="Z: "))
        self.z = TextInput(multiline=False)
        self.x.add_widget(self.z)

        self.add_widget(self.x)

        self.go = Button(text="Go", font_size=40)
        self.go.bind(on_press=self.pressed)
        self.add_widget(self.go)

    def pressed(self, instance):


class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()