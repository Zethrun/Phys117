import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

#Retrieves all files from data folder
folder_path = "C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/Pandas/Individual/"
path_list = [folder_path + folder_name for folder_name in os.listdir(folder_path)]
file_list = [[path + "/" + filename for filename in os.listdir(path)] for path in path_list]


def data_and_plot(files):
    plt.figure()
    (x_len, y_len) = plot_values(files)

    for i in range(len(files)):
        file = pd.read_csv(files[i])
        PT = np.array(file["PT"])
        phi = np.array(file["phi"])
        (PTx, PTy) = (0, 0)
        (energies, events) = ([], [])

        for j in range(len(PT)):
            PTx += PT[j]*np.cos(phi[j])
            PTy += PT[j]*np.sin(phi[j])
            energy = np.sqrt(np.square(PTx) + np.square(PTy))
            energies.append(energy)
            events.append(j)

        plot_style(energies, events, x_len, y_len, i)
    plt.show()


def plot_values(files):
    plot_amount = len(files)
    diff = 200

    for i in range(1, plot_amount + 1):

        for j in range(1, plot_amount + 1):
            
            if i * j == plot_amount and np.abs(i - j) < diff:
                diff = np.abs(i - j)
                (x, y) = (np.min((i, j)), np.max((i, j)))
    
    return (x, y)


def plot_style(x, y, x_len, y_len, i):
    style = "seaborn-darkgrid"
    plt.style.use(style)
    plt.subplot(x_len, y_len, i + 1)
    plt.plot(x, y, marker = ",")
    plt.grid()


for files in file_list:
    data_and_plot(files)