import enum
from errno import ENETUNREACH
from re import X
from tkinter.tix import FileSelectBox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

#Retrieves all files from data folder
folder_path = "C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/Pandas/Sum/"
path_list = [folder_path + folder_name for folder_name in os.listdir(folder_path)]
file_list = [[path + "/" + filename for filename in os.listdir(path)] for path in path_list]

#Specifies data category to analyse and retrieves only those data files from above
stuffs = ["electron", "jet", "photon", "tau"]


def specific_files(file_list):
    stuffs_csv = [stuff + ".csv" for stuff in stuffs]
    specific_file_list = [[file for stuff in stuffs_csv for file in files if file[-len(stuff):] == stuff] for files in file_list]
    return specific_file_list

