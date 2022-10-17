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
background_path_sep = "Data/Pandas/individual/background"
blackhole_path_sep = "Data/Pandas/individual/BH"
sphaleron_path_sep = "Data/Pandas/individual/sphaleron"
test_path_sep = "Data/Pandas/individual/test"

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
    folder_path = "Data/Pandas/individual/"
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
    files_1_path_new = [folder_path + plot_comparison[0] + "/" + file for file in picks_file_1]
    files_2_path_new = [folder_path + plot_comparison[1] + "/" + file for file in picks_file_2]
    return picked_files_1, picked_files_2, files_1_path_new, files_2_path_new, picks_1_names, picks_2_names





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





def calculate_efficiency(data, return_list = False, return_sep = False, for_itterate = False):
    data = data[0]
    efficiencies_list = []
    efficiencies_list_sep = []
    bin_ls = calculate_bin(data, binsize)
    dx = bin_ls[2] - bin_ls[1]
    data_filelist = [{}, {}]
    file_names = [[], []]
    
    check = len(data[0][0] - len(data[1][0]))
    if check != 0:
        print("This only works with pairs of data_file")
        return None
    else:
        for index, type_data in enumerate(data):
            file_names[index] = type_data[1][1]
            for index_2, type_data_file in enumerate(type_data[0]):
                data_filelist[index][file_names[index][index_2]] = type_data_file
        
        for round in range(len(data[0][0])):
            efficiency_list = [] # first index is list of the file_names
            efficiency_list_sep = []
            
            count_1, bins_1 = np.histogram(data_filelist[file_names[0]],bin_ls)
            count_2, bins_2 = np.histogram(data_filelist[file_names[1]],bin_ls)
            norm_fact_1 = 1/(sum(count_1))
            norm_fact_2 = 1/(sum(count_2))
            count_1 = norm_fact_1 * np.array(count_1)
            count_2 = norm_fact_2 * np.array(count_2)


            for k_index, k in enumerate(bin_ls[1:-1]):
                A_total = np.sum(count_1) + np.sum(count_2)   
                A_1_left = np.sum(count_1[:k_index])
                A_1_right = np.sum(count_1[k_index:-1])
                A_2_left = np.sum(count_2[:k_index])
                A_2_right = np.sum(count_2[k_index:-1])
                
                #file1 left, file2 right, alfa:
                e_1_alfa, e_2_alfa = A_1_left/A_total, A_2_right/A_total
                e_T_alfa = e_1_alfa + e_2_alfa
                
                #file1 right, file left, beta:
                e_1_beta, e_2_beta = A_1_right/A_total, A_2_left/A_total
                e_T_beta = e_1_beta + e_2_beta
                    
                if e_T_alfa >= e_T_beta:
                    efficiency_list.append(e_T_alfa)
                    efficiency_list_sep.append([e_1_alfa, e_2_alfa])
                elif e_T_alfa < e_T_beta:
                    efficiency_list.append(e_T_beta)
                    efficiency_list_sep.append([e_1_beta, e_2_beta])
                
        if return_list == True:
            if return_sep == True:
                return efficiency_list_sep
            else:
                return efficiency_list
        else:
            max_efficiency = np.max(efficiency_list)
        return max_efficiency

def itterate_efficiency(data):
    data = data[0]
    data_filelist = [data[0][0][0],[data[0][1][0]]]
    data_filelist_T = list(zip(*data_filelist))
    


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
                #norm_fact = 1/(sum(counts) * binsize)
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
picking_file_order = [["BH_n4_M8", "BH_n4_M10"], ["PP13-Sphaleron-THR9-FRZ15-NB33-60-NSUBP50"]]

data = HT_dist(org_files_folder(path_list_sep), plot_comparison, picking_file_order, random_pick = False, multiple_amount_tuple=(3,1))
#print(calculate_efficiency(data))
plot(data)
print(2)