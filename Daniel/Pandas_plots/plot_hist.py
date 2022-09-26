import matplotlib.pyplot as plt
import math
import numpy as np
from LHCO_reader import LHCO_reader
import pandas as pd
import os

sep_background_path = "Daniel/data/data_pandas/gathered_seperated/background"
sep_blackhole_path = "Daniel/data/data_pandas/gathered_seperated/BH"
sep_sphaleron_path = "Daniel/data/data_pandas/gathered_seperated/sphaleron"

norm_background_path = "Daniel/data/data_pandas/normal/background"
norm_blackhole_path = "Daniel/data/data_pandas/normal/BH"
norm_sphaleron_path = "Daniel/data/data_pandas/normal/sphaleron"



### MET freuency ###

hist_plots = ["electron", "tau", "muon", "muon", "muon"] # max 9
plot_values = ["event", "eta", "phi", "PT", "jmass", "ntrk", "btag", "hadem"]


def hist_data(axs, a, b, data, binwidth, rwidth, max_factor, s = 3):
    if s == 3:
        axs[a,b].hist(data, rwidth = rwidth, bins=range(int(min(data)), int(max_factor * max(data)) + binwidth, binwidth), density = True)
    elif s == 1:
        axs.hist(data, rwidth = rwidth, bins=range(int(min(data)), int(max_factor * max(data)) + binwidth, binwidth), density = True)
    elif s == 2:
        axs[a].hist(data, rwidth = rwidth, bins=range(int(min(data)), int(max_factor * max(data)) + binwidth, binwidth), density = True)


def hist_particles_data(data_folder,hist_list):
    l = len(hist_plots)
    binwidth = 30
    rwidth = 1
    max_factor = 1/2
    data_files = [data_folder + "/" + data_file + ".csv" for data_file in hist_plots]

    typ = plot_values[3] 

    if l <= 3:
        fig, axs = plt.subplots(l)
        for i in range(l):
            data = pd.read_csv(data_files[i])[typ]
            if l == 1:
                hist_data(axs, i, 0, data, binwidth, rwidth, max_factor, s=1)
            elif l == 2:
                hist_data(axs, i, 0, data, binwidth, rwidth, max_factor, s=2)    
            else: 
                hist_data(axs, 1, 0, data, binwidth, rwidth, max_factor)


    elif l > 3 and l <= 6:
        fig, axs = plt.subplots(math.ceil(l/2), 2)
        
        for i in range(math.ceil(l/2)):
            try:
                data_1 = pd.read_csv(data_files[i])[typ]
                hist_data(axs, i, 0, data_1, binwidth, rwidth, max_factor)
                data_2 = pd.read_csv(data_files[i+math.ceil(l/2)])[typ]
                hist_data(axs, i, 1, data_2, binwidth, rwidth, max_factor)
            except:
                pass

    elif l > 6 and l <= 9:
        fig, axs = plt.subplots(math.ceil(l/3), 3)
        for i in range(math.ceil(l/3)):
            try:
                data_1 = pd.read_csv(data_files[i])[typ]
                hist_data(axs, i, 0, data_1, binwidth, rwidth, max_factor)
                data_2 = pd.read_csv(data_files[i+math.ceil(l/3)])[typ]
                hist_data(axs, i, 1, data_2, binwidth, rwidth, max_factor)
                data_3 = pd.read_csv(data_files[i+math.ceil(2*l/3)])[typ]
                hist_data(axs, i, 2, data_3, binwidth, rwidth, max_factor)
            except:
                pass

    plt.show()

hist_particles_data(sep_blackhole_path, hist_plots)