from operator import le
import image_processing
import trajectory_planning
import run_gantry
import utilities


def main(input_img):
    
    segments = image_processing.process_combo_raw(input_img)
    segments = trajectory_planning.calc_path(segments, 5, .01, 1, 120)
    
    run_gantry.main(segments)
    
if __name__ == "__main__":
    import cv2
    filename = "galaxy_inv.jpg"
    input_img = cv2.imread(filename)
    input_img = utilities.resize(input_img, 500, 500)
    
    segments = image_processing.process_combo_raw(input_img)
    preview = image_processing.plot_segments(segments)
    cv2.imshow("preview", preview)
    cv2.waitKey(0)
    segments = trajectory_planning.calc_path(segments, 10, .01, 1, 60)
    
    run_gantry.main(segments, 60)

    # input_img = utilities.resize(input_img, 800, int(800 * input_img.shape[0] / input_img.shape[1]))
