from kivy.config import Config



from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from threading import Thread
from multiprocessing import Process
import cv2
import numpy as np  # used to flip array for properly mirrored output and picture taken
from time import sleep  # not needed, but could become necessary
import time
# import draw_image

import image_processing
import trajectory_planning

Config.set('graphics', 'fullscreen', '0')

# Config.set('graphics', 'width', '1280')
# Config.set('graphics', 'height', '800')

# Config.set('graphics', 'width', '1280')
# Config.set('graphics', 'height', '800')

Config.write()
# Config.set('graphics', 'width', '800')
# Config.set('graphics', 'height', '800')



import run_gantry

'''
GLOBALS
'''
pause = False  # pauses or unpauses the camera feed

isSamir = True
isNikhil = False

# to access the array of the picture being taken, call variable final_picture, might need try/except



'''
END GLOBALS
'''


class CamApp(App):  # build for kivy display
    
    def take_picture(self, picture):  # takes a picture, in a thread later on
        global pause
        # picture = cv2.VideoCapture(0)
        
        ret, frame = picture.read()
        # final_picture = np.fliplr(frame)
        # final_picture = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        # cv2.imwrite("/home/soft-dev/Documents/GantryGame3.0/picassopicture.png", final_picture)
        # cv2.imwrite("picassopicture.png", final_picture)
        
        # preview_image.main(final_picture)
        
        # picture.release()
        pause = True
        segments = image_processing.process_combo_raw(frame)
        self.segments = segments
    #     segments = trajectory_planning.calc_path(segments, 5, .01, 1, 120)
        self.final_picture = image_processing.plot_segments(segments) 
        
        return self.final_picture
    
    global isSamir, isNikhil
    '''
    Colors and Shading
    '''
    button_shade = 1
    button_paused_shade = 0.5

    picture_button_text = 'Take Image'
    retake_button_text = 'Retake Image'
    print_button_text = 'Print'

    picture_button_color = (1, 0, 1, button_shade)
    retake_button_color = (0, 0, 1, button_paused_shade)
    print_button_color = (0, 1, 0, button_paused_shade)

    button_font_size = 88
    Window.clearcolor = (1, 1, 1, 1)


    disable_all_buttons = False
    
    

    # extra
    x = Window.size[0]
    y = Window.size[1]

    # size_x = x/800
    # size_y = 120/y

    size_x = 1
    size_y = .1

    '''
    End Colors and Shading
    '''

    # def update_image(self):
    #     while True:
    #         self.current_image = self.capture.read()[1]




    def build(self):

        # start cv2stuff
        self.img1 = Image()
        layout = FloatLayout()
        layout.add_widget(self.img1)
        self.capture = cv2.VideoCapture(0)

        self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(width, height)

        # assert width == 1920 and height == 1080, "the res is wrong"

        self.segments = None
        self.final_picture = None
        Clock.schedule_interval(self.update, 1.0 / 33.0)

        # end cv2stuff
        def add_button(button: Button):
            layout.add_widget(button)
        def remove_button(button: Button):
            layout.remove_widget(button)

        def disable_all_text():
            picture_button.text = ''
            retake_button.text = ''
            print_button.text = ''

        def enable_all_text():
            picture_button.text = 'Take Image'
            retake_button.text = 'Retake Image'
            print_button.text = 'Print'

        def enable_text(button: Button):
            if button == picture_button:
                picture_button.text = 'Take Image'
            elif button == retake_button:
                retake_button.text = 'Retake Image'
            elif button == print_button:
                print_button.text = 'Print'
            else:
                print(str(button), 'not found, in enable_text. try adding this buttons or callingn ir correctly')

        def disable(button):  # allows to disable or enable a single button
            button.disabled = True
            button.background_color[-1] = self.button_paused_shade

        def enable(button):  # allows to disable or enable a single button
            button.disabled = False
            button.background_color[-1] = self.button_shade

        def ready_to_print():
            global pause
            add_button(picture_button)
            enable_all_text()
            pause = False

        def disable_all_buttons():
            for button in button_array:
                remove_button(button)

        def take_picture_button(instance):  # changes ui, starts thread to take picture, as defined in GLOBALS
            remove_button(picture_button)
            add_button(retake_button)
            # add_button(print_button)
            
            retake_button.text = "Processing..."
            # remove_button(print_button)
            

            print(self.x)
            print(self.y)

            # cv2.destroyAllWindows()
            # self.capture.release()

            # time.sleep(2)

            print('pic taken')
            
            # Process(target=self.take_picture, args=(self.capture,)).start()
            # self.take_picture(self.capture)
            # Thread(target=self.take_picture, args=(self.capture,)).start()
            # take_picture()
            
        def take_picture_button_2(instance):
            self.take_picture(self.capture)
            add_button(print_button)
            
            retake_button.text = "Retake Image"

        def retake_picture_button(instance):  # changes ui accordingly, pauses the camera
            remove_button(retake_button)
            add_button(picture_button)
            remove_button(print_button)
            global pause
            pause = False


        def printing():
            print('calculating traj')
            # print(self.segments)
            freq = 120
            segments = trajectory_planning.calc_path(self.segments, 10, 1, 1, freq)
            try:
                print("handing off to run gantry")
                run_gantry.main(segments, freq)
            except Exception as e:
                print(f'error \"{e}\" encountered while printing')
            sleep(5)
            ready_to_print()


        def thread_printing(instance): # disables all buttons upon print press
            disable_all_buttons()
            # Thread(target=printing).start()
            printing()


        picture_button = Button(size_hint_x=self.size_x, size_hint_y=self.size_y, text=self.picture_button_text,
                                font_size=self.button_font_size, on_press=take_picture_button, on_release=take_picture_button_2,
                                background_color=self.picture_button_color, pos=(0, 0),
                                disabled=self.disable_all_buttons)

        print_button = Button(pos_hint={'top':1}, size_hint_x=self.size_x, size_hint_y=self.size_y,
                              background_color=self.print_button_color,
                              on_press=thread_printing, font_size=self.button_font_size, text=self.print_button_text,
                              disabled=self.disable_all_buttons)

        retake_button = Button(size_hint_x=self.size_x, size_hint_y=self.size_y, text=self.retake_button_text,
                               font_size=self.button_font_size, on_press=retake_picture_button,
                               background_color=self.retake_button_color, pos=(0, 0),
                               disabled=self.disable_all_buttons)
        # ui may break upon entering the pi's screen size, will adjust to screen size later
        button_array = [picture_button, print_button, retake_button]



        temp_count = 1

        if temp_count  == 1:
            # layout.add_widget(retake_button)
            layout.add_widget(picture_button)
            # layout.add_widget(print_button)
            temp_count += 1

        return layout

    def update(self, dt):
        # print(1/dt)
        # global final_picture

        ret, frame = self.capture.read()

        if not pause:
            buf1 = cv2.flip(frame, 1)
            buf2 = cv2.flip(buf1, 0)

            buf = buf2.tostring()

            texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')  # see https://kivy.org/doc/stable/api-kivy.graphics.texture.html
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img1.texture = texture1
        if pause:
            try:
                
                buf1 = cv2.flip(self.final_picture, 1)
                buf2 = cv2.flip(buf1, 0)
                buf = buf2.tobytes()
                cv2.destroyAllWindows()
                texture1 = Texture.create(size=(self.final_picture.shape[1], self.final_picture.shape[0]), colorfmt='bgr')
                texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.img1.texture = texture1
            except NameError:  # occurs because variable final_image is not created yet (instantaneously)
                print("test")
                pass


if __name__ == '__main__':
    Window.size = (1280, 800)
    Window.maximize()
    CamApp().run()
    cv2.destroyAllWindows()
'''
https://kivy.org/doc/stable/api-kivy.uix.floatlayout.html
https://stackoverflow.com/questions/26773932/global-variable-is-undefined-at-the-module-level
https://stackoverflow.com/questions/3323001/what-is-the-maximum-recursion-depth-in-python-and-how-to-increase-it 
https://stackshare.io/numpy/alternatives
useful color calculator for kivy colors: https://corecoding.com/utilities/rgb-or-hex-to-float.php
'''
