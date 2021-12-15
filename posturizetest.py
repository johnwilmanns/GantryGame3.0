import posterize
import cv2
import utilities
import time
from time import sleep
image = cv2.imread("obama.png")
segments = posterize.get_segments(image)
print(segments)

def pen_down():
    print("pen down")

def pen_up():
    print("pen up")

def move(x, y):
    print(f"moved to {x}, {y}")

def blocked_move(x, y):
    print(f"blocked da move to {x}, {y}")

img = utilities.get_blank_image(800,800)

for i, seg in enumerate(segments):
    print(f"Currently on segment {i}/{len(segments)}")
    t0 = time.perf_counter()
    blocked_move(seg[0][0], seg[0][1])
    # print(seg[0])
    pen_down()
    t1 = time.perf_counter()

    move(seg[1][0], seg[0][1])
    # time.sleep(.5)
    print(f"segment written at {(time.perf_counter() - t1)} sec")

    pen_up()

    cv2.line(img, (int(seg[0][0] * 800), int(seg[0][1] * 800)), (int(seg[1][0] * 800), int(seg[1][1] * 800)), (800, 800, 800), 2)
cv2.imshow('image', img)
cv2.waitKey(1)
cv2.waitKey(0)
