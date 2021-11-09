import spidev
import os
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers

spi = spidev.SpiDev()

import json


def main():
    try:
        holder = stepper(port=0, micro_steps=64, speed=200)

        def release():
            holder.go_to_position(0)

        def grab():
            holder.go_to_position(600)

        curr_step = 0
        with open('poo_poo.json', 'r') as stepper_pos_file:
            curr_step = json.loads(stepper_pos_file.read())
        holder.go_to_position(-curr_step['step_pos'])
        holder.set_as_home()

        holder.set_max_speed(300)
        holder.set_speed(110)
        holder.set_micro_steps(64)

        while True:

            text = input("release/grab")

            if text == "release":
                release()
            elif text == "grab":
                grab()

    finally:
        with open('poo_poo.json', 'w') as stepper_pos_file:
            json.dump({"step_pos": holder.getPosition()}, stepper_pos_file)


if __name__ == "__main__":
    main()