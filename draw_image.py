from cv2 import threshold
import image_processing
import trajectory_planning
# import run_gantry
# import utilities

'''Edge Processing Values'''
EDGE_BLUR_RADIUS = 11
EDGE_LOWER_THRESHOLD = 0
EDGE_UPPER_THRESHOLD = 30
EDGE_APERTURE_SIZE = 3
EDGE_BIND_DIST = 10
EDGE_AREA_CUT = 3
EDGE_MIN_LEN = 10
EDGE_CALC_ROGUES = True;


'''Shading Processing Values'''
SHADING_BLUR_RADIUS = 21
SHADING_THRESHOLDS = [10, 30, 50,60]
SHADING_LINE_DIST = 5
SHADING_BIND_DIST = SHADING_LINE_DIST * 2
SHADING_AREA_CUT = 10
SHADING_MIN_LEN = 15




def main(input_img):
    
    print("starting edge processing")
    segments = []
    segments = image_processing.process_edges_raw(input_img, 
                                                    blur_radius = EDGE_BLUR_RADIUS,
                                                    lower_thresh= EDGE_LOWER_THRESHOLD,
                                                    upper_thresh= EDGE_UPPER_THRESHOLD,
                                                    aperture_size= EDGE_APERTURE_SIZE,
                                                    bind_dist = EDGE_BIND_DIST,
                                                    area_cut = EDGE_AREA_CUT,
                                                    min_len = EDGE_MIN_LEN)
    
    print("starting shading processing")
    segments.extend(image_processing.process_shading_raw(input_img,
                                                    blur_radius = SHADING_BLUR_RADIUS,
                                                    thresholds = SHADING_THRESHOLDS,
                                                    line_dist = SHADING_LINE_DIST,
                                                    bind_dist = SHADING_BIND_DIST,
                                                    area_cut = SHADING_AREA_CUT,
                                                    min_len = SHADING_MIN_LEN))

    
    # segments = image_processing.process_combo_raw(input_img)
    # segments = trajectory_planning.calc_path(segments, 5, .01, 1, 120)
    
    # run_gantry.main(segments)
    out_image = image_processing.plot_segments(segments)
    
    print(f"{len(segments)} segments found");
    
    # 
    
    segments = trajectory_planning.calc_path(segments, 10, 1, 1, 120)   
    
    # cv2.waitKey(0)

    # if input("run gantry? (y/n)") == "y":
    #     import run_gantry
    #     run_gantry.main(segments, 120)
    # else:
    cv2.imshow("out_image", out_image)
    cv2.waitKey(0)

    
    
if __name__ == "__main__":
    
    
    import cv2
    filename = "2opencv_frame_8.png"
    input_img = cv2.imread(filename)
    
    main(input_img)
    # # input_img = utilities.resize(input_img, 500, 500)

    # segments = image_processing.process_combo_raw(input_img)
    # preview = image_processing.plot_segments(segments)
    # cv2.imshow("preview", preview)
    # cv2.waitKey(0)
    # segments = trajectory_planning.calc_path(segments, 80, 1, 1, 120)
    # print("running gantry")
    # run_gantry.main(segments[:], 120)

    # input_img = utilities.resize(input_img, 800, int(800 * input_img.shape[0] / input_img.shape[1]))
