# Import modules
import numpy as np
from tqdm import tqdm

# Import functions
from Afiles import files
data_path = "C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/Pandas/Test/"
individual = True
folders = ["BH", "Sphaleron"]
stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
file_amounts = [18, 3]

from Afiles import files
folder_list, filename_list = files(individual, data_path, folders, stuffs, file_amounts)


efficiency_variables = {
    0: [10, "stuff per event (84.8%)"],
    1: [1600, "max PT per event (84.1%)"]
    }


from Cplotter import data_binner

def sphal_or_bh(folder_data, binsize, efficiency_line):
    x, y = data_binner(folder_data, binsize, plot = False)
    bin = efficiency_line
    right = np.sum(y[bin + 1:])
    
    if right >= 0.5:
        is_sphal = True
    else:
        is_sphal = False
        
    return is_sphal


folder_dataset_categories = []
for folder_index, folder in tqdm(enumerate(folder_list)):
    
    efficiency_variable = efficiency_variables[0]
    efficiency_line = efficiency_variable[0]
    
    from Bdata import stuff_amount_data as data_func
    (data_variable, combine_files, binsize) = ("PT", True, 1)
    datasets = data_func(folder, stuffs, data_variable, combine_files)
    dataset_categories = [[] for dataset in datasets]

    
    for dataset_index, dataset in enumerate(datasets):
        print(dataset)
        is_sphal = sphal_or_bh(dataset, binsize, efficiency_line)
        dataset_categories[dataset_index].append(is_sphal)
    
    
    efficiency_variable = efficiency_variables[1]
    efficiency_line = efficiency_variable[0]
    
    from Bdata import PT_max_data as data_func
    (data_variable, combine_files, by_particle, binsize) = ("PT", True, False, 1)
    datasets = data_func(folder, stuffs, by_particle, data_variable, combine_files)
    dataset_categories = [[] for dataset in datasets]

    for dataset_index, dataset in enumerate(datasets):
        is_sphal = sphal_or_bh(dataset, binsize, efficiency_line)
        dataset_categories[dataset_index].append(is_sphal)
        
    folder_dataset_categories.append(dataset_categories)

for index, dataset_categories in enumerate(folder_dataset_categories):
    for dataset in dataset_categories:
        if dataset.count(True) >= 0.5 * len(dataset) and index == 0:
            print("correct")
        elif index == 0:
            print("incorrect")
        else:
            print("correct")


