from ODriveMotors import GGMotors

class Planner():

    drawer = None

    Z_UPPER = 700000
    Z_LOWER = 10000
    X_UPPER = -10000
    X_LOWER = -160500
    Y_UPPER = 83000
    Y_LOWER = 0

    @staticmethod
    def find_motors():
        Planner.drawer = GGMotors()

    def release():
        Planner.drawer.release()

    def grab():
        Planner.drawer.grab()

    def move_z(pos):
        if pos > Planner.Z_UPPER:
            Planner.drawer.set_z_pos_trap(Planner.drawer.Z_UPPER)
        elif pos < Planner.Z_LOWER:
            Planner.drawer.set_z_pos_trap(Planner.drawer.Z_LOWER)
        else:
            Planner.drawer.set_z_pos_trap(pos)

    def move_x(pos):
        if pos > Planner.X_UPPER:
            Planner.drawer.set_x_pos_trap(Planner.drawer.X_UPPER)
        elif pos < Planner.X_LOWER:
            Planner.drawer.set_x_pos_trap(Planner.drawer.X_LOWER)
        else:
            Planner.drawer.set_x_pos_trap(pos)

    def move_y(pos):
        if pos > Planner.Y_UPPER:
            Planner.drawer.set_y_pos_trap(Planner.drawer.Y_UPPER)
        elif pos < Planner.y_LOWER:
            Planner.drawer.set_y_pos_trap(Planner.drawer.Y_LOWER)
        else:
            Planner.drawer.set_y_pos_trap(pos)




