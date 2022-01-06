
import numpy as np
import math


def sin(degrees):
    return math.sin(math.radians(degrees))


def cos(degrees):
    return sin(degrees + 90)


def distance(x1, y1, x2, y2):
    return (((x2 - x1) ** 2 + (y2 - y1) ** 2) ** .5)


def ratio_points(point1, point2, ratio):
    return (point1[0] * (1 - ratio) + point2[0] * ratio, point1[1] * (1 - ratio) + point2[1] * ratio)


class Line():

    def __init__(self, start_pos, end_pos, start_vel=None, acceleration=None):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.start_vel = start_vel
        self.acceleration = acceleration
        pass

    def __repr__(self):
        # return ""
        return str(f"<Line {self.start_vel=} {self.acceleration=} {self.end_vel=}>")
        return str(f"<Line from {self.start_pos} to {self.end_pos} {self.start_vel=} {self.acceleration=} {self.end_vel=}>")

    def get_len(self):
        return distance(*self.start_pos, *self.end_pos)

    def get_total_time(self):
        return -(self.start_vel - math.sqrt(
            self.start_vel ** 2 + 2 * self.acceleration * self.get_len())) / self.acceleration

    def get_pos_at_time(self, t):
        dist = self.start_vel * t + (self.acceleration * t ** 2) / 2
        ratio = dist / self.get_len()
        return ratio_points(self.start_pos, self.end_pos, ratio)
        # return self.start_vel * t + (self.acceleration * t ** 2)/2

    @property
    def end_vel(self):
        if self.start_vel is not None:
            try:
                return math.sqrt(self.start_vel ** 2 + 2 * self.acceleration * self.get_len())
            except ValueError:
                return 0  # TODO fix, this is prob shit
        else:
            return None

    def find_start_vel(self, accel, vf):
        try:
            return math.sqrt(vf ** 2 + 2 * accel * self.get_len())
        except ValueError:
            return 0

    def find_accel(self, vf):
        return (vf ** 2 - self.start_vel ** 2) / (2 * self.get_len())

    # def find_accel2(self, vi, vf):
    #     (vf ** 2 - vi ** 2) / (2 * self.get_len())

    def set_end_vel(self, vel, max_accel):
        # if just modified accel, return None
        # if modified accel and c nct. d.nnr  start_vel, return start_vel

        # self.end_vel = vel
        min_start_vel = self.find_start_vel(max_accel, vel)  # THIS BROKE
        # accel = self.find_accel2()
        # print(f"{max_accel=}")
        # print(f"{vel=}")
        # print(f"{self.end_vel=}")
        # print(f"{self.start_vel=}")
        # print(f"{min_start_vel=}")
        if min_start_vel > self.start_vel:
            self.acceleration = self.find_accel(vel)
            return None
        else:
            self.start_vel = min_start_vel
            self.acceleration = -max_accel
            return self.start_vel

    def get_points_crude(self, num_points):
        points = []

        if self.start_pos == self.end_pos:
            return [self.start_pos]
        elif self.start_pos[0] == self.end_pos[0]:
            x = self.start_pos[0]
            for y in np.arange(self.start_pos[1], self.end_pos[1], (self.end_pos[1] - self.start_pos[1]) / num_points):
                points.append((x, y))
        elif self.start_pos[1] == self.end_pos[1]:
            y = self.start_pos[1]
            for x in np.arange(self.start_pos[0], self.end_pos[0], (self.end_pos[0] - self.start_pos[0]) / num_points):
                points.append((x, y))
        else:
            for x, y in zip(
                    np.arange(self.start_pos[0], self.end_pos[0],
                              (self.end_pos[0] - self.start_pos[0]) / num_points),
                    np.arange(self.start_pos[1], self.end_pos[1], (self.end_pos[1] - self.start_pos[1]) / num_points)):
                points.append((x, y))

        return points


