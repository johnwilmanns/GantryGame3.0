from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.config import Config

from kivy.uix.label import Label
import trajectory_planning
import multiprocessing as mp
import time
import pickle
import subprocess
import os
import cv2
import image_processing

global image_number
# may allah forgive me for how I am dealing with the images
global new_image
def remake_edges(blur_radius = 11, lower_thresh = 0, upper_thresh = 20, aperture_size = 3, bind_dist = 10, area_cut = 3,
        min_len = 20, calc_rogues = False, blur_radius_shade = 21, line_dist = 5, theta = None, bind_dist_shade = 10, area_cut_shade = 10,
        min_len_shade = 10, thresholds = [10, 30, 50, 80]):
    """
    Remakes the edges image using the given parameters.
    """
    filename = "image.png"
    frame = cv2.imread(filename)

    segments = image_processing.process_combo_raw(frame, blur_radius, lower_thresh, upper_thresh, aperture_size, bind_dist, area_cut, min_len, calc_rogues, blur_radius_shade, line_dist, theta, bind_dist_shade, area_cut_shade, min_len_shade, thresholds) #if this line is wrong its github copilots fault
    #     segments = trajectory_planning.calc_path(segments, 5, .01, 1, 120)
    edges_image = image_processing.plot_segments(segments)
    cv2.imwrite("edges_image.jpg", edges_image)
    def cri(segments):

        segments = trajectory_planning.calc_path(segments, 10, 1, 1, 120)
        #pickle the segments
        with open("segments.pkl", "wb") as f:
            pickle.dump(segments, f)
        print("pickled segments")
    p = mp.Process(target=cri, args=(segments,))
    p.start()


def transfer_path():
    global image_number
    image_number += 1
    def pp(image_number):

        os.system('scp segments.pkl soft-dev@gantry-game.local:~/Documents/paths/' + str(image_number) + '.pkl')

    pee = mp.Process(target=pp, args=(image_number,))
    pee.start()
    return image_number
class MainWindow(Screen):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        global new_image
        new_image = True
        camera = self.ids['camera']
        print(self.ids)
        camera.export_to_png("image.png")

        print("Captured")
        remake_edges()







class SecondWindow(Screen):
    def save(self):
        global new_image
        layout = GridLayout(cols=1, padding=10)

        popupLabel = Label(text="Your code is " + str(transfer_path()))
        closeButton = Button(text="Close")

        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)

        # Instantiate the modal popup and display
        popup = Popup(title='Saved!',
                      content=layout)
        popup.open()

        # Attach close button press with popup.dismiss action
        closeButton.bind(on_press=popup.dismiss)
        popup.open()
        new_image = True
class AjustmentWindow(Screen):
    def update_values(self):
        remake_edges(blur_radius= self.blur_radius.value, upper_thresh=self.edge_sensitivity.value, min_len= self.min_len.value)
    def enter(self):
        global new_image
        if new_image:
            self.blur_radius.value = 11
            self.edge_sensitivity.value = 20
            self.min_len.value = 20
            new_image = False



class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("photo_booth.kv")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    global image_number
    global new_image
    image_number = 1000
    new_image = True
    MyMainApp().run()