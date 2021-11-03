import controller
import time

class Controller:

    def __init__(self):
        gantry = controller.Gantry()
        gantry.startup()

