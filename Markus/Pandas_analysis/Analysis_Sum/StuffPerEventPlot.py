from doctest import OutputChecker
import enum
from importlib.util import spec_from_file_location
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

folder_path = "C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/Pandas/Sum/"
path_list = [folder_path + folder_name for folder_name in os.listdir(folder_path)]
file_list = [[path + "/" + filename for filename in os.listdir(path)] for path in path_list]

stuffs = ["electron", "jet", "muon", "photon", "tau"]


def specific_files(file_list):
    stuffs_csv = [stuff + ".csv" for stuff in stuffs]
    specific_file_list = [[file for stuff in stuffs_csv for file in files if file[-len(stuff):] == stuff] for files in file_list]
    return specific_file_list


def xy_data(event_num):
    x, y = [], []
    counts = 1

    for num_index, num in enumerate(event_num):

        if num_index != 0:

            if num == event_num[num_index - 1]:
                counts += 1
            else:
                x.append(counts)
                for i in range((num - 1) - event_num[num_index - 1]):
                    x.append(0)
                counts = 1

    x = np.array(x)

    for index in np.unique(np.sort(x)):
        temp = x[x == index]
        counts = len(temp)
        y.append(counts)

    x = np.unique(np.sort(x))
    y = np.array(y)
    y = y/np.sum(y)

    return x, y


def plot_values(files):
    plot_amount = len(files)
    diff = 200

    for i in range(1, plot_amount + 1):

        for j in range(1, plot_amount + 1):
            
            if i * j == plot_amount and np.abs(i - j) < diff:
                diff = np.abs(i - j)
                x, y = np.min((i, j)), np.max((i, j))
    
    return x, y


def plot_data(file_list):
    plt_data = []

    for files in file_list:
        temp_data = []

        for file in files:
            file = pd.read_csv(file)
            event_num = file["event#"]
            x, y = xy_data(event_num)
            temp_data.append((x, y))
        
        plt_data.append(temp_data)

    return plt_data


def plot_style(subfigs_list, plot_index, subfig_data):
    plot_subfig = subfigs_list[int(np.floor(plot_index/2)), int(np.abs(np.sin(plot_index*np.pi/2)))]
    plot_titles = os.listdir(folder_path)
    plot_subfig.suptitle(plot_titles[plot_index])
    subfigs = plot_subfig.subfigures(2, 1)
    axs_upper = subfigs[0].subplots(1, 2)
    axs_lower = subfigs[1].subplots(1, 3)
    subplot_titles = stuffs
    
    for data_index, data in enumerate(subfig_data):

        if data_index <= 1:
            ax = axs_upper[data_index]
        else:
            ax = axs_lower[data_index - 2]
        
        ax.set_title(subplot_titles[data_index])
        ax.grid()
        ax.bar(data[0], data[1])
        


def plot(file_list):
    fig = plt.figure()
    #style = "seaborn-darkgrid"
    #plt.style.use(style)
    x_len, y_len = plot_values(file_list)
    subfigs_list = fig.subfigures(nrows = x_len, ncols = y_len)
    plt_data = plot_data(file_list)
    for plot_index, data in enumerate(plt_data):
        plot_style(subfigs_list, plot_index, data)
    
    plt.show()

plot(specific_files(file_list))