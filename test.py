import numpy as np
from pieces import Arc
import math

part = Arc((0,0), 1, 350, 20)


if part.end_angle - part.start_angle < -180:
    part.end_angle += 360
elif part.end_angle - part.start_angle > 180:
    part.end_angle -= 360

angle_step = 10
n = math.ceil(abs(part.end_angle-part.start_angle)/angle_step)
stepsize = (part.end_angle-part.start_angle)/n

if part.start_angle < part.end_angle:
    dir = 1
else:
    dir = -1

print(np.arange(part.start_angle, part.end_angle, stepsize))

pairs = [[val, val+stepsize] for val in np.linspace(part.start_angle, part.end_angle-stepsize, n)]

print(pairs)
arcs = []
for pair in pairs:
    arcs.append(Arc(part.center_pos, part.radius, pair[0], pair[1]))

# print(arcs)
# print(pairs)
# print(angle_pairs)