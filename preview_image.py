import time
import image_processing




def main(input_img):
    
    segments = image_processing.process_combo_raw(input_img)
#     segments = trajectory_planning.calc_path(segments, 5, .01, 1, 120)
    # image_processing.plot_segments(segments)
    
    
if __name__ == "__main__":
    import cv2
    filename = "brian.jpg"
    input_img = cv2.imread(filename)

    # input_img = utilities.resize(input_img, 800, int(800 * input_img.shape[0] / input_img.shape[1]))

    
    main(input_img)