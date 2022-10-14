from doctest import OutputChecker
import enum
from importlib.util import spec_from_file_location
from pathlib import Path
from re import sub
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

folder_path = "Data/Pandas/Individual/"
stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
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


def data_filter(data):
    mean, std_dev = np.mean(data), np.std(data)
    data = np.array(data)
    data = np.sort(data[data < mean + 3*std_dev])

    return data


def data_func(folder, filter, MET):
    temp_list_1 = []
    for files in folder:
        temp_list_2 = []
        for index, file in enumerate(files):
            if MET == True and index == 2:
                file = pd.read_csv(file)
                PT = file["PT"]
                event_num = file["event#"]
                temp_list_2.append(tuple(zip(PT, event_num)))
            elif MET == False:
                file = pd.read_csv(file)
                PT = file["PT"]
                event_num = file["event#"]
                temp_list_2.append(tuple(zip(PT, event_num)))
            else:
                pass

        temp_list_1.append(temp_list_2)
    
    data_list = []
    for data in temp_list_1:
        if filter == True:
            plt_data = data_filter(dict_to_data(data, files, MET))
        else:
            plt_data = dict_to_data(data, files, MET)
        data_list.append(plt_data)

    return data_list


def event_num_finder(data_list, files, MET):
    if MET == True:
        data = data_list[0]
        event_num = len(data)
    else:
        for index, data in enumerate(data_list):
            if files[index][-len("MET.csv"):] == "MET.csv":
                event_num = len(data)
    
    return event_num


def dict_to_data(data_list, files, MET):
    event_num = event_num_finder(data_list, files, MET)
    pt_sum = {}
    for i in range(event_num):
        pt_sum[i] = 0

    for index, data in enumerate(data_list):
        if MET == True:
            for tuple in data:
                pt_sum[tuple[1]] += 1
        elif MET == False and stuffs[index] != "MET":
            for tuple in data:
                pt_sum[tuple[1]] += 1

    return list(pt_sum.values())


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
    for plot_index, folder in enumerate(folder_list):
        subplots_data = data_func(folder, filter = False, MET = False)
        if folders[plot_index] != "Sphaleron":
            bh_data = []
            for data in subplots_data:
                for HT in data:
                    bh_data.append(HT)
        else:
            sphaleron_data = []
            for subplot_data in subplots_data:
                sphaleron_data.append(subplot_data)
    
    sphaleron_files = os.listdir(folder_path + "Sphaleron" + "/")

    for plot_index in range(len(sphaleron_files)):
        fig = plt.figure()
        style = "seaborn-darkgrid"
        plt.style.use(style)
        ax = fig.subplots(1, 1)
        ax.set_xlabel("Object Amount")
        ax.set_ylabel("Frequency of Events")
        plot_data = [bh_data, sphaleron_data[plot_index]]
        titles = ["BH", sphaleron_files[plot_index]]
        efficieny, efficieny_line = efficiency_value(plot_data, 1)
        ax.hist(plot_data, bins = 50, alpha = 0.75, label = titles, density = True)

        # for data_index, data in enumerate(plot_data):
        #     x, y = data_binner(data, 1, plot = True)
        #     title = titles[data_index]
        #     ax.plot(x, y, label = title)
        
        plt.axvline(x = efficieny_line, color = "r", label = str(efficieny) + "%")
        ax.legend(prop = {'size': 8})
        plt.show()



folder_list = filtered_list(folder_list_func(path_list_func(folder_path)), stuffs)
plot(folder_list)

