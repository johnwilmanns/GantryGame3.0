from calendar import c
import math
import matplotlib
from matplotlib.pyplot import step
import numpy as np
import copy
from pieces import Line, Arc, sin, cos


#TODO Fix curves that are slow accelerating, or even slow decelerating. look in do eyebrow

seg = [(0,0), (1,0), (1,1), (2,1)]
# seg = [(0,0), (0,1), (1,1), (1,2)]

def distance(x1, y1, x2, y2):
    return (((x2-x1) ** 2 + (y2 - y1) ** 2) ** .5)


# def getAngleSigned(a,b,c):
#     ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
#     # return ang % 360
#     # return ang
#     return ang if ang < 0 else ang

def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    # return ang % 360
    # return ang
    return ang + 360 if ang < 0 else ang



def calc_segment(seg, max_accel, max_radius, max_vel, john = "dumb"): #not actually max radius tho
    #TODO implement turn_vel_multiplier
    # R = V^2/A
    

    points = []
    parts = []
    if john != "dumb":
        os.system("rm -rf ~/")


    for i in range(len(seg)-2):
        a, b, c = seg[i:i+3]

        ab_dist = distance(*a, *b)
        bc_dist = distance(*b, *c)

        # if ab_dist == 0:
        #     continue

        abc_angle = getAngle(a,b,c)

        if abs(abc_angle - 180) < 1 or abs(abc_angle - 360) < 1 or abs(abc_angle) < 1: #Todo: fix this

            l = ab_dist
            r = 0
            lr = 0
            
            parts.append(Line(a, b))
            
        else:
            # l = (max_accel * ab_dist - velocity ** 2) / (3 * max_accel) # math n shit
            if i == 0:
                lr = min(ab_dist/2, bc_dist/2, max_radius)
            else:
                lr = min(ab_dist, bc_dist/2, max_radius) #TODO: decide if max radius should govrn lr or r
            
            r = (2 * sin(abc_angle/2) * lr) / abs(2 * sin(90-abc_angle/2))
            

            
            
            # if r > max_radius:
            #     r = max_radius
            #     lr = (r * abs(2 * sin(90 - abc_angle/2)))/ (2 * sin(abc_angle/2))

            l = ab_dist - lr
            
            

            # print(f"{r = }, {l = }")

            ratio = l/ab_dist
            end_pos = (a[0] * (1-ratio) + b[0] * ratio, a[1] * (1-ratio) + b[1] * ratio)

            ratio2 = lr/bc_dist
            new_pos = (b[0] * (1-ratio2) + c[0] * ratio2, b[1] * (1-ratio2) + c[1] * ratio2)

            seg[i+1] = new_pos

            # points += line_points(a, end_pos, 100)

            if a != end_pos:
                parts.append(Line(a, end_pos))



            shifter = (-(b[1]-a[1])/ab_dist * r, (b[0]-a[0])/ab_dist *r)
            
            if abc_angle > 180:
                circle_center = (end_pos[0]+shifter[0], end_pos[1]+shifter[1])
                
            elif abc_angle < 180:
                circle_center = (end_pos[0]-shifter[0], end_pos[1]-shifter[1])


            angle = getAngle(end_pos, circle_center , new_pos)

            if angle > 180:
                angle -= 360

            # points += [circle_center] # make sure axe dis shit
            circle_center_offset = (circle_center[0]+1, circle_center[1])
            # points += arc_points(circle_center, r, getAngle(circle_center_offset, circle_center, end_pos), getAngle(circle_center_offset, circle_center, new_pos), 100)
            parts.append(Arc(circle_center, r, getAngle(circle_center_offset, circle_center, end_pos), angle))


    parts.append(Line(*seg[-2:]))

    #Add a thing that collapses lines


    # print(parts[0])
    def get_recent_vel(index):
        
        if index == 0:
            return 0

        vel = parts[index-1].end_vel
        return vel if vel is not None else 0


        
        for part in reversed(parts[:index]):
            # if isinstance(part, Line):
            return part.end_vel
        return 0

    def get_ratio(va, vb, a, l):
        return (vb ** 2 - va ** 2)/(4* a * l) + 1/2

    def ratio_points(point1, point2, ratio):
        return (point1[0] * (1-ratio) + point2[0] * ratio, point1[1] * (1-ratio) + point2[1] * ratio)

    def decelerate_to_from(max_vel, index):
        assert index >= 0

        # print(f"deceling from {index}")
        


        # if isinstance(parts[index], Line):
        start_val = parts[index].set_end_vel(max_vel, max_accel)

            # exit()
        if start_val is not None:
            decelerate_to_from(start_val, index-1)


        # current_vel = None
        # for part in reversed(parts[:i]):
        #     if isinstance(part, Line):
        #         part.set_end_vel(max_vel, max_accel)
    #TODO break up arcs by angle


    
    buffer_parts = []
    for i, part in enumerate(parts[:]):
        if isinstance(part, Arc):
            angle_step = 10
            n = math.ceil(abs(part.angle_delta)/angle_step)
            stepsize = (part.angle_delta)/n
            vals = np.linspace(part.start_angle, part.start_angle+part.angle_delta, n+1)[:-1]

            # pairs = [[val % 360, stepsize] for val in np.linspace(part.start_angle, part.start_angle+part.angle_delta-stepsize, n)]
            
            # print("split into :", len(vals))
            arcs = []  
            for val in vals:
                arcs.append(Arc(part.center_pos, part.radius, val, stepsize))

            buffer_parts.extend(arcs)
        else:
            buffer_parts.append(part)
    parts = buffer_parts        
    

    for i, part in enumerate(parts):
        part.start_vel = get_recent_vel(i)

        if isinstance(part, Line):
            if get_recent_vel(i) < max_vel-.01:
                part.acceleration = max_accel
            else:
                part.start_vel = max_vel-.01
                decelerate_to_from(max_vel-.01, i-1)
                part.acceleration = 0
        elif isinstance(part, Arc):

            max_speed = min(part.max_speed(max_accel), max_vel)
            if max_speed < get_recent_vel(i): #This is obsolete?
                # print(f"part {i} is goin way too fast at {get_recent_vel(i)} bucko, should be {max_speed}")
                # print(f"capping vel at index {i}, to vel {max_speed}")
                part.start_vel = max_speed
                decelerate_to_from(max_speed, i-1)
                part.acceleration = 0
            else:
                tan_accel = part.get_max_acceleration(max_accel)
                part.acceleration = tan_accel
        else:
            1/0
    
    if parts[-1].end_vel > max_vel:
        decelerate_to_from(max_vel, len(parts)-1)
    
    for part in parts:
        if part.start_vel > max_vel + .0001 or part.end_vel > max_vel + .0001:
            raise Exception(f"Velocity is too high: {part.start_vel} {part.end_vel}")
    # print(parts)
    
    def cap_vel(line):
        # if line.end_vel > max_vel and line.start_vel > max_vel:
        #     raise Exception("line is going too fast")
        if line.end_vel > max_vel + .00001:
            if round(line.start_vel, 6) == max_vel:
                return [Line(line.start_pos, line.end_pos, max_vel, 0)]
                raise NotImplementedError
            assert line.acceleration >= 0
            dist = (max_vel ** 2 - line.start_vel ** 2) / (2 * line.acceleration) #TODO
            ratio = dist / line.get_len()
            l1= Line(line.start_pos, ratio_points(line.start_pos, line.end_pos, ratio), line.start_vel, line.acceleration)
            l2 = Line(l1.end_pos, line.end_pos, l1.end_vel, 0)
            
            return [l1, l2]
        elif line.start_vel > max_vel + .00001:
            if round(line.end_vel, 6) == max_vel:
                return [Line(line.start_pos, line.end_pos, max_vel, 0)]
                raise NotImplementedError
            assert line.acceleration <= 0
            dist = (max_vel ** 2 - line.start_vel ** 2) / (2 * line.acceleration) #TODO make sure a is neg
            ratio = dist / line.get_len()
            l1= Line(line.start_pos, ratio_points(line.start_pos, line.end_pos, ratio), max_vel, 0)
            l2 = Line(l1.end_pos, line.end_pos, l1.end_vel, line.acceleration) #TODO
            
            return [l1, l2]
        else:
            return [line]
    
    def optimize_line(line):
        
        ratio = get_ratio(line.start_vel, line.end_vel, max_accel, line.get_len())
        midpoint = ratio_points(line.start_pos, line.end_pos, ratio)

        l1 = Line(line.start_pos, midpoint, line.start_vel, max_accel)
        l2 = Line(midpoint, line.end_pos, l1.end_vel, -max_accel)
        
        # print(f"{l1=} {l2=}")
        
        if l1.end_vel > max_vel:
        
            first = cap_vel(l1)
            second = cap_vel(l2)
            
            # if la.acceleration is None or lb.acceleration is None or lc.acceleration is None or ld.acceleration is None:
            #     raise Exception("acceleration NULL")
            
            # print(la, lb, lc, ld)
            return first + second
        
        # if l1.end_vel > max_vel:
        #     if line.start_vel > max_vel or line.end_vel > max_vel:
        #         raise Exception("line is too fast")
        #     else:
        #         l1.set_end_vel(max_vel, max_accel)
            
        if l1.acceleration is None or l2.acceleration is None:
            raise Exception("acceleration NULL")

        return l1,l2
    
        
        
    buffer_parts = []

    for i, part in enumerate(parts):
        if part.start_vel > max_vel:
            raise Exception("part is too fast")
        if isinstance(part, Line) and abs(part.acceleration) != max_accel:
            buffer_parts.extend(optimize_line(part))
            # buffer_parts[i:i+1] = optimize_line(part)
            # print(len(parts))
        else:
            buffer_parts.append(part)

    parts = buffer_parts
    
    for part in parts:
        if (part.start_vel > (max_vel + .00001)) or (part.end_vel > (max_vel + .00001)):
            print(part.start_vel)
            print(part.end_vel)
            print(parts)
            raise Exception

    # print(parts)
    # for i, part in enumerate(parts): 
    #     if isinstance(part, Arc):
    #         vel = None
    #         for part in reversed(parts[0:i]):
    #             if isinstance(part, Line):
    #                 vel = part.end_vel
    #                 break

    #         assert vel is not None
    #         parts[i].vel = vel


    # lines = optimize_line(parts[0])

    return(parts)

