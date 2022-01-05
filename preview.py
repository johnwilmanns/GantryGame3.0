from face_full_processing import process_face, plot_path_full


segments, freq = process_face("small_obama.jpg", blur_radius = 11, lower_thresh = 10,
        upper_thresh = 50, segmentSplitDistance=15, areaCut = 3,
        minNumPixels = 15, max_accel = 40, max_lr = 1, turn_vel_multiplier = 1, freq = 120, plot_steps = False)
plot_path_full(segments)
