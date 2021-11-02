import controller

g = controller.Gantry()
g.dump_errors()
g.startup()
g.dump_errors()
g.__del__()

