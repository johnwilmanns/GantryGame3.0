import gantry
import time


class Controller:

    def __init__(self):
        self.gantry = gantry.Gantry()
        self.gantry.startup()

    def set_pos(self, x, y, z):
        self.gantry.set_pos_noblock(x, y, z)
