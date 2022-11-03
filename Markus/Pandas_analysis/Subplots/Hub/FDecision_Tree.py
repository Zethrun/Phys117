# Import modules
import numpy as np
from tqdm import tqdm
import pandas as pd
import os


def remover(list, to_be_removed):
    list = [element for element in list if element != to_be_removed and type(element) == type(to_be_removed)]
    return list


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


def data(folder, stuffs, folder_name):
    folder_data = []
    for file in folder:
        file_data = []
        for stuff_data in file:
            stuff_name = os.path.split(stuff_data)[1]
            if stuff_name[:-len(".csv")] in stuffs:
                data = pd.read_csv(stuff_data)
                event_num = data["event#"]
                phi = data["phi"]
                pt = data["PT"] + 3.142
                particle_name = [stuff_name[:-len(".csv")] for i in range(len(event_num))]
                dataset = [folder_name for i in range(len(event_num))]
                data_tuple_list = list(zip(dataset, event_num, particle_name, phi, pt))
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

# Import functions
from Afiles import files
individual = True
data_path = "C:/Users/mhals/Dropbox/PC (2)/Documents/GitHub/Phys117/Data/Pandas/Individual/"
folders = ["BH", "Sphaleron"]
stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
file_amounts = [18, 3]
folder_list, filename_list = files(individual, data_path, folders, stuffs, file_amounts)


train_to_total = 0.8
train_amounts = [int(amount) for amount in np.round(train_to_total * np.array(file_amounts))]

train_list, train_names = [], []
test_list, test_names = [], []
for index, folder, file_names in zip([i for i in range(len(folders))], folder_list, filename_list):
    train_list.append(folder[:train_amounts[index] + 1])
    train_names.append(file_names[:train_amounts[index] + 1])
    test_list.append(folder[train_amounts[index] + 1:])
    test_names.append(file_names[train_amounts[index] + 1:])
    

dataset_index = 0
event_num_index = 1
particle_name_index = 2
phi_index = 3
pt_index = 4


train_data = []
for folder, folder_name in zip(train_list, folders):
    folder_data = unpacker(data(folder, stuffs, folder_name), [])
    train_data.append(folder_data)

test_data = []
for folder, folder_name in zip(test_list, folders):
    folder_data = unpacker(data(folder, stuffs, folder_name), [])
    test_data.append(folder_data)


train_ptmax = [[] for folder in folders]
train_stuff_amount = [[] for folder in folders]
train_MET = [[] for folder in folders]
for folder_index, folder_events in enumerate(train_data):
    for event in folder_events:
        ptmax = sorted(event, key = lambda x: x[pt_index])[-1][1]
        train_ptmax[folder_index].append(ptmax)
        train_stuff_amount[folder_index].append(len(event) - 1)
        met = [particle for particle in event if particle[particle_name_index] == "MET"][0][pt_index]
        train_MET[folder_index].append(met)


eff_tupes = []
eff_ptmax = efficiency_value(train_ptmax, binsize = 1)
eff_tupes.append(eff_ptmax)
eff_stuff_amount = efficiency_value(train_stuff_amount, binsize = 0.5)
eff_tupes.append(eff_stuff_amount)
eff_MET = efficiency_value(train_MET, binsize = 1)
eff_tupes.append(eff_MET)
print(eff_tupes)


dataset = []
test_ptmax = []
test_stuff_amount = []
test_MET = []
for folder_index, folder_events in enumerate(test_data):
    for event in folder_events:
        dataset.append(folders[folder_index])
        ptmax = sorted(event, key = lambda x: x[pt_index])[-1][pt_index]
        test_ptmax.append(ptmax)
        test_stuff_amount.append(len(event) - 1)
        met = [particle for particle in event if particle[particle_name_index] == "MET"][0][pt_index]
        test_MET.append(met)


correct = 0
indeterminate = 0
total = 0
for event_index in range(len(list(zip(dataset, test_ptmax, test_stuff_amount, test_MET)))):
    bh_or_sphal = []

    folder = dataset[event_index]
    ptmax = test_ptmax[event_index]
    stuff_amount = test_stuff_amount[event_index]
    met = test_MET[event_index]

    to_test = [ptmax, stuff_amount, met]
    for eff_index, eff_tupe in enumerate(eff_tupes):
        test_val = to_test[eff_index]
        sep_val = eff_tupe[0]
        sep_rel = eff_tupe[2]
        if test_val < sep_val:
            if sep_rel == "BH < Sphal":
                bh_or_sphal.append(True) if folder == "BH" else bh_or_sphal.append(False)
            else:
                bh_or_sphal.append(True) if folder == "Sphaleron" else bh_or_sphal.append(False)
        else:
            if sep_rel == "BH > Sphal":
                bh_or_sphal.append(True) if folder == "BH" else bh_or_sphal.append(False)
            else:
                bh_or_sphal.append(True) if folder == "Sphaleron" else bh_or_sphal.append(False)


    if float(bh_or_sphal.count(True)) > len(bh_or_sphal) / 2:
        correct += 1
    elif float(bh_or_sphal.count(True)) == len(bh_or_sphal) / 2:
       indeterminate += 1
    total += 1


accuracy = np.round((correct / total) * 100, 2)
print(f"{'correct':10} : ", correct)
print(f"{'undetermined':10} : ", indeterminate)
print(f"{'total':10} : ", total)
print(f"{'accuracy':10} : ", accuracy, "%")