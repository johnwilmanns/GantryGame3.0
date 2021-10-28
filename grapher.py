import matplotlib.pyplot as plt
import time
import numpy as np
import pandas as pd
import pandas.plotting
import sys



def init():
    global costs
    costs = []
    global values
    values = []
def show_graph():
    print("showing graph")
    print(costs)
    print(costs[1])
    # plt.plot(costs)
    # plt.plot(values)


    df = pd.DataFrame(values)
    print("John's stupid dataframe: ")
    print(df)
    try:
        df[0].plot()
        df[1].plot(secondary_y=True, style="g")
    except:
        pass



def exepthook(type, value, tb):
    print("exepted")
    #show_graph()

#sys.excepthook = exepthook