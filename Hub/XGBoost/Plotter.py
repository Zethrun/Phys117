# Import modules
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
import numpy as np
import os
stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
data_variables = ["HT", "met", "phi_diff", "ptmax", "stuff_amount"]
file_amounts = [2, 18, 3]
font = {'family': 'Times New Roman',
        'color':  'black',
        'weight': 'normal'
        }


def work_space(path):
    while True:
        if os.path.split(path)[1] != "Programs":
            path = os.path.split(path)[0]
        else:
            return path.replace("\\", "/")

work_dir = work_space(os.getcwd())
data_path = work_dir + "/Hub/VariableData/"
folders = os.listdir(data_path)
data_files = [data_path + data_file for data_file in folders]


def remover(old_list, index):
    new_list = [element for element_index, element in enumerate(old_list) if element_index != index]
    return new_list


def unpacker(folder_data, new_folder_data):
    for nested_list in folder_data:
        if type(nested_list) == list:
            unpacker(nested_list, new_folder_data)
        else:
            new_folder_data.append(nested_list)
    folder_data = new_folder_data
    return folder_data


def data_binner(data, binsize):
    data = unpacker(data, [])

    if len(data) == 0:
        x = [bin * binsize for bin in range(200)]
        y = [0 for bin in range(200)]
        return x, y

    max_value = np.max(data)
    bins = int(np.round(max_value / binsize))
    bins = np.arange(0, bins)
    data = np.array(data)
    x, y = [], []

    for bin in range(len(bins)):
        temp = data
        temp = temp[temp <= (bin + 1/2)*binsize]
        temp = temp[(bin - 1/2)*binsize < temp]
        if len(temp) != 0:
            y.append(len(temp))
            x.append(bin*binsize)

    y = y/np.sum(y)

    return x, y


def plot_filter(interval_data, filter_strength):
    interval_data = sorted(interval_data)
    cutoff = round((len(interval_data) * filter_strength))
    interval_data = interval_data[:cutoff]
    x_min = np.min(interval_data)
    x_max = np.max(interval_data)
    extra = (x_max - x_min) / 10
    return [x_min - extra, x_max + extra]


def sampler(output_dataframe, output_filenames, file_amounts, combine_data):
    from random import sample

    output_dataframe = [[(dataframe, filename) for dataframe, filename in zip(dataframes, filenames)] for dataframes, filenames in zip(output_dataframe, output_filenames)]
    samples = [sample(dataframes, file_amount) for dataframes, file_amount in zip(output_dataframe, file_amounts)]

    if combine_data:
        output_dataframe = [pd.concat([sample[0] for sample in dataframes]) for dataframes in samples]
        labels = folders
    else:
        output_dataframe = [[sample[0] for sample in dataframes] for dataframes in samples]
        labels = [[sample[1] for sample in dataframes] for dataframes in samples]

    return output_dataframe, labels


def plotter(variables, output_dataframes, output_filenames, colors, filter_strengths, binsizes, figsize):
    titles = ["$H_T$", "MET", "$\phi_{diff}$ (Largest $P_T$ vs MET)", "$P_{Tmax}$", "Object Multiplicity"]
    xlabels = ["[GeV]", "[GeV]", "[Radians]", "[GeV]", ""]
    for variable in variables:
        fig = plt.figure(figsize = (12, figsize))
        style = "seaborn-darkgrid"
        plt.style.use(style)
        subplots = fig.subplots(2, 1)
        for i in range(2):
            dataframes = unpacker(output_dataframes, [])
            filenames = unpacker(output_filenames, [])
            if i == 1:
                dataframes = unpacker(remover(output_dataframes, 0), [])
                filenames = unpacker(remover(output_filenames, 0), [])
            color_indices = [0, 0, 0]
            ax = subplots[i]
            if i == 0:
                title = titles[data_variables.index(variable)] + " Distribution"
                ax.set_title(title, fontdict = font, fontsize = 24)
            if i == 1:
                xlabel = titles[data_variables.index(variable)] + " " + xlabels[data_variables.index(variable)]
                ax.set_xlabel(xlabel, fontdict = font, fontsize = 16)
            ax.set_ylabel("Relative Frequency", fontdict = font, fontsize = 16)

            binsize = binsizes[data_variables.index(variable)] if type(binsizes) == list else binsizes
            filter_strength = filter_strengths[data_variables.index(variable)] if type(filter_strengths) == list else filter_strengths
            interval = np.concatenate([dataframe[variable] for dataframe in dataframes])
            ax.set_xlim(plot_filter(interval, filter_strength))

            for dataframe, label in zip(dataframes, filenames):
                raw_data = dataframe[variable]
                bins, counts = data_binner(raw_data, binsize)
                if label[:len("ttbar")] == "ttbar":
                    color = colors[0][color_indices[0]]
                    color_indices[0] += 1
                    ax.plot(bins, counts, label = label, color = color)
                elif label[:len("BH")] == "BH":
                    color = colors[1][color_indices[1]]
                    color_indices[1] += 1
                    ax.plot(bins, counts, label = label, color = color)
                else:
                    color = colors[2][color_indices[2]]
                    color_indices[2] += 1
                    ax.plot(bins, counts, label = label, color = color)
            
            ax.legend(prop = {'size': 8})
        plt.show()
        plt.close()