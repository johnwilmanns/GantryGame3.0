def main():
    # import gantry
    import pickle
    import time

    scale_factor = 8
    offset = (0,0)

    def pen_up():
        gantry.set_pos_noblock(z=5)
        time.sleep(1)
    def pen_down():
        gantry.set_pos_noblock(z=0)
        time.sleep(1)

    def move(point):
        x,y = point
        x *= scale_factor
        y *= scale_factor


        x += offset[0]
        y += offset[1]

        gantry.trap_move(x,y)

        time.sleep(.2)
        while any(axis.is_moving() for axis in gantry.axes()):
            time.sleep(.1)

    def pen_up():
        print('up')

    def pen_down():
        print('down')
    
    def move(point):

        x,y = point
        x *= scale_factor
        y *= scale_factor


        x += offset[0]
        y += offset[1]
        
        point = (x,y)

        print(f"Going to {point}")
        
        
    segments = None
    import os
    import sys

    with open(os.path.join(sys.path[0], "path.pickle"), "rb") as file:
        segments = pickle.load(file)
        # print(segments)



    # gantry = gantry.Gantry()
    # gantry.startup()

    pen_up()
    for seg in segments:
        move(seg[0])
        pen_down()
        for point in seg[1:]:
            move(point)
        pen_up()

    print("done")



    

if __name__ == "__main__":
    main()

