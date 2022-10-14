# Import modules
from tqdm import tqdm

# Import functions
from Afiles import files
data_path = "C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/Pandas/Individual/"

# Data variables
individual = True
folders = ["BH", "Sphaleron"]
stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
bool_list = [True, False]


MET_dist = bool_list[1]
if MET_dist:
    file_amounts = [1, 1]
    stuffs = ["MET"]
    
    folder_list, filename_list = files(individual, data_path, folders, stuffs, file_amounts)


    from Bdata import MET_data

    (data_variable, combine_files) = ("PT", False)

    folders_data = []
    for folder_index, folder in tqdm(enumerate(folder_list)):
        plot_data = MET_data(folder, stuffs, data_variable, combine_files)
        folders_data.append(plot_data)


    from Cplotter import MET_dist
    
    (binsize, filter_strengths, xlabel, compare) = (25, [10, 3], "MET [GeV]", True)

    MET_dist(folders_data, folders, filename_list, stuffs, binsize, filter_strengths, xlabel, compare, combine_files)
        

HT_dist = bool_list[1]
if HT_dist:
    file_amounts = [1, 1]
    stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
    
    folder_list, filename_list = files(individual, data_path, folders, stuffs, file_amounts)


    from Bdata import HT_data

    (data_variable, combine_files) = ("PT", False)

    folders_data = []
    for folder_index, folder in tqdm(enumerate(folder_list)):
        plot_data = HT_data(folder, stuffs, data_variable, combine_files)
        folders_data.append(plot_data)


    from Cplotter import HT_dist
    
    (binsize, filter_strengths, xlabel, compare) = (100, [10, 3], "HT [GeV]", True)

    HT_dist(folders_data, folders, filename_list, stuffs, binsize, filter_strengths, xlabel, compare, combine_files)


stuff_amount = bool_list[1]
if stuff_amount:
    file_amounts = [1, 1]
    stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
    
    folder_list, filename_list = files(individual, data_path, folders, stuffs, file_amounts)


    from Bdata import stuff_amount_data

    (data_variable, combine_files) = ("PT", False)

    folders_data = []
    for folder_index, folder in tqdm(enumerate(folder_list)):
        plot_data = stuff_amount_data(folder, stuffs, data_variable, combine_files)
        folders_data.append(plot_data)


    from Cplotter import stuff_amount_plot
    
    (binsize, filter_strengths, xlabel, compare) = (0.5, [10, 0], "Particle Amount", True)

    stuff_amount_plot(folders_data, folders, filename_list, stuffs, binsize, filter_strengths, xlabel, compare, combine_files)


stuff_count = bool_list[1]
if stuff_count:
    file_amounts = [1, 1]
    stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
    
    folder_list, filename_list = files(individual, data_path, folders, stuffs, file_amounts)


    from Bdata import stuff_counts_data

    (data_variable, combine_files) = ("PT", False)

    folders_data = []
    for folder_index, folder in tqdm(enumerate(folder_list)):
        plot_data = stuff_counts_data(folder, stuffs, data_variable, combine_files)
        folders_data.append(plot_data)


    from Cplotter import stuff_counts_plot
    
    (binsize, filter_strengths, xlabel, compare) = (0.5, [10, 0], "Particle Amount", True)

    stuff_counts_plot(folders_data, folders, filename_list, stuffs, binsize, filter_strengths, xlabel, compare, combine_files)


PT_max = bool_list[0]
if PT_max:
    file_amounts = [18, 3]
    stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
    
    folder_list, filename_list = files(individual, data_path, folders, stuffs, file_amounts)


    from Bdata import PT_max_data

    (data_variable, combine_files, by_particle) = ("PT", True, False)

    folders_data = []
    for folder_index, folder in tqdm(enumerate(folder_list)):
        plot_data = PT_max_data(folder, stuffs, by_particle, data_variable, combine_files)
        folders_data.append(plot_data)


    from Cplotter import PT_max_plot
    
    (binsize, filter_strengths, xlabel, compare) = (100, [10, -10], "PT [GeV]", True)

    PT_max_plot(folders_data, folders, filename_list, stuffs, by_particle, binsize, filter_strengths, xlabel, compare, combine_files)


Phi_between_angles = bool_list[1]
if Phi_between_angles:
    file_amounts = [18, 3]
    stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
    
    folder_list, filename_list = files(individual, data_path, folders, stuffs, file_amounts)


    from Bdata import Phi_between_angles_data

    (data_variable, combine_files) = ("PT", True)

    folders_data = []
    for folder_index, folder in tqdm(enumerate(folder_list)):
        plot_data = Phi_between_angles_data(folder, stuffs, data_variable, combine_files)
        folders_data.append(plot_data)


    from Cplotter import Phi_between_angles_plot
    
    (binsize, filter_strengths, xlabel, compare) = (1, [10, 0], "Particle Amount", True)

    Phi_between_angles_plot(folders_data, folders, filename_list, stuffs, binsize, filter_strengths, xlabel, compare, combine_files)


efficiency_variables = {
    "stuff per event (84.8%)": [10, "stuff_amount_data", "stuff_amount_plot"],
    "max PT per event (84.1%)": [1600, "PT_max_data", "PT_max_plot"]
    }