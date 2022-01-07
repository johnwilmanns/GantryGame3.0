from face_full_processing import process_face, plot_path_full


segments, freq = process_face("C:/Users/Samir/OneDrive/Documents/Drawing Bot/GantryGame3.0/GantryGame3.0/small_obama.jpg", blur_radius = 11, lower_thresh = 10,
        upper_thresh = 50, segmentSplitDistance=15, areaCut = 3,
        minNumPixels = 15, max_accel = 5, max_lr = 1, turn_vel_multiplier = 1, freq = 60, plot_steps = False)
plot_path_full(segments)
