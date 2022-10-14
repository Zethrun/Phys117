from doctest import OutputChecker
import enum
from fileinput import filename
from importlib.util import spec_from_file_location
from pathlib import Path
from re import sub
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

folder_path = "Data/Pandas/Individual/"
stuffs = ["MET"]
folders = ["BH", "Sphaleron"]

def path_list_func(path):
    temp_list = []
    folder_names = os.listdir(path)
    for name in folder_names:
        if name in folders:
            temp_list.append(path + name)
    
    path_list = []
    for path in temp_list:
        folder_names = os.listdir(path)
        path_list.append([path + "/" + name for name in folder_names])

    return path_list


def folder_list_func(path_list):
    folder_list = []
    for paths in path_list:
        temp_list_1 = []
        for path in paths:
            temp_list_2 = []
            for name in os.listdir(path):
                temp_list_2.append(path + "/" + name)
            temp_list_1.append(temp_list_2)
        folder_list.append(temp_list_1)

    return folder_list


def filtered_list(folder_list, stuffs):
    stuffs_csv = [stuff + ".csv" for stuff in stuffs]
    filtered_files = []
    for file_list in folder_list:
        temp_list_1 = []
        for files in file_list:
            temp_list_2 = []
            for file in files:
                for stuff in stuffs_csv:
                    if file[-len(stuff):] == stuff:
                        temp_list_2.append(file)
            temp_list_1.append(temp_list_2)
        filtered_files.append(temp_list_1)
    
    return filtered_files


def data_filter(data, filter_strength):
    mean, std_dev = np.mean(data), np.std(data)
    data = np.array(data)
    data = np.sort(data[data < mean + filter_strength*std_dev])

    return data


def data_func(folder, filter, filter_strength):
    data_list = []
    for files in folder:
        temp_list = []
        for file in files:
            file = pd.read_csv(file)
            if filter == True:
                MET_pt = data_filter(file["PT"], filter_strength)
            else:
                MET_pt = file["PT"]
            temp_list.append(MET_pt)
        data_list.append(temp_list)

    return data_list


def fig_dim(files):
    plot_amount = len(files)
    dim = int(np.ceil(np.sqrt(plot_amount)))
    for i in range(1, dim + 1):
        for j in range(1, dim + 1):
            try:
                if i * j >= plot_amount and i * j - plot_amount <= diff:
                    diff = np.abs(i - j)
                    x_dim, y_dim = np.max((i, j)), np.min((i, j))
                    if i * j == plot_amount:
                        return x_dim, y_dim             
            except:
                diff = plot_amount
                x_dim, y_dim = np.max((i, j)), np.min((i, j))

    return x_dim, y_dim


def subfigs_func(fig, files):
    x_dim, y_dim = fig_dim(files)
    subfigs_list = []
    if y_dim > 1:
        subfigs_y = fig.subfigures(y_dim, 1)
        for i in range(y_dim):
            for j in range(len(files)):
                if int(np.floor(j / x_dim)) == i and (int(np.floor((j + 1) / x_dim)) == i + 1 or len(files) == j + 1):
                    if len(files) == j + 1:
                        x_dim = len(files) - x_dim * (y_dim - 1)
                        if x_dim == 1:
                            subfigs_x = [subfigs_y[i].subfigures(1, x_dim)]
                        else:
                            subfigs_x = subfigs_y[i].subfigures(1, x_dim)
                    else:
                        subfigs_x = subfigs_y[i].subfigures(1, x_dim)
                    for subfig in subfigs_x:
                        subfigs_list.append(subfig)
    else:
        subfigs_y = [fig.subfigures(y_dim, 1)]
        if x_dim == 1:
            subfigs_x = [subfigs_y[0].subfigures(1, x_dim)]
        else:
            subfigs_x = subfigs_y[0].subfigures(1, x_dim)
        for subfig in subfigs_x:
            subfigs_list.append(subfig)

    return subfigs_list


def data_binner(data, binsize, plot):
    max_value = np.max(data)
    bins = int(np.round(max_value / binsize))
    bins = np.arange(0, bins)
    data = np.array(data)
    x, y = [], []

    if plot == True:
        for bin in range(len(bins)):
            temp = data
            temp = temp[temp <= (bin + 1/2)*binsize]
            temp = temp[(bin - 1/2)*binsize < temp]
            if len(temp) != 0:
                y.append(len(temp))
                x.append(bin)

        y = y/np.sum(y)

        return x, y

    else:
        for bin in range(len(bins)):
            temp = data
            temp = temp[temp <= (bin + 1/2)*binsize]
            temp = temp[(bin - 1/2)*binsize < temp]
            y.append(len(temp))
            x.append(bin)

        y = y/np.sum(y)

        return x, y


def efficiency_value(data, binsize):
    bh_data, sphal_data = data
    x_bh, y_bh = data_binner(bh_data, binsize, plot = False)
    x_sphal, y_sphal = data_binner(sphal_data, binsize, plot = False)
    x_interval = np.concatenate((x_bh, x_sphal))
    x_min, x_max = np.min(x_interval), np.max(x_interval)
    binsize = x_bh[1] - x_bh[0]
    bins = int(np.round((x_max - x_min)/binsize))
    efficiencies = []

    for bin in range(bins + 1):
        sphal_left = y_sphal[:bin + 1]
        sphal_right = y_sphal[bin + 1:]
        sphal_split = [sphal_left, sphal_right]

        bh_left = y_bh[:bin + 1]
        bh_right = y_bh[bin + 1:]
        bh_split = [bh_right, bh_left]
        
        temp_efficiencies = []
        for i in range(len(["left", "right"])):
            sphal_efficiency = np.sum(sphal_split[i])/2
            bh_efficiency = np.sum(bh_split[i])/2
            total_efficiency = sphal_efficiency + bh_efficiency
            temp_efficiencies.append(total_efficiency)
        temp_efficiencies = sorted(temp_efficiencies)
        efficiencies.append((temp_efficiencies[-1], bin))
    
    sorted_list = sorted(efficiencies, key = lambda x: x[0])
    efficiency_data = sorted_list[-1]
    efficieny = np.round(efficiency_data[0], 5) * 100
    bin = efficiency_data[1]
    efficieny_line = x_min + bin*binsize

    return efficieny, efficieny_line


def plot(folder_list):
    fig = plt.figure()
    style = "seaborn-darkgrid"
    plt.style.use(style)
    ax = fig.subplots(1, 1)
    ax.set_xlabel("MET_pt [GeV]")
    ax.set_ylabel("Frequency of Events")
    plot_titles = folders
    efficiency_data = []


    for plot_index, folder in enumerate(folder_list):
        subplots_data = data_func(folder, filter = True, filter_strength = 3)
        plot_data = []
        for data in subplots_data:
            for PT in data:
                for real_PT in PT:
                    plot_data.append(real_PT)
        x, y = data_binner(plot_data, 30, plot = True)
        print(y)
        ax.plot(x, y, label = plot_titles[plot_index])
        efficiency_data.append(plot_data)
    
    efficieny, efficieny_line = efficiency_value(efficiency_data, 30)
    plt.axvline(x = efficieny_line, color = "r", label = str(efficieny) + "%")
    ax.legend(prop = {'size': 8})
    plt.show()


folder_list = filtered_list(folder_list_func(path_list_func(folder_path)), stuffs)
plot(folder_list)