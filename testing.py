import numpy as np
import random as rd

rd.seed(42)

a = [(i/10) ** 2 for i in range(-50,50)]
b = [i+rd.randint(-10,10) for i in a]


a = np.array(a)
b = np.array(b)

def rmse_calc(values: np.array, input_pos: float):
       return np.sqrt(((values - input_pos) ** 2).mean())

def vibration_calc(values: np.array):
    	
    variances = np.array([])
    for i in range(len(values)-2):
        variance = (values[i] + values[i+2])/2 - values[i+1]
        variances = np.append(variances,variance)
              
    return rmse_calc(variances, 0)



print(a)
print(b)

print(rmse_calc(a, 0))
print(rmse_calc(b, 0))

print(vibration_calc(a))
print(vibration_calc(b))

