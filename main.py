import multiprocessing as mp
import cv2
def main():
    import gantry
    import pickle
    import time

    scale_factor = 8
    offset = (0,0)

    def draw_progress(queue1, queue2):
        def distance(x1, y1, x2, y2):
            return (((x2-x1) ** 2 + (y2 - y1) ** 2) ** .5)
        #figure out how to make a blank image, i'm too retarded / impatitiant to try to understand samir's shit
        img = input_img.copy()
        mask = cv2.inRange(img, (0,0,0), (255,255,255))
        img[mask>0] = (255,255,255)
        old_x = 0
        old_y = 0
        while True:
            if queue1.empty() is False:
                seg = queue1.get()
                color = tuple(rd.randrange(0,255) for i in range(3))
                i = 0
                for i in range(len(seg)-1):

                    # print(seg[i])
                    if distance(seg[i][0], seg[i][1], seg[i+1][0], seg[i+1][1]) < 2000:
                        x1,y1,x2,y2 = seg[i][0], seg[i][1], seg[i+1][0], seg[i+1][1]
                        cv2.line(img,(x1,y1),(x2,y2),color,2)
            if queue2.empty() is False:
                x, y = queue2.get()
                cv2.line(img,(old_x,old_y),(x,y),(0,0,0),2)
            cv2.imshow('image', img)
            cv2.waitKey(1) #probably NOT how this works



    def pen_up():
        gantry.set_pos_noblock(z=5)
        time.sleep(.05)
        while any(axis.is_moving() for axis in gantry.axes()):
            time.sleep(.005)
    def pen_down():
        gantry.set_pos_noblock(z=0)
        time.sleep(.05)
        while any(axis.is_moving() for axis in gantry.axes()):
            time.sleep(.005)

    def move(point, cords=None):

        x,y = point
        x *= scale_factor
        y *= scale_factor


        x += offset[0]
        y += offset[1]

        gantry.trap_move(x,y, cords, queue2) #todo will this be defined?

        # # time.sleep(.1)
        # while any(axis.is_moving() for axis in gantry.axes()):
        #     time.sleep(.1)

        threshold = .1


        # while abs(gantry.x.get_pos() - x) > threshold or abs(gantry.y.get_pos() - y) > threshold:
        #     time.sleep(.001)
        
        
    segments = None
    import os
    import sys

    with open("path.pickle", "rb") as file:
        segments = pickle.load(file)
        # print(segments)



    gantry = gantry.Gantry()
    gantry.startup()
    print("started")


    # while True:
    #     gantry.set_pos_noblock(z=float(input()))

    pen_up()

    input("press return to start")
    queue1 = mp.Queue()
    queue2 = mp.Queue()
    visualizer = mp.Process(target=draw_progress, args=(queue))
    visualizer.start()
    pen_up()
    for i, seg in enumerate(segments):
        print(f"Currently on segment {i}/{len(segments)}")
        queue1.put(seg)
        move(seg[0])
        # print(seg[0])
        pen_down()
        cords = None
        for point in seg[1:]:
            cords = move(point, cords)
        pen_up()

    print("done")
    try:
        visualizer.close()
    except ValueError:
        print("sucsessfully terminated visualizer")
    pen_up()


    

if __name__ == "__main__":
    main()