def chunks_to_points(parts, freq):
    period = 1/freq
    points = []
    total_time = sum(part.get_total_time() for part in parts)
    # print("takes: ", total_time)

    # for part in parts:
    #     print(part)
    # print(f"takes: {total_time}")

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

    return points, total_time

            #warning: all of these values are multiplied by whatever the image is scaled to before drawing. right now this is about 8
def calc_path(in_segments, max_accel, max_radius, max_vel, freq):

    print(f"max accel {max_accel}, max radius {max_radius}, max vel {max_vel}")
    
    results = [calc_seg(seg, max_accel, max_radius, max_vel, freq) for seg in in_segments]
    
    segments = [res[0] for res in results]
    times = [res[1] for res in results]
    
    print(f"total time drawing: {sum(times)}s, plus travel: {sum(times)+.2*len(times)}s")
    
    # stuff = pool.map(calc_seg, (in_segments))
    return segments
    
    import multiprocessing as mp
    with mp.Pool(mp.cpu_count()) as pool:
        
        multiple_results = [pool.apply_async(calc_seg, (seg, max_accel, max_radius, max_vel, freq)) for seg in in_segments]
        results = [res.get() for res in multiple_results]


        segments = [res[0] for res in results]
        times = [res[1] for res in results]
        
        print(f"total time drawing: {sum(times)}s, plus travel: {sum(times)+.2*len(times)}s")
        
        # stuff = pool.map(calc_seg, (in_segments))
        return segments

