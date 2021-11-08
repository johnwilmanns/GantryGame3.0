import controller


def main():
    controller = controller.Controller()
    while True:
        x = int(input("x plz "))
        y = int(input("y plz "))
        controller.trap_move(x, y)

if __name__ == "__main__":
    try: 
        main()
    except Exception:
        controller.trap_move(3,3)
        import guess_what_this_does