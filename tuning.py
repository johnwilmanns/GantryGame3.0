from main import main

for i in range(1, 10):
    main(max_accel= 40, max_lr=.1, freq=10 * i, offset=(1 * i, .5 * i))
