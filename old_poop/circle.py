from planner import Planner
import time

def main():

    Planner.find_motors()
    ggmotors = Planner.drawer

    # ggmotors.circle_pos(1,1)


    # ggmotors.set_y_pos(1)

    print("Hello world!")


    # while True:
    #     time.sleep(.2)
    #     print(f"X = {ggmotors.get_x_pos()}")
    #     print(f"Y = {ggmotors.get_y_pos()}")
    #     print(f"X = {ggmotors.get_z_pos()}")

    for axis in ggmotors.axes:
        print(f"{axis}: {ggmotors.axes[axis].get_pos()}")

if __name__ == "__main__":

    main()

    # try:
    #     main()
    # except Exception as e:
    #     print(e)