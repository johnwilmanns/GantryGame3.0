from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
import pickle
global segments
import run_gantry

def show_popup():
    show = P() # Create a new instance of the P class

    popupWindow = Popup(title="Popup Window", content=show, size_hint=(None,None),size=(400,400))
    # Create the popup window

    popupWindow.open() # show the popup
class MainWindow(Screen):
    def enter_code(self):
        #get list form pickle file
        global segments
        try:
            segments = pickle.load(open("/home/soft-dev/Documents/paths/" + self.code.text + ".pkl", "rb"))
            self.code.text = ""
            run_gantry.main(segments)
        except Exception:
            show_popup()


class SecondWindow(Screen):
    pass

class P(FloatLayout):
    pass

class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("picasso_side_gui.kv")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()