# Import modules
import numpy as np
from tqdm import tqdm
import pandas as pd
import os


def remover(old_list, to_be_removed):
    if type(to_be_removed) == list:
        new_list = [element for element in old_list if element not in to_be_removed]
    else:
        new_list = [element for element in old_list if element != to_be_removed and type(element) == type(to_be_removed)]
    return new_list


def event_num_finder(file_data, stuffs):
    for stuff_index, stuff_data in enumerate(file_data):
        filename = stuffs[stuff_index]
        if filename == "MET":
            event_num = len(stuff_data)

    return event_num


def events(file_data, stuffs):
    event_num = event_num_finder(file_data, stuffs)
    file_data = unpacker(file_data, [])
    events_list = {i: [] for i in range(event_num)}
    for data_tuple in file_data:
        events_list[data_tuple[1]].append(data_tuple)
    events_tupes = [tuple(event) for event in list(events_list.values())]
    return events_tupes


def data(folder, stuffs, folder_name, data_variables):
    folder_data = []
    for file in folder:
        file_data = []
        for stuff_data in file:
            stuff_name = os.path.split(stuff_data)[1]
            if stuff_name[:-len(".csv")] in stuffs:
                data = pd.read_csv(stuff_data)
                variables_data = [data[data_variable] for data_variable in data_variables]
                particle_name = [stuff_name[:-len(".csv")] for i in range(len(variables_data[0]))]
                dataset = [folder_name for i in range(len(variables_data[0]))]
                data_tuple_list = list(zip(dataset, *variables_data, particle_name))
                file_data.append(data_tuple_list)
        file_data = events(file_data, stuffs)
        folder_data.append(file_data)
    return folder_data


def unpacker(folder_data, new_folder_data):
    for nested_list in folder_data:
        if type(nested_list) == list:
            unpacker(nested_list, new_folder_data)
        else:
            new_folder_data.append(nested_list)
    folder_data = new_folder_data
    return folder_data


def data_binner(data, binsize, plot):
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
 

def efficiency_value(train_data, binsize):
    bh_data, sphal_data = train_data
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


bool_list = [True, False]
dataset_index = 0
event_num_index = 1
eta_index = 2
phi_index = 3
pt_index = 4
jmass_index = 5
ntrk_index = 6
btag_index = 7
hadem_index = 8
particle_name_index = 9


# Import functions
from Afiles import files
individual = True
data_path = "C:/Users/mhals/Dropbox/PC (2)/Documents/GitHub/Phys117/Data/Pandas/Individual/"
data_variables = ["event#", "eta", "phi", "PT", "jmass", "ntrk", "btag", "hadem"]
folders = ["Background", "BH", "Sphaleron"]
stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
file_amounts = [2, 18, 3]
folder_list, filename_list = files(individual, data_path, folders, stuffs, file_amounts)


event_data = unpacker([data(folder, stuffs, folder_name, data_variables) for folder, folder_name in zip(folder_list, folders)], [])

old_counts = [1 for stuff in stuffs]
for event in event_data:
    new_counts = [1 for stuff in stuffs]
    for particle in event:
        for stuff_index, stuff in enumerate(stuffs):
            new_counts[stuff_index] += 1 if particle[particle_name_index] == stuff else 0
    for count_index, new_count in enumerate(new_counts):
        old_counts[count_index] = new_count if new_count > old_counts[count_index] else old_counts[count_index]

counts = old_counts
print(counts)


particles = np.array([stuff + str(count_index) for stuff_index, stuff in enumerate(stuffs) for count_index in range(1, counts[stuff_index])])
data_variables = np.array(["ptmax", "stuff_amount", "MET"])
data = {stuff + "-" + str(count_index) + "." + str(variable_index): [np.nan for i in range(len(event_data))] for stuff_index, stuff in enumerate(stuffs) for count_index in range(1, counts[stuff_index]) for variable_index in range(len(data_variables))}
data["dataset"] = [0 for i in range(len(event_data))]



for event_index, event in enumerate(event_data):
    event_counts = [1 for stuff in stuffs]
    ptmax = sorted(event, key = lambda x: x[pt_index])[-1][pt_index]
    stuff_amount = len(event) - 1
    met = [particle for particle in event if particle[particle_name_index] == "MET"][0][pt_index]
    for particle in event:
        for stuff_index, stuff in enumerate(stuffs):
            if particle[particle_name_index] == stuff:
                count_index = event_counts[stuff_index]
                particle_data = list(remover(particle, [particle[dataset_index], particle[event_num_index], particle[particle_name_index]]))
                particle_data.extend([ptmax, stuff_amount, met])
                for variable_index, variable_data in enumerate(particle_data):
                    data[stuff + "-" + str(count_index) + "." + str(variable_index)][event_index] = variable_data
                event_counts[stuff_index] += 1
    data["dataset"][event_index] = folders.index(event[0][dataset_index])


particles = [particle for particle in particles for i in range(len(data_variables))]
data_variables = list(data_variables) * np.sum(counts)
for i in range(len(event_data) - len(data_variables)):
    data_variables.extend([np.nan])
for i in range(len(event_data) - len(particles)):
    particles.extend([np.nan])
particles = np.array(particles)
data_variables = np.array(data_variables)

data["data_variables"] = data_variables
data["particles"] = particles



event_data = pd.DataFrame(data)
print(event_data)
event_data.to_csv("Markus/Pandas_analysis/Subplots/Hub/EventData.csv")