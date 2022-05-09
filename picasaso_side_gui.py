from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import pickle
global edges
class MainWindow(Screen):
    def enter_code(self):
        #get list form pickle file
        global edges
        edges = pickle.load(open("~/Documents/paths/" + self.code + ".pkl", "rb"))



class SecondWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()