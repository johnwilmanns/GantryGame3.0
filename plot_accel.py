from cProfile import label
from gantry import Gantry
import time
import matplotlib.pyplot as plt


gantry = Gantry()

gantry.startup()
gantry.enable_motors()

gantry.set_pos(0,0)

gantry.set_pos_noblock(7,7)

x_vals = []
y_vals = []
x_times = []
y_times = []

while True:
    x = gantry.x.get_pos()
    x_vals.append(x)
    x_times.append(time.time())
    
    y = gantry.y.get_pos()
    y_vals.append(y)
    y_times.append(time.time())

    if x > 4.95 and y > 4.95:
        break
    

# x_vals = [1,2,3,5]
# x_times = [0,1,2,3]

# y_vals = [2,3,4, 6]
# y_times = [0,1,2,3]

fig, axs = plt.subplots(3, 1)
axs[0].plot(x_times, x_vals, label = "X")
axs[0].plot(y_times, y_vals, label = "Y")
axs[0].legend()
axs[0].set_ylabel("position (in)")
axs[0].set_xlabel("time (s)")


dvx_vals = []
for ((x0, x1), (t0, t1)) in zip(zip(x_vals, x_vals[10:]), zip(x_times, x_times[10:])):
    dvx = (x1-x0)/(t1-t0)
    dvx_vals.append(dvx)
    
dvy_vals = []
for ((y0, y1), (t0, t1)) in zip(zip(y_vals, y_vals[10:]), zip(y_times, y_times[10:])):
    dvy = (y1-y0)/(t1-t0)
    dvy_vals.append(dvy)
    
# x_times.pop(0)
# y_times.pop(0)
x_times = x_times[10:]
y_times = y_times[10:]
    
axs[1].plot(x_times, dvx_vals, label = "X")
axs[1].plot(y_times, dvy_vals, label = "Y")
axs[1].legend()
axs[1].set_ylabel("velocity (in/s)")
axs[1].set_xlabel("time (s)")




dv2x_vals = []
for ((x0, x1), (t0, t1)) in zip(zip(dvx_vals, dvx_vals[10:]), zip(x_times, x_times[10:])):
    dv2x = (x1-x0)/(t1-t0)
    dv2x_vals.append(dv2x)
    
dv2y_vals = []
for ((y0, y1), (t0, t1)) in zip(zip(dvy_vals, dvy_vals[10:]), zip(y_times, y_times[10:])):
    dv2y = (y1-y0)/(t1-t0)
    dv2y_vals.append(dv2y)
    
x_times = x_times[10:]
y_times = y_times[10:]

axs[2].plot(x_times, dv2x_vals, label = "X")
axs[2].plot(y_times, dv2y_vals, label = "Y")
axs[2].legend()
axs[2].set_ylabel("acceleration (in/s^2)")
axs[2].set_xlabel("time (s)")

print(f"got {len(x_vals)} x measurements and {len(y_vals)} y measurements")
plt.show()
