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
    pt_lists = {}
    for i in range(event_num):
        pt_lists[i] = []

    for index, data in enumerate(data_list):
        if MET == True:
            for tuple in data:
                pt_lists[tuple[1]].append(tuple[0])
        elif MET == False and stuffs[index] != "MET":
            for tuple in data:
                pt_lists[tuple[1]].append(tuple[0])
    
    max_values = []
    for pt_list in list(pt_lists.values()):
        if len(pt_list) == 0:
            max_values.append(0)
        else:
            max_value = np.max(pt_list)
            max_values.append(max_value)

    return max_values


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


def plot(folder_list):
    fig = plt.figure()
    style = "seaborn-darkgrid"
    plt.style.use(style)
    ax = fig.subplots(1, 1)
    ax.set_xlabel("Object PT [GeV]")
    ax.set_ylabel("Frequency of Events")
    plot_titles = folders

    plot_data = []

    for plot_index, folder in enumerate(folder_list):
        subplots_data = data_func(folder, filter = False, MET = False)
        subplot_data = []
        for data in subplots_data:
            for HT in data:
                subplot_data.append(HT)
        plot_data.append(subplot_data)

    
    ax.hist(plot_data, bins = 500, alpha = 0.75, density = True, label = plot_titles, histtype = "step")
    ax.set_xlim(0, 4000)
    ax.legend(prop = {'size': 8})

    plt.show()


folder_list = filtered_list(folder_list_func(path_list_func(folder_path)), stuffs)
plot(folder_list)