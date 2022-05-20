from threading import Thread

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.label import Label

# Imports for Cesars code
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.lang import Builder

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
global image

SCREEN_MANAGER = ScreenManager()
#add names here
SECOND_SCREEN_NAME = 'second'

def remake_edges(blur_radius=11, lower_thresh=0, upper_thresh=20, aperture_size=3, bind_dist=10, area_cut=3,
                 min_len=20, calc_rogues=False, blur_radius_shade=21, line_dist=5, theta=None, bind_dist_shade=10,
                 area_cut_shade=10,
                 min_len_shade=10, thresholds=[10, 30, 50, 80]):
    """
    Remakes the edges image using the given parameters.
    """
    print("remaking edges")
    global image
    # filename = "image.png"
    # frame = cv2.imread(filename)

    frame = image
    segments = image_processing.process_combo_raw(frame, blur_radius, lower_thresh, upper_thresh, aperture_size,
                                                  bind_dist, area_cut, min_len, calc_rogues, blur_radius_shade,
                                                  line_dist, theta, bind_dist_shade, area_cut_shade, min_len_shade,
                                                  thresholds)  # if this line is wrong its github copilots fault
    #     segments = trajectory_planning.calc_path(segments, 5, .01, 1, 120)
    edges_image = image_processing.plot_segments(segments)
    cv2.imwrite("edges_image.jpg", edges_image)

    def cri(segments):
        segments = trajectory_planning.calc_path(segments, 10, 1, 1, 120)
        # pickle the segments
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

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        # opencv2 stuffs
        # self.capture = cv2.VideoCapture(0, cv2.CAP_V4L)
        # self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        # self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        # self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(width, height)
        Clock.schedule_interval(self.update, 1.0 / 33.0)

    def update(self, dt):
        # display image from cam in opencv window
        ret, frame = self.capture.read()
        # convert it to texture
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        # if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer.
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.ids.img1.texture = texture1
        self.ids.img1.size_hint_x = .5
        self.ids.img1.size_hint_y = .5
        self.ids.img1.pos_hint = {'center_x': .5, 'center_y': .5}

        # print(1 / dt)



    def take_picture_thread(self):
        # Clock.schedule_once(self.take_picture, .1)
        Thread(target=self.take_picture).start()

    def take_picture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''

        # print("taking image")

        global new_image
        new_image = True

        global image

        self.take_picture_button.text = "3"
        time.sleep(1)
        self.take_picture_button.text = "2"
        time.sleep(1)
        self.take_picture_button.text = "1"
        time.sleep(1)
        _, image = self.capture.read()
        # camera = self.ids['camera']
        # print(self.ids)
        # camera.export_to_png("image.png")
        #
        # print("Captured")
        self.take_picture_button.text = "CHEESE"
        remake_edges()
        Clock.schedule_once(self.switch_to_second_screen, 0)
        self.take_picture_button.text = "TAKE PICTURE"

    def switch_to_second_screen(self, dt):
        SCREEN_MANAGER.current = SECOND_SCREEN_NAME
        SCREEN_MANAGER.transition.direction = "up"


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
        remake_edges(blur_radius=self.blur_radius.value, upper_thresh=self.edge_sensitivity.value,
                     min_len=self.min_len.value, thresholds=[int(self.threshold1.value), int(self.threshold2.value), int(self.threshold3.value), int(self.threshold4.value)])

    def enter(self):
        global new_image
        if new_image:
            self.reset_values()
        new_image = False

    def reset_values(self):
        self.blur_radius.value = 11
        self.edge_sensitivity.value = 20
        self.min_len.value = 20
        self.threshold1.value = 10
        self.threshold2.value = 30
        self.threshold3.value = 50
        self.threshold4.value = 80

class WindowManager(ScreenManager):
    pass


Builder.load_file("photo_booth.kv")
SCREEN_MANAGER.add_widget(MainWindow(name="main"))
SCREEN_MANAGER.add_widget(SecondWindow(name="second"))
SCREEN_MANAGER.add_widget(AjustmentWindow(name="ajustment"))

class MyMainApp(App):
    def build(self):
        return SCREEN_MANAGER


if __name__ == "__main__":
    global image_number
    global new_image
    image_number = 1000
    new_image = True
    MyMainApp().run()
