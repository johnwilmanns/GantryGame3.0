from pieces import sin, cos




# if r > max_radius:
#     r = max_radius
#     lr = (r * abs(2 * sin(90 - abc_angle/2)))/ (2 * sin(abc_angle/2))


def lr_to_r(lr, abc_angle):
    r = (2 * sin(abc_angle/2) * lr) / abs(2 * sin(90-abc_angle/2))
    return r

def r_to_lr(r, abc_angle):
    lr = (r * abs(2 * sin(90 - abc_angle/2)))/ (2 * sin(abc_angle/2))
    return lr

angle = 

lr = 1

r = lr_to_r(lr, angle)
lr2 = r_to_lr(r, angle)