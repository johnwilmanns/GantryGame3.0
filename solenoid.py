import pyfirmata
import time

board = pyfirmata.Arduino('/dev/ttyACM0')
pwm = board.get_pin('d:9:p')

#puts the pen up
def pen_up():
    """ooga booga
    """    
    pwm.write(1) #writes pwm

#puts the pen down
def pen_down():
    pwm.write(0) #writes pwm
    
    
if __name__ == "__main__":
    while True:
        time.sleep(.02)
        pen_down()
        time.sleep(.05)
        pen_up()
        
