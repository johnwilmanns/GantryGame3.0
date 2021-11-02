import controller

g = controller.Gantry()
g.dump_errors()
g.sensorless_home([True, True, True])
g.dump_errors()
g.__del__()

