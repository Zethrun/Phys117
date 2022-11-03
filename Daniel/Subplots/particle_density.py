import matplotlib.pyplot as plt
import math
import numpy as np
from LHCO_reader import LHCO_reader
import pandas as pd
import os

sep_background_path = "Data/Pandas/individual/Background"
sep_blackhole_path = "Data/Pandas/individual/BH"
sep_sphaleron_path = "Data/Pandas/individual/Sphaleron"
sep_test_path = "Data/Pandas/individual/Test"

sum_background_path = "Data/Pandas/Sum/Background"
sum_blackhole_path = "Data/Pandas/Sum/BH"
sum_sphaleron_path = "Data/Pandas/Sum/Sphaleron"
sum_test_path = "Data/Pandas/Sum/Test"

sep_path_list = [sep_background_path, sep_blackhole_path, sep_sphaleron_path, sep_test_path]
sum_path_list = [sum_background_path, sum_blackhole_path, sum_sphaleron_path, sum_test_path]


each_file = True
hist_plots = ["electron", "tau", "muon", "muon", "muon"] # max 9
plot_values = ["event", "eta", "phi", "PT", "jmass", "ntrk", "btag", "hadem"]
path_names = ["Background", "BH", "Sphaleron", "Test"]



def org_file_folder(path_list):
    org_dict = {
        "Background" : [],
        "BH" : [],
        "Sphaleron" : [],
        "Test" : []
    }

    for index, path in enumerate(path_list):
        path_file_list = [path + "/" + files for files in os.listdir(path)]
        for file in path_file_list:
            path_particle_list = [file + "/" + particle_file for particle_file in os.listdir(file)]
            org_dict[path_names[index]].append([path_particle_list])

    return org_dict



def plot():
    if each_file:
        pass

print(org_file_folder(sep_path_list)["BH"][0])