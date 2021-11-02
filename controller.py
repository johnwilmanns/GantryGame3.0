import ODrive_Ease_Lib
import odrive
import time

class Gantry:

    def __init__(self):

        self.odrv1_serial = "20793595524B" # Previously Xavier
        self.odrv0_serial = "20673593524B" # Previously Yannie


        self.odrv1 = odrive.find_any(serial_number=self.odrv1_serial)
        self.odrv0 = odrive.find_any(serial_number=self.odrv0_serial)

        self.x = ODrive_Ease_Lib.Axis(self.odrv0.axis1) # X
        self.y = ODrive_Ease_Lib.Axis(self.odrv1.axis0) # Y
        self.z = ODrive_Ease_Lib.Axis(self.odrv1.axis1) # Z

    def startup(self):
        self.calibrate()
        self.home()
        self.print_positions()
        self.print_errors()


    def __del__(self):
        self.x.idle()
        self.y.idle()
        self.z.idle()

    def axes(self):
        yield self.x
        yield self.y
        yield self.z

    def print_errors(self):
        print(odrive.utils.dump_errors(self._xavier))
        print(odrive.utils.dump_errors(self._yannie))

    def calibrate(self):
        for motor in self.axes():
            motor.calibrate_no_hold()
        for motor in self.axes():
            motor.hold_until_calibrated()
        print("calibrated")

    def home(self, axis=[True, True, True]):
        print("homing")
        if axis[0]:  # x axis
            self.x.set_vel(1)
            while True:
                print(self.odrv0.get_gpio_states() & 0b00100)
                if self.odrv0.get_gpio_states() & 0b00100 == 0:  # needs to be changed upon rewire

                    self.x.set_vel(0)
                    self.x.set_home()
                    print("yes")
                    break
                time.sleep(.1)

        print("homed x")

        if axis[1]:  # axis
            self.y.set_vel(1)
            while True:
                print(self.odrv1.get_gpio_states() & 0b00100)
                if self.odrv1.get_gpio_states() & 0b00100 == 0:  # needs to be changed upon rewire

                    self.x.set_vel(0)
                    self.x.set_home()
                    print("yes")
                    break
                time.sleep(.1)

    def sensorless_home(self, home_axes = [True, True, True]):
        for num, axis in enumerate(self.axes()) :
            if home_axes[num]:
                axis.sensorless_home()



    def print_positions(self):
        print(f"X = {self.x}")
        print(f"Y = {self.y}")
        print(f"Z = {self.z}")


    



        
        

