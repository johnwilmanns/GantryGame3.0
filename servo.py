import pyfirmata
import time
# from pynput import keyboard
try:
    board = pyfirmata.Arduino('/dev/ttyUSB0')
except Exception:
    board = pyfirmata.Arduino('/dev/ttyUSB1')
    
# board = pyfirmata.Arduino('/dev/ttyUSB1')

iterator = pyfirmata.util.Iterator(board)
iterator.start()

time.sleep(1)
    
pen = board.get_pin('d:10:s')
lock = board.get_pin('d:9:s')
limit_switch = board.get_pin('d:2:i')

limit_switch.enable_reporting()


# pen.write(90)
# pwm.write(1)

PEN_UP = 25
PEN_DOWN = 34

LOCK = 180
UNLOCK = 0

def lock_open():
    lock.write(UNLOCK)

def lock_close():
    if is_closed():
        lock.write(LOCK)
    else:
        raise Exception("Limit switch not closed")


def pen_high_up():
    pen.write(10)
    time.sleep(.05)

def pen_up():
    pen.write(PEN_UP)
    time.sleep(.05)


def pen_down():
    pen.write(PEN_DOWN) #writes pwm
    time.sleep(.05)
    
def is_closed():
    return not limit_switch.read()


pen_high_up()

if __name__ == "__main__":
    pass
    # while True:
    #     val = input("a/b")
    #     if val == 'a':
    #         lock_open()
    #     if val == 'b':
    #         lock_close()
    # pen_down()
    # time.sleep(20)
    # print("pen up")
    # time.sleep(5)
    # pen_down()



