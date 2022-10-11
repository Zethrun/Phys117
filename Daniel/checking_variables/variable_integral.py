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
import random

folder_path = "Data/Pandas/Individual/" ###

### Paths ###
background_path_sep = "Data/Pandas/individual/Background"
blackhole_path_sep = "Data/Pandas/individual/BH"
sphaleron_path_sep = "Data/Pandas/individual/Sphaleron"
test_path_sep = "Data/Pandas/individual/Test"

background_path_sum = "Data/Pandas/Sum/Background"
blackhole_path_sum = "Data/Pandas/Sum/BH"
sphaleron_path_sum = "Data/Pandas/Sum/Sphaleron"
test_path_sum = "Data/Pandas/Sum/Test"


###
path_list_sep = ([background_path_sep, blackhole_path_sep, sphaleron_path_sep, test_path_sep], "sep")
path_list_sum = ([background_path_sum, blackhole_path_sum, sphaleron_path_sum, test_path_sum], "sum")
###


particle_list = ["electron", "jet", "MET", "muon", "photon", "tau"] 
particle_values = ["event", "eta", "phi", "PT", "jmass", "ntrk", "btag", "hadem"]
path_names = ["background", "BH", "sphaleron", "test"]


particles = ["electron", "PT"]


### For sep, the format is org_dict["FOLDER_TYPE"] [file indexed byinteger] ["particle"]
### For ex. org_dict["sphaleron"][0][1] == "Data/Pandas/individual/Sphaleron/PP13-Sphaleron-THR9-FRZ15-NB33-60-NSUBP50/jet.csv"
### the particle indexs are integers corresponding to the order in Particle_list

### for sum, ..

def org_files_folder(path_list_tuple):
    path_list = path_list_tuple[0]
    org_dict = {
        "background" : [[],[]],
        "BH" : [[],[]],
        "sphaleron" : [[],[]],
        "test" : [[],[]]
    }

    if path_list_tuple[1] == "sep":
        for index, path in enumerate(path_list):
            path_file_list = [path + "/" + files for files in os.listdir(path)]
            file_names = [file for file in os.listdir(path)]
            org_dict[path_names[index]][1] = file_names
            
            for file in path_file_list:
                path_particle_list = [file + "/" + particle_file for particle_file in os.listdir(file)]
                org_dict[path_names[index]][0].append(path_particle_list)

        return org_dict
    
    elif path_list_tuple[1] == "sum":
        for index, path in enumerate(path_list):
            file_list = [path + "/" + file for file in os.listdir(path)]
            for file in os.listdir(path):
                org_dict[path_names[index]][0].append(path + "/" + file)
                org_dict[path_names[index]][1].append(file)

        return org_dict
    else:
        print("Have to sepcify sep or sum..")



#print(org_files_folder(path_list_sep)["BH"][1].index('BH_n5_M11'))

#only works for sep

def find_files_for_analysis(org_files_folder, plot_comparison, picking_file_order, random_pick = False, multiple_amount_tuple = None):
    #pick_file_order is a list if not single
    pick_file_order_multiple = picking_file_order
        
    files_1 = org_files_folder[plot_comparison[0]][0]
    files_2 = org_files_folder[plot_comparison[1]][0]
    amount_1, amount_2 = len(files_1), len(files_2)
    picks_file_1 = pick_file_order_multiple[0]
    picks_file_2 = pick_file_order_multiple[1]
    
    if random_pick:
        #willpick same amount as specified
        if pick_file_order_multiple != None and multiple_amount_tuple == None:
            len_picks_1 = len(picks_file_1)
            len_picks_2 = len(picks_file_2)
        elif multiple_amount_tuple != None: # if we dont specify what files
            len_picks_1 = multiple_amount_tuple[0]
            len_picks_2 = multiple_amount_tuple[1]
        picks_1 = [random.randint(0, amount_1-1) for i in range(len_picks_1)]
        picks_2 = [random.randint(0, amount_2-1) for i in range(len_picks_2)]
        picks_1_names = [org_files_folder[plot_comparison[0]][1][index] for index in picks_1]
        picks_2_names = [org_files_folder[plot_comparison[1]][1][index] for index in picks_2]
    
    else:
        picks_1 = []
        picks_2 = []
        picks_1_names = []
        picks_2_names = []
        
        for picked_file in picks_file_1:
            pick_1 = org_files_folder[plot_comparison[0]][1].index(picked_file)
            picks_1_names.append(picked_file)
            picks_1.append(pick_1) 
                        
        for picked_file in picks_file_2:
            pick_2 = org_files_folder[plot_comparison[1]][1].index(picked_file)
            picks_2_names.append(picked_file)
            picks_2.append(pick_2)
    
    picked_files_1 = [files_1[i] for i in picks_1]
    picked_files_2 = [files_2[i] for i in picks_2]
    files_1_path = [file[0].removesuffix("/electron.csv") for file in picked_files_1]
    files_2_path = [file[0].removesuffix("/electron.csv") for file in picked_files_2]
    return picked_files_1, picked_files_2, files_1_path, files_2_path, picks_1_names, picks_2_names





