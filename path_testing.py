from full_face_processing import plot_path_full, process_combo_raw_multi, process_combo_raw
import full_face_processing
import cv2
import utilities
def main():
    filename = "brian.jpg"
    input_img = cv2.imread(filename)

    input_img = utilities.resize(input_img, 800, int(800 * input_img.shape[0] / input_img.shape[1]))

    # segments = process_combo(filename, 30, 1, 1, 120)
    # plot_path_full(segments)

    edges = process_combo_raw_multi(input_img)
    segments = full_face_processing.calc_path(edges, 5, .001, 1, 60)

    plot_path_full(segments)

if __name__ == '__main__':
    main()