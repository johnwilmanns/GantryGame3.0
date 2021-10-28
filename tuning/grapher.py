import matplotlib.pyplot as plt
import time
import numpy as np
import pandas as pd
import pandas.plotting
import sys
import csv


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

def export_values():
    try:
        with open("outputstuff.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows([costs, values])
    except:
        print("it appears I am retarded")
        pass


def exepthook(type, value, tb):
    print("exepted")
    #show_graph()

#sys.excepthook = exepthook