def HT_dist(org_files_folder, plot_comparison, picking_file_order, random_pick = False, multiple_amount_tuple = None):
    
    picked_files_1, picked_files_2, files_1_path, files_2_path, picks_1_names, picks_2_names = find_files_for_analysis(org_files_folder, plot_comparison, picking_file_order, random_pick, multiple_amount_tuple)
    amount_files_1 = len(picked_files_1)
    amount_files_2 = len(picked_files_2)
    HT_lists = [[[] for i in range(amount_files_1)],[[] for i in range(amount_files_2)]]
    files_list = [[(picked_files_1[i], files_1_path[i]) for i in range(amount_files_1)], [(picked_files_2[i], files_2_path[i]) for i in range(amount_files_2)]]
    
    
    for type_index, files_of_type in enumerate(files_list):
        for i, file_i in enumerate(files_of_type):
            nr_events = len(pd.read_csv(file_i[1] + "/MET.csv")["event#"])
            
            event_dict = dict.fromkeys(range(nr_events))
            for event in event_dict:
                event_dict[event] = 0
            
            for particle_file in file_i[0]:
                if particle_file == file_i[1] + "/MET.csv":
                    pass
                else:
                    file_csv = pd.read_csv(particle_file)
                    for index, row in file_csv.iterrows():
                        event_nr = row["event#"]
                        PT = row["PT"]
                        event_dict[event_nr] += PT
            
            for event in range(nr_events):
                HT_lists[type_index][i].append(event_dict[event])
            
    return [[HT_lists[0], [plot_comparison[0], picking_file_order[0]]], [HT_lists[1], [plot_comparison[1], picking_file_order[1]]]], "HT[Gev]"

'1w'



def largest_pt(org_files_folder, plot_comparison, picking_file_order, random_pick = False, multiple_amount_tuple = None):
    pass





def MET_dist(org_files_folder, plot_comparison, picking_file_order, multiple = True, random_pick = False, multiple_amount_tuple = None):
    
    picked_files_1, picked_files_2, files_1_path, files_2_path, picks_1_names, picks_2_names = find_files_for_analysis(org_files_folder, plot_comparison, picking_file_order, random_pick, multiple_amount_tuple)
    amount_files_1 = len(picked_files_1)
    amount_files_2 = len(picked_files_2)
    MET_lists = [[[] for i in range(amount_files_1)],[[] for i in range(amount_files_2)]]
    files_list = [[(picked_files_1[i], files_1_path[i]) for i in range(amount_files_1)], [(picked_files_2[i], files_2_path[i]) for i in range(amount_files_2)]]
    
    
    for type_index, files_of_type in enumerate(files_list):
        for i, file_i in enumerate(files_of_type):
            nr_events = len(pd.read_csv(file_i[1] + "/MET.csv")["event#"])
            
            event_dict = dict.fromkeys(range(nr_events))
            for event in event_dict:
                event_dict[event] = 0
            
            for particle_file in file_i[0]:
                if not particle_file == file_i[1] + "/MET.csv":
                    pass
                else:
                    file_csv = pd.read_csv(particle_file)
                    for index, row in file_csv.iterrows():
                        event_nr = row["event#"]
                        MET = row["PT"]
                        event_dict[event_nr] += MET
            
            for event in range(nr_events):
                MET_lists[type_index][i].append(event_dict[event])
            
    return [[MET_lists[0], [plot_comparison[0], picking_file_order[0]]], [MET_lists[1]], [plot_comparison[1], picking_file_order[1]]], "MET[Gev]"