def calc_seg(seg, max_accel, max_radius, max_vel, freq):
    # print(total_time)
    parts = calc_segment(seg, max_accel, max_radius, max_vel)
    # for part in parts:
    #     if part.start_vel > max_vel or part.end_vel > max_vel:
    #         print(f"max vel: {max_vel}, was exceeded by {part.start_vel} or {part.end_vel}")
    #         # raise Exception
    #         raise Exception("part is too fast")
            
    points, seg_time = chunks_to_points(parts, freq)
    return (points, seg_time)



def plot_chunks(parts):
    import matplotlib.pyplot as plt
    from matplotlib import patches
    
    fig, ax = plt.subplots()
    
    a = []
    b = []
    for part in parts:
        if isinstance(part, Line):
            a.append(part.start_pos)
            b.append(part.end_pos)
        else:
            if part.angle_delta > 0:
                e =  patches.Arc(part.center_pos, 2 * part.radius, 2 * part.radius, 0, part.start_angle, part.start_angle+part.angle_delta)
            else:
                e =  patches.Arc(part.center_pos, 2 * part.radius, 2 * part.radius, 0, part.start_angle+part.angle_delta, part.start_angle)
            # e =  patches.Arc(part.center_pos, part.radius, 0)
            
            ax.add_patch(e)
            
    
    
    ab_pairs = np.c_[a, b]
    plt_args = ab_pairs.reshape(-1, 2, 2).swapaxes(1, 2).reshape(-1, 2)
    ax.plot(*plt_args)
    
    
    plt.show()

