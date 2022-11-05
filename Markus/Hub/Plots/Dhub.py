# Import modules
from tqdm import tqdm

# Import functions
from FilesFunc import files

# Data variables
data_path = "C:/Users/mhals/Dropbox/PC (2)/Documents/GitHub/Phys117/Data/Pandas/Individual/"
individual = True
folders = ["BH", "Sphaleron"]
stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
bool_list = [True, False]
file_amounts = [1, 1]


MET_dist = bool_list[1]
if MET_dist:
    file_amounts = [18, 3]
    stuffs = ["MET"]
    
    folder_list, filename_list = files(individual, data_path, folders, stuffs, file_amounts)
    for sphal_index, sphal_file in enumerate(folder_list[1]):
        for bh_index, bh_file in enumerate(folder_list[0]):
            data_folder_list = [[bh_file], [sphal_file]]
            name_list = [[filename_list[0][bh_index]], [filename_list[1][sphal_index]]]

            from Bdata import MET_data

            (data_variable, combine_files) = ("PT", False)

            folders_data = []
            for folder_index, folder in tqdm(enumerate(data_folder_list)):
                plot_data = MET_data(folder, stuffs, data_variable, combine_files)
                folders_data.append(plot_data)
            
            efficiencies_plot = True


            from Cplotter import MET_dist
            
            (binsize, filter_strength, xlabel) = (1, 0.95, "MET [GeV]")

            MET_dist(folders_data, folders, filename_list, stuffs, binsize, filter_strength, xlabel, combine_files, efficiencies_plot)
        

HT_dist = bool_list[1]
if HT_dist:
    stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
    
    folder_list, filename_list = files(individual, data_path, folders, stuffs, file_amounts)


    from Bdata import HT_data

    (data_variable, combine_files) = ("PT", False)

    folders_data = []
    for folder_index, folder in tqdm(enumerate(folder_list)):
        plot_data = HT_data(folder, stuffs, data_variable, combine_files)
        folders_data.append(plot_data)
    
    efficiencies_plot = True


    from Cplotter import HT_dist_plot
    
    (binsize, filter_strength, xlabel) = (25, 1, "HT [GeV]")

    HT_dist_plot(folders_data, folders, filename_list, stuffs, binsize, filter_strength, xlabel, combine_files, efficiencies_plot)


stuff_amount = bool_list[1]
if stuff_amount:
    stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
    
    folder_list, filename_list = files(individual, data_path, folders, stuffs, file_amounts)


    from Bdata import stuff_amount_data

    (data_variable, combine_files) = ("PT", False)

    folders_data = []
    for folder_index, folder in tqdm(enumerate(folder_list)):
        plot_data = stuff_amount_data(folder, stuffs, data_variable, combine_files)
        folders_data.append(plot_data)
    
    efficiencies_plot = True


    from Cplotter import stuff_amount_plot
    
    (binsize, filter_strength, xlabel) = (0.5, 1, "Particle Amount")

    stuff_amount_plot(folders_data, folders, filename_list, stuffs, binsize, filter_strength, xlabel, combine_files, efficiencies_plot)


stuff_count = bool_list[1]
if stuff_count:
    stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
    
    folder_list, filename_list = files(individual, data_path, folders, stuffs, file_amounts)


    from Bdata import stuff_counts_data

    (data_variable, combine_files) = ("PT", False)

    folders_data = []
    for folder_index, folder in tqdm(enumerate(folder_list)):
        plot_data = stuff_counts_data(folder, stuffs, data_variable, combine_files)
        folders_data.append(plot_data)
    
    efficiencies_plot = True


    from Cplotter import stuff_counts_plot
    
    (binsize, filter_strength, xlabel) = (0.5, 1, "Particle Amount")

    stuff_counts_plot(folders_data, folders, filename_list, stuffs, binsize, filter_strength, xlabel, combine_files, efficiencies_plot)


PT_max = bool_list[1]
if PT_max:
    file_amounts = [18, 3]
    stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
    
    folder_list, filename_list = files(individual, data_path, folders, stuffs, file_amounts)

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
            
            efficiencies_plot = True


            from Cplotter import PT_max_plot
            
            (binsize, filter_strength, xlabel) = (1, 0.975, "PT [GeV]")

            PT_max_plot(folders_data, folders, name_list, stuffs, by_particle, binsize, filter_strength, xlabel, combine_files, efficiencies_plot)
    
    
Phis = bool_list[1]
if Phis:
    file_amounts = [1, 1]
    stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
    
    folder_list, filename_list = files(individual, data_path, folders, stuffs, file_amounts)


    from Bdata import phi_data

    (data_variable, combine_files, by_particle) = ("phi", False, True)

    folders_data = []
    for folder_index, folder in tqdm(enumerate(folder_list)):
        plot_data = phi_data(folder, stuffs, by_particle, data_variable, combine_files)
        folders_data.append(plot_data)
    
    efficiencies_plot = True


    from Cplotter import phi_plot
    
    (binsize, filter_strength, xlabel) = (0.01, 1, "phi [radians]")

    phi_plot(folders_data, folders, filename_list, stuffs, binsize, filter_strength, xlabel, combine_files, efficiencies_plot)


Phi_between_angles = bool_list[0]
if Phi_between_angles:
    file_amounts = [1, 1]
    stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
    
    folder_list, filename_list = files(individual, data_path, folders, stuffs, file_amounts)


    from Bdata import phi_diff_data

    (data_variable, combine_files, by_particle) = ("phi", False, True)

    folders_data = []
    for folder_index, folder in tqdm(enumerate(folder_list)):
        plot_data = phi_diff_data(folder, stuffs, by_particle, data_variable, combine_files)
        folders_data.append(plot_data)
    
    efficiencies_plot = True


    from Cplotter import phi_diff_plot
    
    (binsize, filter_strength, xlabel) = (0.01, 1, "phi [radians]")

    phi_diff_plot(folders_data, folders, filename_list, stuffs, binsize, filter_strength, xlabel, combine_files, efficiencies_plot)


efficiency_variables = {
    "stuff per event (84.8%)": [10, "stuff_amount_data", "stuff_amount_plot"],
    "max PT per event (84.1%)": [1600, "PT_max_data", "PT_max_plot"]
    }