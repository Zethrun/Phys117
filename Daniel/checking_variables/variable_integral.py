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

path_list_sep = ([background_path_sep, blackhole_path_sep, sphaleron_path_sep, test_path_sep], "sep")
path_list_sum = ([background_path_sum, blackhole_path_sum, sphaleron_path_sum, test_path_sum], "sum")


each_file = True
particle_list = ["electron", "jet", "MET", "muon", "photon", "tau"] # max 9
particle_values = ["event", "eta", "phi", "PT", "jmass", "ntrk", "btag", "hadem"]
path_names = ["Background", "BH", "Sphaleron", "Test"]

plot_list = ["electron", "PT", "MET"]

### For sep, the format is org_dict["FOLDER_TYPE"] [file indexed byinteger] ["particle"]
### For ex. org_dict["sphaleron"][0][1] == "Data/Pandas/individual/Sphaleron/PP13-Sphaleron-THR9-FRZ15-NB33-60-NSUBP50/jet.csv"
### the particle indexs are integers corresponding to the order in Particle_list

### for sum, ..

def org_file_folder(path_list_tuple):
    path_list = path_list_tuple[0]
    org_dict = {
        "background" : [],
        "BH" : [],
        "sphaleron" : [],
        "test" : []
    }

    if path_list_tuple[1] == "sep":
        for index, path in enumerate(path_list):
            path_file_list = [path + "/" + files for files in os.listdir(path)]
            for file in path_file_list:
                path_particle_list = [file + "/" + particle_file for particle_file in os.listdir(file)]
                org_dict[path_names[index]].append(path_particle_list)

        return org_dict
    
    elif path_list_tuple[1] == "sum":
        for index, path in enumerate(path_list):
            file_list = [path + "/" + file for file in os.listdir(path)]
            for file in os.listdir(path):
                org_dict[path_names[index]].append(path + "/" + file)

        return org_dict
    else:
        print("Have to sepcify sep or sum..")

#print(org_file_folder(path_list_sep))

def plot_file(data_dict, type1, type2, variable):
    data_files_1 = data_dict[type1]
    data_files_2 = data_dict[type2]

    plt.hist()