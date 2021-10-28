import odrive
from odrive.enums import *
from odrive.utils import start_liveplotter
import time
import numpy as np


odrv0_serial = "20793595524B"  # Previously Xavier
odrv1_serial = "20673593524B"  # Previously Yannie

odrv0 = odrive.find_any(serial_number=odrv0_serial)
odrv1 = odrive.find_any(serial_number=odrv1_serial)

axis = None

def move(dist = 5):
    axis.controller.input_pos = 0
    time.sleep(2)

    axis.controller.input_pos = dist

def move2(t = 1):
    startpos = axis.encoder.pos_estimate

    axis.controller.input_vel = 3
    time.sleep(t)
    axis.controller.input_vel = -3
    time.sleep(t)
    axis.controller.input_pos = startpos

def rmse_calc(values: np.array, input_pos: float):
       return np.sqrt(((values - input_pos) ** 2).mean())


def vibration_calc(values: np.array):
    	
    variances = np.array([])
    for i in range(len(values)-2):
        variance = (values[i] + values[i+2])/2 - values[i+1]
        variances = np.append(variances,variance)

    return rmse_calc(variances, 0)


"""Gathers data along a movement, returns a numpy array"""


def analyze_move(t=1):
    t0 = time.time()

    values = np.array([])
    input_pos = axis.controller.input_pos

    while(time.time()-t0 < t):
        values = np.append(values, axis.encoder.pos_estimate)

    rmse = rmse_calc(values, input_pos)
    var = vibration_calc(values)

    return rmse, var


"""Evaluates the sucsess of the values based on the vibration and rsme distance"""


def evaluate_values(values, mov_dist=1, rmse_weight=1, variance_weight=1):

    assert -0.05 < axis.encoder.pos_estimate < .05

    axis.controller.config.vel_gain = values[0]
    axis.controller.config.pos_gain = values[1]
    axis.controller.config.vel_integrator_gain = values[2]

    axis.controller.input_pos = mov_dist
    base_rmse, base_variance = analyze_move(2)
    axis.controller.input_pos = 0
    move = analyze_move(2)
    base_rmse += move[0]
    base_variance += move[1]
    base_rmse /= 2
    base_variance /= 2


    print(f"rmse = {base_rmse}, variance = {base_variance}")

    return base_rmse ** rmse_weight * base_variance ** variance_weight


def start_plotter(data_list = [axis.encoder.pos_estimate, axis.controller.input_pos]):
    start_liveplotter(lambda:data_list)



def startup(odrv_num = 1, axis_num = 1):
    global axis

    assert odrv_num == 1 or odrv_num == 0
    assert axis_num == 1 or axis_num == 0

    odrv0_serial = "20793595524B"  # Previously Xavier
    odrv1_serial = "20673593524B"  # Previously Yannie

    odrv0 = odrive.find_any(serial_number=odrv0_serial)
    odrv1 = odrive.find_any(serial_number=odrv1_serial)

    if odrv_num:
        if axis_num:
            axis = odrv1.axis1
        else:
            axis = odrv1.axis0
    else:
        if axis_num:
            axis = odrv0.axis1
        else:
            axis = odrv0.axis0


    axis.requested_state =  AXIS_STATE_FULL_CALIBRATION_SEQUENCE

    while axis.current_state != AXIS_STATE_IDLE:
        pass
    time.sleep(1)

    axis.controller.config.vel_limit = 20
    axis.controller.config.enable_overspeed_error = False

    axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    axis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
    axis.controller.config.input_mode = INPUT_MODE_PASSTHROUGH
    time.sleep(1)

def main():


    start_plotter()
    startup()
    

    print("Type the key letter, a space, and then a number to set gain value. EX: \"P 50\"")
    print("Type \"d\" to reset all values to their default")
    print("Type \"m\" to move by position, type \"m2\" to move by velocity, can be followed by a space and distance")

    while True:
        print(f"""
        vel_gain (v) = {axis.controller.config.vel_gain}
        pos_gain (p) = {axis.controller.config.pos_gain}
        vel_integrator_gain (i) = {axis.controller.config.vel_integrator_gain}""")
        

        text = input()

        try:

            if text == "d":
                axis.controller.config.vel_gain = .16
                axis.controller.config.pos_gain = 20
                axis.controller.config.vel_integrator_gain = .32


            elif text[0:2] == 'm2':

                val = float(text.split(" ")[1])
                print(f"moving vel {val}")
                move2(float(val))

            elif text[0] == 'm':

                val = float(text.split(" ")[1])
                print(f"moving {val}")
                move(float(val))


                
            else:
                target, val = text.split(" ")
                val = float(val)

                if target == "v":
                    axis.controller.config.vel_gain = val
                elif target == "p":
                    axis.controller.config.pos_gain = val
                elif target == "i":
                    axis.controller.config.vel_integrator_gain = val
                

            
        except Exception as e:
            print(f"ERROR: {e}")

    

# odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
# odrv0.axis0.motor.config.pre_calibrated = True
# odrv0.axis0.config.startup_encoder_offset_calibration = True
# odrv0.axis0.config.startup_closed_loop_control = True
# odrv0.save_configuration()
# odrv0.reboot()

print("done!")

if __name__ == "main":
    main()

