import math
import numpy as np
from pieces import Line, Arc, sin, cos

seg = [(0,0), (1,0), (1,1), (2,1)]
# seg = [(0,0), (0,1), (1,1), (1,2)]

def distance(x1, y1, x2, y2):
    return (((x2-x1) ** 2 + (y2 - y1) ** 2) ** .5)




def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang




def calc_segment(seg, max_accel, max_radius, john = "dumb"):

    # R = V^2/A

    points = []
    parts = []



    for i in range(len(seg)-2):
        a, b, c = seg[i:i+3]

        ab_dist = distance(*a, *b)
        bc_dist = distance(*b, *c)

        # if ab_dist == 0:
        #     continue

        abc_angle = getAngle(a,b,c)

        if abc_angle == 180 or abc_angle == 360 or abc_angle == 0:
            l = ab_dist
            r = 0
            lr = 0
            
            parts.append(Line(a, b))
            
        else:
            # l = (max_accel * ab_dist - velocity ** 2) / (3 * max_accel) # math n shit
            if i == 0:
                lr = min(ab_dist/2, bc_dist/2)
            else:
                lr = min(ab_dist, bc_dist/2) #TODO: decide if max radius should govrn lr or r
            r = (2 * sin(abc_angle/2) * lr) / abs(2 * sin(90-abc_angle/2))
            
            if r > max_radius:
                r = max_radius
                lr = (r * abs(2 * sin(90 - abc_angle/2)))/ (2 * sin(abc_angle/2))

            l = ab_dist - lr
            
            

            print(f"{r = }, {l = }")

            ratio = l/ab_dist
            end_pos = (a[0] * (1-ratio) + b[0] * ratio, a[1] * (1-ratio) + b[1] * ratio)

            ratio2 = lr/bc_dist
            new_pos = (b[0] * (1-ratio2) + c[0] * ratio2, b[1] * (1-ratio2) + c[1] * ratio2)

            seg[i+1] = new_pos

            # points += line_points(a, end_pos, 100)

            if a != end_pos:
                parts.append(Line(a, end_pos))



            shifter = (-(b[1]-a[1])/ab_dist * r, (b[0]-a[0])/ab_dist *r)
            circle_center = None
            if abc_angle > 180:
                circle_center = (end_pos[0]+shifter[0], end_pos[1]+shifter[1])
            elif abc_angle < 180:
                circle_center = (end_pos[0]-shifter[0], end_pos[1]-shifter[1])
            

            if circle_center:
                # points += [circle_center] # make sure axe dis shit
                circle_center_offset = (circle_center[0]+1, circle_center[1])
                # points += arc_points(circle_center, r, getAngle(circle_center_offset, circle_center, end_pos), getAngle(circle_center_offset, circle_center, new_pos), 100)
                parts.append(Arc(circle_center, r, getAngle(circle_center_offset, circle_center, end_pos), getAngle(circle_center_offset, circle_center, new_pos)))


    parts.append(Line(*seg[-2:]))

    #Add a thing that collapses lines


    print(parts[0])
    def get_recent_vel(index):
        if index == 0:
            return 0
        for part in reversed(parts[:index]):
            if isinstance(part, Line):
                return part.end_vel
        return 0

    def get_ratio(va, vb, a, l):
        return (vb ** 2 - va ** 2)/(4* a * l) + 1/2

    def ratio_points(point1, point2, ratio):
        return (point1[0] * (1-ratio) + point2[0] * ratio, point1[1] * (1-ratio) + point2[1] * ratio)

    def decelerate_to_from(max_vel, index):
        assert index >= 0

        print(f"deceling from {index}")
        


        if isinstance(parts[index], Line):
            start_val = parts[index].set_end_vel(max_vel, max_accel)

            # exit()
            if start_val is not None:
                decelerate_to_from(start_val, index-1)
        else:
            decelerate_to_from(max_vel, index-1)
        # current_vel = None
        # for part in reversed(parts[:i]):
        #     if isinstance(part, Line):
        #         part.set_end_vel(max_vel, max_accel)


    for i, part in enumerate(parts):
        if isinstance(part, Line):
            part.start_vel = get_recent_vel(i)
            part.acceleration = max_accel
        elif isinstance(part, Arc):

            max_speed = part.max_speed(max_accel)
            if max_speed < get_recent_vel(i): #This is obsolete?
                # print(f"part {i} is goin way too fast at {get_recent_vel(i)} bucko, should be {max_speed}")

                decelerate_to_from(max_speed, i-1)
        else:
            raise "ouoeuoeuoe"
    
    # print(parts)

    def optimize_line(line):
        ratio = get_ratio(line.start_vel, line.end_vel, max_accel, line.get_len())
        midpoint = ratio_points(line.start_pos, line.end_pos, ratio)

        l1 = Line(line.start_pos, midpoint, line.start_vel, max_accel)
        l2 = Line(midpoint, line.end_pos, l1.end_vel, -max_accel)

        return l1,l2
        

    for i, part in enumerate(parts):
        if isinstance(part, Line) and abs(part.acceleration) != max_accel:
            parts[i:i+1] = optimize_line(part)

    for i, part in enumerate(parts): 
        if isinstance(part, Arc):
            vel = None
            for part in reversed(parts[0:i]):
                if isinstance(part, Line):
                    vel = part.end_vel
                    break

            assert vel is not None
            parts[i].vel = vel


    # lines = optimize_line(parts[0])
    return(parts)

def chunks_to_points(parts, freq):
    period = 1/freq
    points = []
    total_time = sum(part.get_total_time() for part in parts)

    # print(f"part 1 takes {parts[3].get_total_time()}")
    for t in np.arange(0,total_time, period):
        t2 = t
        for i, part in enumerate(parts):
            if t2 - part.get_total_time() > 0:
                t2 -= part.get_total_time()
            else:
                # print(f"gooching from part {i} at time {t}")
                # if isinstance(part, Line):
                points.append(part.get_pos_at_time(t2))
                break

    return points

def calc_path(in_segments, max_accel, max_radius, freq):
    segments = []
    for seg in in_segments:
        parts = calc_segment(seg, max_accel, max_radius)
        points = chunks_to_points(parts, freq)
        segments.append(points)

    return segments



def plot_path(parts):
    import matplotlib.pyplot as plt


    points = []
    # for chunk in parts:
    #     points += chunk.get_points_crude(100)

    # x = [point[0] for point in points]

    # print(parts[3].get_total_time())


    points = chunks_to_points(parts, 15)

    plt.scatter(*zip(*points)) 
    
    plt.show()

def plot_path_full(segments):
    import matplotlib.pyplot as plt
    points = []

    for seg in segments:
        for point in seg:
            points.append(point)

    plt.scatter(*zip(*points))
    plt.show()
    



if __name__ == "__main__":
    import pickle
    # print(calc_segment(seg, radius=))
    with open("path.pickle", 'rb') as file:
        segments = pickle.load(file)
        # segments = [[(0,0), (1,0), (1,1), (2,1)]]
        # for i in range(0,len(segments)):
        parts = calc_path(segments, 3, 1, 10)
        plot_path_full(parts)
    

    # parts = calc_segment(seg, 1, 10)
    # print(parts)
    # plot_path(parts)


[[(0,0),(0,0)],[(0,0),(0,0)]]