from face_full_processing import process_face, plot_path_full


segments, freq = process_face("small_obama.jpg", blur_radius = 11, lower_thresh = 10,
        upper_thresh = 60, splitDistance = 1.5, areaCut = 3,
        minSegmentLen = 5, max_accel = 40, max_lr = 1, turn_vel_multiplier = 1, freq = 120, plot_steps = True)
# plot_path_full(segments)