def object_dist():
    pass



def calculate_bin(data, binsize): # must be data[0] inserted to the function
    max_list = []
    for type_data in data:
        amount = len(type_data[0])
        max_list += [max(type_data[0][i]) for i in range(amount)]
    b_value = max(max_list)
    a_value = 0
    b_value_n = a_value + round((b_value - a_value)/binsize)*binsize
    return np.linspace(a_value, b_value_n, num=(int((b_value_n-a_value)/binsize) + 1))





def calculate_efficiency(data):
    data = data[0]
    bin_ls = calculate_bin(data, binsize)
    dx = bin_ls[2] - bin_ls[1]
    data_filelist = {}
    file_names = []
    efficiency_list = [] # first index is list of the file_names
    check = len(data[0][0])
    if check > 2:
        print("This only works with a pair of data_file")
        return None
    else:
        for type_data in data:
            file_names.append(type_data[1][0])
            for type_data_file in type_data[0]:
                data_filelist[type_data[1][0]] = type_data_file
        
        count_1, bins_1 = np.histogram(data_filelist[file_names[0]])
        count_2, bins_2 = np.histogram(data_filelist[file_names[1]])
        
        for k_index, k in enumerate(bin_ls[:-1]):
            #1_file left
            area_f_1_l = 0
            area_f_2_l = 0
                        
            for index, i in enumerate(bin_ls[:-1]):
                try:
                    if i < k_index:
                        area_f_1_l += count_1[index]*dx
                    elif i >= k_index:
                        area_f_2_l += count_2[index]*dx
                except:
                    pass
            
            area_l_total = area_f_1_l + area_f_2_l
            e_1_l = area_f_1_l / area_l_total
            e_2_l = area_f_2_l / area_l_total
            
            #1_file right
            area_f_1_r = 0
            area_f_2_r = 0
            
            for index, i in enumerate(bin_ls[:-1]):
                try:
                    if i < k_index:
                        area_f_1_r += count_1[index]*dx
                    elif i >= k_index:
                        area_f_2_r += count_2[index]*dx
                except:
                    pass
                    
            area_r_total = area_f_1_r + area_f_2_r
            e_1_r = area_f_1_r / area_r_total
            e_2_r = area_f_2_r / area_r_total)
            
            if (e_1_l + e_2_l) < (e_1_r + e_2_r):
                efficiency_list.append([e_1_l, e_2_l])
            elif  (e_1_l + e_2_l) > (e_1_r + e_2_r):
                efficiency_list.append([e_1_r, e_2_r])
            else:
                efficiency_list.append([e_1_l, e_2_l])
    
        return efficiency_list





def plot(data, plt_hist=False, seperate_plot = False, efficiency = False):
    label = data[1]
    data = data[0]
    
    histtype = "bar"
    fig = plt.figure()
    style = "seaborn-darkgrid"
    plt.style.use(style)
    plt.legend("")
    bin_ls = calculate_bin(data, binsize)
    
    if not plt_hist:
        for type_data in data:
            for type_data_file in type_data[0]:
                counts, bins = np.histogram(type_data_file,bin_ls)
                bin_ls = bin_ls[:-1]
                norm_fact = 1/(sum(counts))
                counts = norm_fact * np.array(counts)
                
                plt.plot(bin_ls,counts)
    
    else:
        for type_data in data:
            plt.hist(type_data[0], bins=bin_ls, alpha = alpha)
    
    plt.show()
    
    if efficiency:
        pass



#plot variables:
rwidth = 1
binsize = 80
alpha = 0.8

#files
plot_comparison = ["BH", "sphaleron"]
picking_file_order = [["BH_n4_M8"], ["PP13-Sphaleron-THR9-FRZ15-NB33-60-NSUBP50"]]

data = HT_dist(org_files_folder(path_list_sep), plot_comparison, picking_file_order, random_pick = False, multiple_amount_tuple=(3,1))
print(calculate_efficiency(data))
plot(data)
print(2)