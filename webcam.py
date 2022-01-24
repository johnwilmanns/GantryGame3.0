import cv2


def capture_image():
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)

    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        cv2.imshow("preview", frame)
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        # if key == 27: # exit on ESC
        #     break
        if key == ord(' '):
            break

    vc.release()
    cv2.destroyWindow("preview")
    
    return frame

if __name__ == "__main__":
    img = capture_image()
    print(img.shape)
    cv2.imshow("pic", img)
    
    cv2.waitKey(0)