class Arc():
    def __init__(self, center_pos, radius, start_angle, angle_delta):
        self.center_pos = center_pos
        self.radius = radius
        self.start_angle = start_angle
        self.angle_delta = angle_delta
        self.start_vel = None
        self.acceleration = None
    def __repr__(self):
        # return str(self.)
        # return str(f"<Arc with start_vel = {self.start_vel}, end_vel = {self.end_vel}, acceleration = {self.acceleration}")
        return str(
            f"<Arc centered at {self.center_pos}, from {self.start_angle} + {self.angle_delta} with radius {self.radius}>")

    # def max_accel(self, vel):
    #     return vel ** 2 / self.radius
    
    @property
    def theta(self):
        # a1 = self.start_angle % 360
        # a2 = self.end_angle % 360
        
        # angle = 180 - abs(abs(a1 - a2) - 180)

        return math.radians(abs(self.angle_delta))
    @property
    def end_vel(self):

        

        if self.start_vel is not None:
            try:
                return math.sqrt(self.start_vel ** 2 + 2 * self.acceleration * self.theta * self.radius)
            except ValueError:
                return 0  # TODO fix, this is prob shit
        else:
            return None



    def get_max_acceleration(self, max_accel):
        

        a = ((math.sqrt(
            (max_accel ** 2) * (self.radius ** 4) + 4 * (self.theta ** 2) * (max_accel ** 2) * (self.radius ** 2) - (self.radius ** 2) * (self.start_vel ** 4)) - 2 * self.theta * (
            self.start_vel ** 2))) / (4 * (self.theta ** 2) + (self.radius ** 2))

        return a

    def get_max_deceleration(self, max_accel, vi):
        if math.isclose(vi, self.max_speed(max_accel)):
            return 0
        return math.sqrt((max_accel**2) * (self.radius**2) - (vi**4))/self.radius

    def find_start_vel(self, max_accel, vf):

        vi = math.sqrt(((2 * math.sqrt(-self.theta ** 2  * (vf ** 4 - 4 * self.theta ** 2 * max_accel ** 2 * self.radius ** 2 - max_accel**2 * self.radius**2))) / (4 * self.theta ** 2 + 1)) + (vf ** 2/(4 * self.theta**2 + 1)))

        # vi = math.sqrt(math.sqrt(4 * (self.theta**2) * (max_accel**2) * (self.radius**2) - (vf**4) * (self.radius**2)))/(math.sqrt(2)*math.sqrt(self.theta))
        return vi

    def find_accel(self, vf):

        return (vf ** 2 - self.start_vel ** 2) / (2 * self.theta * self.radius)

    def set_end_vel(self, vel, max_accel):
        # if just modified accel, return None
        # if modified accel and c nct. d.nnr  start_vel, return start_vel

        # self.end_vel = vel

        self.acceleration = -self.get_max_deceleration(max_accel, self.start_vel)
        if self.end_vel > vel:
            min_start_vel = self.find_start_vel(max_accel, vel)
            self.start_vel = min_start_vel
            self.acceleration = -self.get_max_deceleration(max_accel, self.start_vel)
            return self.start_vel
        else:
            self.acceleration = self.find_accel(vel)
            return None

        min_start_vel = self.find_start_vel(max_accel, vel)  # THIS BROKE
        # accel = self.find_accel2()
        # print(f"{max_accel=}")
        # print(f"{vel=}")
        # print(f"{self.end_vel=}")
        # print(f"{self.start_vel=}")
        # print(f"{min_start_vel=}")
        if min_start_vel > self.start_vel:
            self.acceleration = self.find_accel(vel)
            return None
        else:
            self.start_vel = min_start_vel
            self.acceleration = -max_accel
            return self.start_vel

    #TODO fix these
    # def get_total_time(self):
    #     return self.radius * math.radians(abs(self.end_angle - self.start_angle)) / self.vel

    def get_total_time(self):
        if self.acceleration == 0:
            return self.radius * self.theta / self.start_vel

        return -(self.start_vel - math.sqrt(
            self.start_vel ** 2 + 2 * self.acceleration * self.radius * self.theta)) / self.acceleration

    def get_pos_at_time(self, t):

        # if self.end_angle - self.start_angle < -180:
        #     self.end_angle += 360
        # elif self.end_angle - self.start_angle > 180:
        #     self.end_angle -= 360

        # i dont think this is right
        w0 = self.start_vel/self.radius
        alpha = self.acceleration / self.radius

        angle_moved = math.degrees(w0 * t + 1/2 * alpha * t ** 2)

        # angle_delta = angular_vel * t


        angle = self.start_angle + angle_moved * np.sign(self.angle_delta)

        return (cos(angle) * self.radius + self.center_pos[0], sin(angle) * self.radius + self.center_pos[1])
        # return self.start_vel * t + (self.acceleration * t ** 2)/2



    def max_speed(self, accel):
        return math.sqrt(accel * self.radius)



    # def get_max_speed()


if __name__ == "__main__":
    a = Arc((0,0), 2, 0, 180)
    # print(a.get_max_acceleration(1, 2, 1))
    
    print(a.find_start_vel(1,.5))
