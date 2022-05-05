from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
import time


import cv2
import image_processing

global edges_image

# may allah forgive me for how I am dealing with the images

class MainWindow(Screen):
    def capture(self):
        global edges_image
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        camera.export_to_png("image.png")

        print("Captured")

        filename = "image.png"
        frame = cv2.imread(filename)

        segments = image_processing.process_combo_raw(frame)

        #     segments = trajectory_planning.calc_path(segments, 5, .01, 1, 120)
        edges_image = image_processing.plot_segments(segments)

        cv2.imwrite("edges_image.jpg", edges_image)






class SecondWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("photo_booth.kv")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()