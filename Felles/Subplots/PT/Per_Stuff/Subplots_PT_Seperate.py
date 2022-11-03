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

folder_path = "Data/Pandas/Sum/"
stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]

def path_list_func(path):
    path_list = []
    folder_names = os.listdir(path)
    for name in folder_names:
        path_list.append(path + name)
    
    return path_list


def folder_list_func(path_list):
    folder_list = []
    for path in path_list:
        temp_list = []
        for name in os.listdir(path):
            temp_list.append(path + "/" + name)
        folder_list.append(temp_list)

    return folder_list


def filtered_list(folder_list, stuffs):
    stuffs_csv = [stuff + ".csv" for stuff in stuffs]
    filtered_files = []
    for files in folder_list:
        temp_list = []
        for file in files:
            for stuff in stuffs_csv:
                if file[-len(stuff):] == stuff:
                    temp_list.append(file)
        filtered_files.append(temp_list)
    
    return filtered_files


def data_filter(data):
    mean, std_dev = np.mean(data), np.std(data)
    data = np.array(data)
    data = np.sort(data[data < mean + 3*std_dev])

    return data


def data_func(files, filter):
    plt_data = []
    for file in files:
        file = pd.read_csv(file)
        if filter == True:
            PT = data_filter(file["PT"])
        else:
            PT = file["PT"]
        plt_data.append(PT)

    return plt_data



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


def subplots_func(fig, files, title):
    x_dim, y_dim = fig_dim(files)
    subplots_list = []
    if y_dim > 1:
        subfigs_y = fig.subfigures(y_dim, 1)
        subfigs_y[0].suptitle(title)
        for i in range(y_dim):
            for j in range(len(files)):
                if int(np.floor(j / x_dim)) == i and (int(np.floor((j + 1) / x_dim)) == i + 1 or len(files) == j + 1):
                    if len(files) == j + 1:
                        x_dim = len(files) - x_dim * (y_dim - 1)
                        if x_dim == 1:
                            subplots_x = [subfigs_y[i].subplots(1, x_dim)]
                        else:
                            subplots_x = subfigs_y[i].subplots(1, x_dim)
                    else:
                        subplots_x = subfigs_y[i].subplots(1, x_dim)
                    for subplot in subplots_x:
                        subplots_list.append(subplot)
    else:
        subfigs_y = [fig.subfigures(y_dim, 1)]
        subfigs_y[0].suptitle(title)
        if x_dim == 1:
            subplots_x = [subfigs_y[0].subplots(1, x_dim)]
        else:
            subplots_x = subfigs_y[0].subplots(1, x_dim)
        for subplot in subplots_x:
            subplots_list.append(subplot)
            
    return subplots_list


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
    fig_subfigs = subfigs_func(fig, folder_list)
    plot_titles = os.listdir(folder_path)

    for plot_index, files in enumerate(folder_list):
        subfig = fig_subfigs[plot_index]
        title = plot_titles[plot_index]
        subplots = subplots_func(subfig, files, title)
        subplots_data = data_func(files, filter = True)
        subplots_titles = stuffs

        for subplot_index in range(len(files)):
            data = subplots_data[subplot_index]
            title = subplots_titles[subplot_index]
            ax = subplots[subplot_index]
            ax.set_title(title)
            ax.hist(data, bins = 100)

    plt.show()


for i in range(len(stuffs)):
    stuffs_temp = stuffs[:(1 + i)]

    files_list = filtered_list(folder_list_func(path_list_func(folder_path)), stuffs_temp)

    plot(files_list)