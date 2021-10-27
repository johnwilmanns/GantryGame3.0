import ODrive_Ease_Lib
import odrive


class Gantry:

    def __init__(self,odrv0_serial, odrv1_serial):

        self.odrv0_serial = "20793595524B" # Previously Xavier
        self.odrv1_serial = "20673593524B" # Previously Yannie


        self.odrv0 = odrive.find_any(serial_number=self.odrv0_serial)
        self.odrv1 = odrive.find_any(serial_number=self.odrv1_serial)

        self.x = ODrive_Ease_Lib.ODrive_Axis(self.odrv1.axis1) # X
        self.y = ODrive_Ease_Lib.ODrive_Axis(self.odrv0.axis0) # Y
        self.z = ODrive_Ease_Lib.ODrive_Axis(self.odrv0.axis1) # Z

    def startup(self):
        self.calibrate()
        self.home()
        self.print_positions()
        self.print_errors()


    def __del__(self):
        self._xavier.axis0.requested_state = 1
        self._xavier.axis1.requested_state = 1
        self._yannie.axis1.requested_state = 1

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

    def home(self):

        self.x.scuffed_home()
        self.y.scuffed_home()
        self.z.scuffed_home()

        self.set_x_zero()
        self.set_y_zero()
        self.set_z_zero()
        print("homed")

    def print_positions(self):
        print(f"X = {self.x}")
        print(f"Y = {self.y}")
        print(f"Z = {self.z}")


    



        
        

