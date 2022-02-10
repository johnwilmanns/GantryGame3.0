import pyfirmata
import time

board = pyfirmata.Arduino('/dev/ttyACM0')
pwm = board.get_pin('d:9:s')
pwm.write(180)

#puts the pen up
def pen_up():
    print("Pen up")
    pwm.write(100) #writes pwm
    time.sleep(.1)


#puts the pen down
def pen_down():
    print("pen down")
    pwm.write(80) #writes pwm
    time.sleep(.1)

    
def up_damp(delay=.015, hold_pow=.2):
    pwm.write(1)
    time.sleep(delay)
    pwm.write(hold_pow)
    
    
if __name__ == "__main__":
    while True:
        input()
        pen_up()
        input()
        pen_down()
        
