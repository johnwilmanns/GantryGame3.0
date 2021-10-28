import matplotlib.pyplot as plt
import time
import numpy as np
import pandas as pd
import pandas.plotting

def init():
    global costs
    costs = []
    global values
    values = []
def show_graph():

    try:
        plt.plot(costs)
        plt.plot(values)
    except:
        pass
    try:
        df = pd.DataFrame(values)
        df[0].plot()
        df[1].plot(secondary_y=True, style="g")

    except:
        pass

    time.sleep(100)