import pyfirmata
import time
# from pynput import keyboard
try:
    board = pyfirmata.Arduino('/dev/ttyUSB0')
except Exception:
    board = pyfirmata.Arduino('/dev/ttyUSB1')
    
# board = pyfirmata.Arduino('/dev/ttyUSB1')
    
pwm = board.get_pin('d:10:s')
pwm.write(90)
# pwm.write(1)
upval = 60
downval = 50



def set_manual(val):
    pwm.write(val)

#puts the pen up
def pen_up():
    # print("Pen up")
    pwm.write(upval) #writes pwm
    time.sleep(.05)


#puts the pen down
def pen_down():
    # print("pen down")
    pwm.write(downval) #writes pwm
    time.sleep(.05)

pen_up()

if __name__ == "__main__":

    
    while True:
        print("up")
        pen_up()    

        print("down")
        pen_down()


