from gantry import Gantry
import time
"""VARIABLES"""

x_range = 10
y_range = 8
trial_runs = 10


gantry = Gantry()

gantry.startup()

x_accel = []
y_accel = []
gantry.enable_motors()
for i in range(trial_runs):
    gantry.set_pos(1, 1)
    time.sleep(.02)
    t0 = time.perf_counter()
    oldx = gantry.x.get_pos()
    oldy = gantry.y.get_pos()
    while time.perf_counter() - t0 < .1:
        pass
    x_accel.append( abs(2 * (gantry.x.get_pos() - oldx) / ((t0-time.perf_counter())**2)))
    y_accel.append( abs(2 * (gantry.y.get_pos() - oldy) / ((t0-time.perf_counter())**2)))

    time.sleep(.5)
    gantry.set_pos(1 + x_range, 1+y_range)
    time.sleep(.02)
    t0 = time.perf_counter()
    oldx = gantry.x.get_pos()
    oldy = gantry.y.get_pos()
    while time.perf_counter() - t0 < .1:
        pass
    x_accel.append( abs(2 * (gantry.x.get_pos() - oldx) / ((t0-time.perf_counter())**2)))
    y_accel.append( abs(2 * (gantry.y.get_pos() - oldy) / ((t0-time.perf_counter())**2)))

print(f"Average x accel = {sum(x_accel) / len(x_accel)}, lowest x accel = {min(x_accel)}")
print(f"Average y accel = {sum(y_accel) / len(y_accel)}, lowest y accel = {min(y_accel)}")
