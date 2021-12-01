from face_full_processing import process_face, plot_path_full

segments, freq = process_face("ricardo.jpg", blur_radius = 17, lower_thresh = 0,
        upper_thresh = 40, splitDistance = 5, areaCut = 3,
        minSegmentLen = 15, max_accel = 40, max_lr = 1, freq = 60, plot_steps = False)
plot_path_full(segments)