# Import modules
from tqdm import tqdm
import numpy as np
import os

# Import functions
from FilesFunc import files

# Data variables
def work_space(path):
    while True:
        if os.path.split(path)[1] != "Phys117":
            path = os.path.split(path)[0]
        else:
            return path.replace("\\", "/")

work_dir = work_space(os.getcwd())
data_path = work_dir + "/Data/Pandas/"
individual = True
folders = ["Background", "BH", "Sphaleron"]
stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
bool_list = [True, False]
file_amounts = [1, 1]



def unpacker(folder_data, new_folder_data):
    for nested_list in folder_data:
        if type(nested_list) == list:
            unpacker(nested_list, new_folder_data)
        else:
            new_folder_data.append(nested_list)
    folder_data = new_folder_data
    return folder_data


def tuple_unpacker(folder_data, new_folder_data):
    for nested_list in folder_data:
        if type(nested_list) == list or type(nested_list) == tuple:
            tuple_unpacker(nested_list, new_folder_data)
        else:
            new_folder_data.append(nested_list)
    folder_data = new_folder_data
    return folder_data


def data_binner(data, binsize, plot):
    data = [data for data in tuple_unpacker(data, []) if type(data) != str]

    if len(data) == 0:
        x = [bin * binsize for bin in range(200)]
        y = [0 for bin in range(200)]
        return x, y

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
 

def efficiency_value(efficiency_data, binsize):
    bh_data, sphal_data = efficiency_data
    bh_data = [data for data in tuple_unpacker(bh_data, []) if type(data) != str]
    sphal_data = [data for data in tuple_unpacker(sphal_data, []) if type(data) != str]
    x_bh, y_bh = data_binner(bh_data, binsize, plot = False)
    x_sphal, y_sphal = data_binner(sphal_data, binsize, plot = False)
    x_interval = np.concatenate((x_bh, x_sphal))
    x_min, x_max = np.min(x_interval), np.max(x_interval)
    bins = int(np.round((x_max - x_min)/binsize))
    x = [x_min + (bin + 1)*binsize for bin in range(bins + 1)]
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
                temp_efficiency.append((total_efficiency, "BH < Sphal"))
            else:
                temp_efficiency.append((total_efficiency, "BH > Sphal"))



        total_efficiencies.append((*sorted(temp_efficiency, key = lambda x: x[0])[-1], bin))
    
    max_efficiency = sorted(total_efficiencies, key = lambda x: x[0])[-1]
    me_value = max_efficiency[0] / 2
    me_dir = max_efficiency[1]
    me_bin = max_efficiency[2]
    me_x = x_min + me_bin * binsize
    
    return [me_x, me_value, me_dir]



PT_max = bool_list[0]
if PT_max:
    file_amounts = [1, 1]
    stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
    
    folder_list, filename_list = files(individual, data_path, folders, stuffs, file_amounts)
    efficiencies = []

    for sphal_index, sphal_file in enumerate(folder_list[1]):
        for bh_index, bh_file in enumerate(folder_list[0]):
            data_folder_list = [[bh_file], [sphal_file]]
            name_list = [[filename_list[0][bh_index]], [filename_list[1][sphal_index]]]

            from Bdata import PT_max_data

            (data_variable, combine_files, by_particle) = ("PT", False, False)

            folders_data = []
            for folder_index, folder in tqdm(enumerate(data_folder_list)):
                plot_data = PT_max_data(folder, stuffs, by_particle, data_variable, combine_files)
                folders_data.append(plot_data)

            efficiency_data = []
            for folder_index, folder_data in enumerate(folders_data):
                plot_data = unpacker(folder_data, [])
                efficiency_data.append(plot_data)
            eff_tup = efficiency_value(efficiency_data, binsize = 1)
            efficiencies.append(eff_tup)

    av_eff = np.sum([eff_tup[0] for eff_tup in efficiencies]) / len(efficiencies)
    print(av_eff)


stuff_amount = bool_list[0]
if stuff_amount:
    file_amounts = [1, 1]
    stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
    
    folder_list, filename_list = files(individual, data_path, folders, stuffs, file_amounts)
    efficiencies = []

    for sphal_index, sphal_file in enumerate(folder_list[1]):
        for bh_index, bh_file in enumerate(folder_list[0]):
            data_folder_list = [[bh_file], [sphal_file]]
            name_list = [[filename_list[0][bh_index]], [filename_list[1][sphal_index]]]

            from Bdata import stuff_amount_data

            (data_variable, combine_files) = ("PT", False)

            folders_data = []
            for folder_index, folder in tqdm(enumerate(data_folder_list)):
                plot_data = stuff_amount_data(folder, stuffs, data_variable, combine_files)
                folders_data.append(plot_data)

            efficiency_data = []
            for folder_index, folder_data in enumerate(folders_data):
                plot_data = unpacker(folder_data, [])
                efficiency_data.append(plot_data)
            eff_tup = efficiency_value(efficiency_data, binsize = 1)
            efficiencies.append(eff_tup)

    av_eff = np.sum([eff_tup[0] for eff_tup in efficiencies]) / len(efficiencies)
    print(av_eff)


MET_dist = bool_list[0]
if MET_dist:
    file_amounts = [1, 1]
    stuffs = ["MET"]
    
    folder_list, filename_list = files(individual, data_path, folders, stuffs, file_amounts)
    efficiencies = []

    for sphal_index, sphal_file in enumerate(folder_list[1]):
        for bh_index, bh_file in enumerate(folder_list[0]):
            data_folder_list = [[bh_file], [sphal_file]]
            name_list = [[filename_list[0][bh_index]], [filename_list[1][sphal_index]]]

            from Bdata import MET_data

            (data_variable, combine_files, by_particle) = ("PT", False, False)

            folders_data = []
            for folder_index, folder in tqdm(enumerate(data_folder_list)):
                plot_data = MET_data(folder, stuffs, data_variable, combine_files)
                folders_data.append(plot_data)


            efficiency_data = []
            for folder_index, folder_data in enumerate(folders_data):
                plot_data = unpacker(folder_data, [])
                efficiency_data.append(plot_data)
            eff_tup = efficiency_value(efficiency_data, binsize = 1)
            efficiencies.append(eff_tup)

    av_eff = np.sum([eff_tup[0] for eff_tup in efficiencies]) / len(efficiencies)
    print(av_eff)


