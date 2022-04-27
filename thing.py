import cv2
import time
import utilities

cam = cv2.VideoCapture(0, cv2.CAP_V4L)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

FULL_RES = True

if FULL_RES:
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

assert width == 1920 and height == 1080, "the res is wrong"


print(width, height)

cv2.namedWindow("test")

img_counter = 0

while True:
    t0 = time.time()

    
    ret, frame = cam.read()
    
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", utilities.resize(frame, 960, 540))

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "2opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1
    print(f"recording at {1 / (time.time() - t0)}hz")
cam.release()

cv2.destroyAllWindows()
