import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

file = "Data/Pandas/Sum/Background/"
file_list = [file + filename for filename in os.listdir(file)]

def data_func(files):
    plt_data = []
    for file in files:
        file = pd.read_csv(file)
        PT = file["PT"][:5]
        event_num = file["event#"][:5]
        stack = np.vstack((PT, event_num))
        plt_data.append(stack)

    return plt_data

data = data_func(file_list)
print(data)