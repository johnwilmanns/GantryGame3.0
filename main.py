def main():
    import gantry
    import pickle


    def pen_up():
        pass
    def pen_down():
        pass
    
    segments = None

    with open("path.pickle", "rb") as file:
        segments = pickle.load(file)
        print(segments)



    gantry = gantry.Gantry()
    gantry.startup()

    
    for seg in segments:
        for point in seg:
            gantry.trap_move(*point)


    

if __name__ == "__main__":
    main()

