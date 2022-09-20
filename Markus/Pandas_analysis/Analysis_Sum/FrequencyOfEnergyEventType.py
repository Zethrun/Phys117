import enum
from errno import ENETUNREACH
from re import X
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

#Retrieves all files from data folder
folder_path = "C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/Pandas/Sum/"
path_list = [folder_path + folder_name for folder_name in os.listdir(folder_path)]
file_list = [[path + "/" + filename for filename in os.listdir(path)] for path in path_list]

#Specifies data category to analyse and retrieves only those data files from above
stuffs = ["electron", "jet", "muon", "photon", "tau"]


def specific_files(file_list):
    stuffs_csv = [stuff + ".csv" for stuff in stuffs]
    specific_file_list = [[file for stuff in stuffs_csv for file in files if file[-len(stuff):] == stuff] for files in file_list]
    return specific_file_list


#Determines the shape of the subplot figure trying to be as square as possible
#Should change it in case the amount of subplots is a prime number
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



#Takes index of subplot and returns the name of folder as title
def subplot_title(index_plot):
    path = path_list[index_plot]
    title = path[len(folder_path):]
    return title


def data_filter(eta, PT):
    energy = np.sort(np.abs(PT/np.cos(eta)))
    median = np.median(energy)
    std_dev = np.sqrt(median)
    energy = energy[energy < median + 50*std_dev]
    return energy


def binsize_mean(energy, bins):
    mean = np.mean(energy)
    std_dev = np.std(energy)
    range = 3*std_dev
    binsize = np.round(2*range/bins, 2)
    return binsize, mean


#Takes the categorized datafiles from above and returns the data for a plot
def data_plot(files, bins):
    data = []

    for file in files:
        x, y = [], []
        file = pd.read_csv(file)
        eta, PT = file["eta"], file["PT"]
        energy = data_filter(eta, PT)
        binsize, mean = binsize_mean(energy, bins)

        for i in range(-int(bins/2), int(bins/2)):
            temp = energy
            temp = temp[temp < mean + (i + 1)*binsize]
            temp = temp[temp >= mean + i*binsize]
            x.append(mean + (i + 1/2)*binsize)
            y.append(len(temp))

        y = y/np.sum(y)
        data.append((x, y))

    return data


#Plots the data in a typical plot
def plot_plot(data, x_len, y_len, index_plot, title):
    for index, (x, y) in enumerate(data):
        style = "seaborn-darkgrid"
        plt.style.use(style)
        plt.subplot(x_len, y_len, index_plot + 1)
        plt.title(title)
        label = stuffs[index]
        plt.plot(data[index][0], data[index][1], label = label)
        plt.legend()
        plt.grid()


#Takes the data from the file_list and runs it through the functions above plotting the data
def plot(file_list):
    bins = 20
    plt.figure()
    (x_len, y_len) = plot_values(file_list)

    for index_plot, files in enumerate(file_list):
        data = data_plot(files, bins)
        title = subplot_title(index_plot)
        plot_plot(data, x_len, y_len, index_plot, title)
    
    plt.show()

plot(specific_files(file_list))