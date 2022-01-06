import numpy as np
from full_path_planning import chunks_to_points, plot_path
from pieces import Arc
import math

part = Arc((0,0), 1, 90, 20)


angle_step = 2
n = math.ceil(abs(part.angle_delta)/angle_step)
stepsize = (part.angle_delta)/n
vals = np.arange(part.start_angle, part.start_angle+part.angle_delta, stepsize)

# pairs = [[val % 360, stepsize] for val in np.linspace(part.start_angle, part.start_angle+part.angle_delta-stepsize, n)]

print("split into :", len(vals))
arcs = []  
for val in vals:
    arcs.append(Arc(part.center_pos, part.radius, val, stepsize))

# parts[i:i+1] = arcs

print(vals)


for arc in arcs:
    arc.start_vel = 1
    arc.acceleration = 0

points, time = chunks_to_points(arcs, 60)

print()
plot_path(points)
# print(pairs)
# print(angle_pairs)