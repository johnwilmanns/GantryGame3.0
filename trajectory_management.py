import time

class Manger:
    def __init__(self):
        self.x_goal = 0
        self.y_goal = 0
    def set_goal(self, x, y):
        self.x_goal = x
        self.y_goal = y
    def hold(self, new_x, new_y):
