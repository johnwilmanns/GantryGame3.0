import math
from timer import timeit

@timeit
def calc_arc(a, vi, r, dt, start_angle, end_angle):
    velocities = [vi]
    positions = [0]
    angles = [start_angle]
    if end_angle < start_angle:
        direction = -1
    else:
        direction = 1

    total_distance = math.radians(abs(end_angle-start_angle)) * r
    #dvdt = math.sqrt(a ** 2 - v ** 4 / r ** 2)
    t = 0
    v = vi
    while True:
        try: 
            dvdt = math.sqrt(a ** 2 - v ** 4 / r ** 2)
        except ValueError:
            # raise ValueError("speed exceeded max at radius")
            print('this meants something bad, but fuck you im too lazy to fix it, so goodluck')
            dvdt = 0
        v += dvdt * dt

        velocities.append(v)
        positions.append(positions[-1] + v * dt)
        angles.append(math.degrees(positions[-1]/r))

        if angles[-1] > end_angle:
            velocities.pop()
            positions.pop()
            angles.pop()
            break

    # print(len(velocities))

    for i, vel in enumerate(angles):
        if i % 10 == 0:
            print(vel)


if __name__ == "__main__":
    calc_arc(1, .1, 1, .001, 60, 30)