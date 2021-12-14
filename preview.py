from face_full_processing import process_face, plot_path_full

<<<<<<< HEAD
segments, freq = process_face("small_obama.jpg", blur_radius = 11, lower_thresh = 10,
        upper_thresh = 60, splitDistance = 1.5, areaCut = 3,
        minSegmentLen = 5, max_accel = 40, max_lr = 1, turn_vel_multiplier = 1, freq = 120, plot_steps = True)
# plot_path_full(segments)
=======
segments, freq = process_face("C:/Users/Samir/OneDrive/Documents/Drawing Bot/GantryGame3.0/GantryGame3.0/square.jpg", blur_radius = 5, lower_thresh = 0,
        upper_thresh = 40, splitDistance = 6, areaCut = 5,
        minSegmentLen = 30, max_accel = 1, max_lr = 1, turn_vel_multiplier = 1, freq = 30, plot_steps = False)
plot_path_full(segments)        
>>>>>>> 5d68c686cfb74b3332d6c39beb133a01a6602dc9
