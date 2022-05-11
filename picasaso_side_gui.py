from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

import pickle
global segments
import run_gantry
class MainWindow(Screen):
    def enter_code(self):
        #get list form pickle file
        global segments
        try:
            segments = pickle.load(open("/home/soft-dev/Documents/paths/" + self.code.text + ".pkl", "rb"))
            self.code.text = ""
            run_gantry.main(segments)
        except Exception:
            layout = GridLayout(cols=1, padding=10)

            popupLabel = Label(text="Invalid Code, Please try again")
            closeButton = Button(text="Close")

            layout.add_widget(popupLabel)
            layout.add_widget(closeButton)

            # Instantiate the modal popup and display
            popup = Popup(title='Failed',
                          content=layout)
            popup.open()

            # Attach close button press with popup.dismiss action
            closeButton.bind(on_press=popup.dismiss)

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