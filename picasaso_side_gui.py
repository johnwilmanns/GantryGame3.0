from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import pickle
global segments
import run_gantry
class MainWindow(Screen):
    def enter_code(self):
        #get list form pickle file
        global segments
        segments = pickle.load(open("/home/soft-dev/Documents/paths/" + self.code.text + ".pkl", "rb"))
        self.code.text = ""
        run_gantry.main(segments)


class SecondWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("picasso_side_gui.kv")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()