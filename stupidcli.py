import controller

controller = controller.Controller()

while True:
    x = int(input("x plz "))
    y = int(input("y plz "))
    controller.trap_move(x, y)