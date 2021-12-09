from face_full_processing import process_face, plot_path_full

segments, freq = process_face("C:/Users/Samir/OneDrive/Documents/Drawing Bot/GantryGame3.0/GantryGame3.0/ricardo.jpg", blur_radius = 5, lower_thresh = 0,
        upper_thresh = 40, splitDistance = 6, areaCut = 5,
        minSegmentLen = 30, max_accel = 40, max_lr = 1, turn_vel_multiplier = 1, freq = 120, plot_steps = True)
# plot_path_full(segments)