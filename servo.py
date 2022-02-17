import pyfirmata
import time
from pynput import keyboard

board = pyfirmata.Arduino('/dev/ttyACM1')
pwm = board.get_pin('d:9:s')
pwm.write(0)

upval = 108
downval = 100

def set_up():
    global upval
    print("setting up")
    pen_up()
    with keyboard.Events() as events:
        for event in events:
            if event.key == keyboard.Key.enter and str(event)[0] == "P":
                break
            elif event.key == keyboard.Key.up and str(event)[0] == "P":
                upval-=1
            elif event.key == keyboard.Key.down and str(event)[0] == "P":
                upval+=1
            print(upval)
            pen_up()
            
            
def set_down():
    global downval
    print("setting down")
    pen_down()
    with keyboard.Events() as events:
        for event in events:
            if event.key == keyboard.Key.enter and str(event)[0] == "P":
                break
            elif event.key == keyboard.Key.up and str(event)[0] == "P":
                downval-=1
            elif event.key == keyboard.Key.down and str(event)[0] == "P":
                downval+=1
            print(downval)
            pen_down()

#puts the pen up
def pen_up():
    # print("Pen up")
    pwm.write(upval) #writes pwm
    time.sleep(.1)


#puts the pen down
def pen_down():
    # print("pen down")
    pwm.write(downval) #writes pwm
    time.sleep(.1)


if __name__ == "__main__":
    set_up()

