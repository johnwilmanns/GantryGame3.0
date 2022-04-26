import cv2
import time
cam = cv2.VideoCapture(0)


FULL_RES = 1


if FULL_RES:
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

# assert width == 1920 and height == 1080, "the res is wrong"

# cv2.CAP_PROP_FPS = 20
print(width, height)
# print(cv2.CAP_OPENCV_MJPEG)

# print(cv2.CAP_PROP_FPS)
# print(f"current api:{cam.get()}")

print(f"fps is: {cam.get(5)}")

cam.set(5, 20)

print(f"fps is: {cam.get(5)}")

cv2.namedWindow("test")

img_counter = 0

while True:
    t0 = time.time()
    
    ret, frame = cam.read()
    
    if not ret:
        continue
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1
    print(f"recording at {1/(time.time()-t0)}hz")
cam.release()

cv2.destroyAllWindows()