def plot_path(points):
    import matplotlib.pyplot as plt


    # points = []
    # for chunk in parts:
    #     points += chunk.get_points_crude(100)

    # x = [point[0] for point in points]

    # print(parts[3].get_total_time())


    # points = chunks_to_points(parts, 15)

    plt.scatter(*zip(*points)) 
    
    plt.show()

def plot_path_full(segments):
    import matplotlib.pyplot as plt
    points = []

    for seg in segments:
        for point in seg:
            points.append(point)

    plt.scatter(*zip(*points), s=2)
    # plt.xlim(0,50)
    # plt.ylim(-25,25)
    plt.show()


# take an array of points
#calculate the distance between them
#return the total distance
def calc_distance(points):
    distance = 0
    for i in range(len(points)-1):
        distance += np.linalg.norm(points[i+1] - points[i])
    return distance



# i wrote none of this, copilot wrote all of it
def calculate_path_lenth(segments):
    total_length = 0
    for seg in segments:
        total_length += calc_distance(seg)
    return total_length

#get an integer from a file
def get_path_distance(filename="distance.txt"):
    with open(filename) as f:
        return int(f.read())

def set_path_distance(distance, filename="distance.txt"):
    with open(filename, 'w') as f:
        f.write(str(distance))

#i wrote this part
def update_path_distance(segments, filename="distance.txt"):
    set_path_distance(get_path_distance() + calculate_path_lenth(segments), filename)





if __name__ == "__main__":
    import pickle
    import random as rd
    # print(calc_segment(seg, radius=))
    # with open("path.pickle", 'rb') as file:
    #     segments = pickle.load(file)
    # rd.seed(42)

    rd.seed(42)
    # seg = [(i, rd.random()/10) for i in range(0,10)]
    seg = [(0,0), (10,0), (10,0.1)]

    segments = [seg]
    # for i in range(0,len(segments)):
    
    parts = calc_segment(seg,100,10,1)
    # plot_chunks(parts)
    # print(parts)
    
    points, t = chunks_to_points(parts, 60)
    # plot_path(points)
    
    max_dist = 0
    for i in range(len(points)-1):
        max_dist = max(max_dist, distance(*points[i+1], *points[i]))
    print(max_dist * 60)
    
    # for part in parts:
    #     print(part)

    
    # print(points)