# Import modules
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
import numpy as np
import os


def work_space(path):
    while True:
        if os.path.split(path)[1] != "Phys117":
            path = os.path.split(path)[0]
        else:
            return path.replace("\\", "/")

work_dir = work_space(os.getcwd())
data_path = work_dir + "/Markus/Hub/VariableData/"
folders = os.listdir(data_path)
data_files = [data_path + data_file for data_file in folders]
stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
data_variables = ["met", "HT", "stuff_amount", "ptmax", "phi_diff"]
file_amounts = [2, 18, 3]


def unpacker(folder_data, new_folder_data):
    for nested_list in folder_data:
        if type(nested_list) == list:
            unpacker(nested_list, new_folder_data)
        else:
            new_folder_data.append(nested_list)
    folder_data = new_folder_data
    return folder_data


def efficiencies_data(efficiency_data, binsize):
    bh_data, sphal_data = efficiency_data
    x_bh, y_bh = data_binner(bh_data, binsize, plot = False)
    x_sphal, y_sphal = data_binner(sphal_data, binsize, plot = False)
    x_interval = np.concatenate((x_bh, x_sphal))
    x_min, x_max = np.min(x_interval), np.max(x_interval)
    bins = int(np.round((x_max - x_min)/binsize))
    total_efficiencies = []

    for bin in range(bins + 1):
        bh_left = y_bh[:bin + 1]
        bh_right = y_bh[bin + 1:]
        bh_split = [bh_left, bh_right]
        
        sphal_left = y_sphal[:bin + 1]
        sphal_right = y_sphal[bin + 1:]
        sphal_split = [sphal_right, sphal_left]

        temp_efficiency = []
        for i in range(len(["left", "right"])):
            bh_efficiency = np.sum(bh_split[i])
            sphal_efficiency = np.sum(sphal_split[i])
            total_efficiency = bh_efficiency + sphal_efficiency
            if i == 0:
                temp_efficiency.append((total_efficiency, 0))
            else:
                temp_efficiency.append((total_efficiency, 1))


        total_efficiencies.append((*sorted(temp_efficiency, key = lambda x: x[0])[-1], bin))
    
    max_efficiency = sorted(total_efficiencies, key = lambda x: x[0])[-1]
    me_value = max_efficiency[0] / 2
    me_dir = max_efficiency[1]
    me_bin = max_efficiency[2]
    me_x = x_min + me_bin * binsize
    
    return [me_x, me_value, me_dir]


def data_binner(data, binsize, plot):
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

    if plot:
        for bin in range(len(bins)):
            temp = data
            temp = temp[temp <= (bin + 1/2)*binsize]
            temp = temp[(bin - 1/2)*binsize < temp]
            if len(temp) != 0:
                y.append(len(temp))
                x.append(bin*binsize)

        y = y/np.sum(y)

        return x, y
    else:
        for bin in range(len(bins)):
            temp = data
            temp = temp[temp <= (bin + 1/2)*binsize]
            temp = temp[(bin - 1/2)*binsize < temp]
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


def sampler(output_dataframe, output_filenames, folders, file_amounts, combine_data):
    folders = [folder for folder, file_amount in zip(folders, file_amounts) if file_amount != 0]


    from random import sample
    output_dataframe = [[(dataframe, filename) for dataframe, filename in zip(dataframes, filenames)] for dataframes, filenames in zip(output_dataframe, output_filenames)]
    samples = [sample(dataframes, file_amount) for dataframes, file_amount in zip(output_dataframe, file_amounts)]
    samples = [dataframes for dataframes in samples if len(dataframes) != 0]


    if combine_data:
        output_dataframe = [pd.concat([sample[0] for sample in dataframes]) for dataframes in samples]
        labels = folders
    else:
        output_dataframe = [[sample[0] for sample in dataframes] for dataframes in samples]
        labels = [[sample[1] for sample in dataframes] for dataframes in samples]


    return output_dataframe, labels, folders


def eff_calc(data_sample, labels, combine_data, data_variables, binsizes):
    rows, columns = labels
    columns = [columns] if type(columns) != list else columns
    rows = [rows] if type(rows) != list else rows

    for variable_index, variable in enumerate(data_variables):
        data = {column: [] for column in columns}
    
        if combine_data:
            filename = variable + "Combined"
            dataframes = data_sample
            raw_data = [dataframe[variable] for dataframe in dataframes]
            binsize = binsizes[variable_index] if type(binsizes) == list else binsizes
            me_x, me_value, me_dir = efficiencies_data(raw_data, binsize)
            data[columns[0]].append((me_x, me_value, me_dir))
            print(f'{"Maximum Efficiency is: "}', f'{np.round(me_value, 3):5}', " at ", f'{variable:12}', " = ", f'{np.round(me_x, 2):5}', ", with ", f'{me_dir:10}')

        else:
            filename = variable
            for row_index, bh_data in enumerate(data_sample[folders.index("BH")]):
                for column_index, sphal_data in enumerate(data_sample[folders.index("Sphaleron")]):
                    dataframes = [bh_data, sphal_data]
                    raw_data = [dataframe[variable] for dataframe in dataframes]
                    binsize = binsizes[variable_index] if type(binsizes) == list else binsizes
                    me_x, me_value, me_dir = efficiencies_data(raw_data, binsize)
                    data[columns[column_index]].append((me_x, me_value, me_dir))
                    print(f'{"Maximum Efficiency is: "}', f'{np.round(me_value, 3):5}', " at ", f'{variable:12}', " = ", f'{np.round(me_x, 2):5}', ", with ", f'{me_dir:10}')
        
        save_path = work_dir + "/Markus/Hub/Efficiencies/EfficiencyData/" + filename + ".csv"
        pd.DataFrame(data = data, columns = columns, index = rows).to_csv(save_path)



from FilesFunc import files
folder_list, filename_list = files(data_path, folders, file_amounts)
foldered_dataframes = [[pd.read_csv(data_file).drop("Unnamed: 0", axis = 1) for data_file in folder_files] for folder_files in folder_list]



combine_data = False
data_sample, labels, folders = sampler(foldered_dataframes, filename_list, folders, file_amounts = [0, 18, 3], combine_data = combine_data)
eff_calc(data_sample, labels, combine_data, data_variables, binsizes = [50, 50, 0.5, 50, 0.2])