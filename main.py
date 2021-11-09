def main():
    import gantry
    import pickle

    scale_factor = 8
    offset = (0,0)

    def pen_up():
        pass
    def pen_down():
        pass
    def move(point):
        x,y = point
        x,y *= scale_factor

        x += offset[0]
        y += offset[1]

        gantry.trap_move(x,y)
        



    segments = None

    with open("path.pickle", "rb") as file:
        segments = pickle.load(file)
        print(segments)



    gantry = gantry.Gantry()
    gantry.startup()

    
    for seg in segments:
        move(seg[0])
        pen_down()
        for point in seg[1:]:
            move(point)
        pen_up()

    print("done")



    

if __name__ == "__main__":
    main()

