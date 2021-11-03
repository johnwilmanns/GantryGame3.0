import controller
import time

class Controller:

    def __init__(self):
        self.gantry = controller.Gantry()
        self.gantry.startup()

    def set_pos(self, x, y, z):
        self.gantry.set_pos(x, y, z)