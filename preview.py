from face_full_processing import process_face, plot_path_full

segments, freq = process_face("ricardo.jpg", blur_radius = 17, lower_thresh = 0,
        upper_thresh = 40, splitDistance = 20, areaCut = 10,
        minSegmentLen = 15, max_accel = 40, max_lr = .02, freq = 60, plot_steps = True)
plot_path_full(segments)