from full_face_processing import plot_path_full
import full_face_processing
input_img = "small_obama.png"

segments = full_face_processing.process_combo_raw("ricardo.jpg")
segments = full_face_processing.calc_path(segments, 5, .001, 1, freq)

plot_path_full(segments)