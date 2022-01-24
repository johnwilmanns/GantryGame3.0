import pyfirmata
import time

board = pyfirmata.Arduino('/dev/ttyACM0')
pwm = board.get_pin('d:9:p')

#puts the pen up
def pen_up():
    pwm.write(1) #writes pwm
    time.sleep(.1)

#puts the pen down
def pen_down():
    pwm.write(0) #writes pwm
    time.sleep(.1)
    
    
if __name__ == "__main__":
    while True:
        time.sleep(.1)
        pen_down()
        time.sleep(.1)
        pen_up()
        
