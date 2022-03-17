import run_gantry
import trajectory_planning
import time
import numpy as np
WIDTH = .025
F = 60

g = run_gantry.gantry

input("move to start corner")
start = (g.x.get_pos(), g.y.get_pos())
print(start)



input("move to end corner")
end = (g.x.get_pos(), g.y.get_pos())
print(end)

segments = []
for y in np.arange(start[1], end[1], WIDTH*2):
    segments.append([(start[0], y), (end[0], y)])
    segments.append([(end[0], y+.5*WIDTH), (start[0], y+.5*WIDTH)])
    
print(segments)
segments = trajectory_planning.calc_path(segments, 5, 1, 0, F)
segments.reverse()



print(segments)


run_gantry.main(segments, F)