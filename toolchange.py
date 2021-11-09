import spidev
import os
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers

spi = spidev.SpiDev()




def main():
    try:
        holder = stepper(port=0, micro_steps=64, speed=200)

        curr_step = 0
        # holder.go_to_position(-curr_step['step_pos'])
        holder.set_as_home()

        holder.set_max_speed(300)
        holder.set_speed(110)
        holder.set_micro_steps(64)

        while True:

            text = input("r/g")

            if text == "r":
                curr_step+= 600
                holder.go_to_position(curr_step)
            elif text == "g":
                curr_step -= 600
                holder.go_to_position(curr_step)

    finally:
        pass


if __name__ == "__main__":
    main()