from doctest import OutputChecker
import enum
from importlib.util import spec_from_file_location
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

folder_path = "Data/Pandas/Sum/"
path_list = [folder_path + folder_name for folder_name in os.listdir(folder_path)]
file_list = [[path + "/" + filename for filename in os.listdir(path)] for path in path_list]

stuffs = ["electron", "jet", "MET", "muon"]


def specific_files(file_list):
    stuffs_csv = [stuff + ".csv" for stuff in stuffs]
    specific_file_list = [[file for stuff in stuffs_csv for file in files if file[-len(stuff):] == stuff] for files in file_list]
    return specific_file_list


def data_filter(PT):
    mean = np.mean(PT)
    std_dev = np.std(PT)
    PT = np.array(PT)
    PT = np.sort(PT[PT < mean + 3*std_dev])
    return PT


def binsize_func(PT):
    bin_amount = 100
    diff = np.max(PT) - np.min(PT)
    binsize = diff/bin_amount
    bins = []

    for index in range(bin_amount):
        bins.append(index*binsize)

    return binsize, bins


def xy_data(PT):
    x, y = [], []
    binsize, bins = binsize_func(PT)
    
    for index, bin in enumerate(bins):
        temp = np.array(PT)
        temp = temp[temp > index*binsize]
        temp = temp[temp <= (index + 1)*binsize]
        x.append(index*binsize)
        y.append(len(temp))

    return x, y


def plot_values(files):
    plot_amount = len(files)
    diff = 200

    for i in range(0, plot_amount + 1):

        for j in range(0, plot_amount + 1):
            
            if i + j == plot_amount and np.abs(i - j) < diff:
                diff = np.abs(i - j)
                x, y = np.max((i, j)), np.min((i, j))
    if x == y == 1:
        x, y = 2, 0

    return x, y


def plot_data(file_list):
    plt_data = []

    for files in file_list:
        temp_data = []

        for file in files:
            file = pd.read_csv(file)
            PT = data_filter(file["PT"])
            x, y = xy_data(PT)
            temp_data.append((x, y))
        
        plt_data.append(temp_data)

    return plt_data


def plot_subfigs(fig, file_list):
    x_len, y_len = plot_values(file_list)
    subfigs_list = []
    
    if y_len >= 1:
        subfigs = fig.subfigures(2, 1)
        subfigs_upper = subfigs[0].subfigures(1, y_len)
        subfigs_lower = subfigs[1].subfigures(1, x_len)
        for subfig in subfigs_upper:
            subfigs_list.append(subfig)
    else:
        subfigs_lower = fig.subfigures(1, x_len)

    for subfig in subfigs_lower:
        subfigs_list.append(subfig)

    return subfigs_list


def plot_style(subfigs_list, plot_index, subfig_data):
    plot_subfig = subfigs_list[plot_index]
    plot_titles = os.listdir(folder_path)
    x_len, y_len = plot_values(subfig_data)

    if y_len >= 1:
        subfigs = plot_subfig.subfigures(2, 1)
    else:
        subfigs = [plot_subfig.subfigures(1, 1)]
    print(subfigs)
    subfigs[0].suptitle(plot_titles[plot_index])
    axs = []
    subplot_titles = stuffs

    if len(subfigs) == 1:
        axs_lower = subfigs[0].subplots(1, x_len)

        if x_len == 1:
            axs.append([axs_lower])
        else:
            axs.append(axs_lower)

        for index, data in enumerate(subfig_data):
            binsize = data[0][1] - data[0][0]
            ax = axs[0][index]
            ax.set_title(subplot_titles[index])
            ax.bar(data[0], data[1], width = binsize)
    
    else:
        axs_lower = subfigs[0].subplots(1, x_len)
        axs_upper = subfigs[1].subplots(1, y_len)
        axs.append(axs_lower)

        if y_len == 1:
            axs.append([axs_upper])
        else:
            axs.append(axs_upper)

        for index, data in enumerate(subfig_data):
            binsize = data[0][1] - data[0][0]

            if index - x_len >= 0:
                ax = axs[1][index - x_len]
            else:
                ax = axs[0][index]
            
            ax.set_title(subplot_titles[index])
            ax.bar(data[0], data[1], width = binsize)


def plot(file_list):
    fig = plt.figure()
    style = "seaborn-darkgrid"
    plt.style.use(style)
    subfigs_list = plot_subfigs(fig, file_list)
    plt_data = plot_data(file_list)

    for plot_index, data in enumerate(plt_data):
        plot_style(subfigs_list, plot_index, data)
    
    plt.show()


for i in range(len(stuffs)):
    stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
    stuffs = stuffs[:(1 + i)]
    plot(specific_files(file_list))