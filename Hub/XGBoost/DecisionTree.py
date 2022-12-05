# Import modules
import numpy as np
from tqdm import tqdm
import pandas as pd
import os


def work_space(path):
    while True:
        if os.path.split(path)[1] != "Phys117":
            path = os.path.split(path)[0]
        else:
            return path.replace("\\", "/")

work_dir = work_space(os.getcwd())
data_path = work_dir + "/Markus/Hub/Efficiencies/EfficiencyData/"
filenames = os.listdir(data_path)
data_files = [data_path + data_file for data_file in filenames]
folders = ["BH", "Sphaleron"]
stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
data_variables = ["HT", "met", "phi_diff", "ptmax", "stuff_amount"]


filenames_path = work_dir + "/Data/Pandas/Individual/"
from FilesFunc import files
folder_list, filename_list = files(filenames_path, folders, file_amounts = [18, 3])
bh_files = [filename + ".csv" for filename in filename_list[0]]
sphal_files = [filename + ".csv" for filename in filename_list[1]]



def retriever(data_files):
    dataframes = [(pd.read_csv(data_file), filename) for data_file, filename in zip(data_files, filenames)]
    return dataframes


def selector(combine_data, dataframes):
    if combine_data:
        dataframes = [dataframe[0].drop("Unnamed: 0", axis = 1).set_index(dataframe[0]["Unnamed: 0"]) for dataframe in dataframes if dataframe[1][-len("Combined.csv"):] == "Combined.csv"]
    else:
        dataframes = [dataframe[0].drop("Unnamed: 0", axis = 1).set_index(dataframe[0]["Unnamed: 0"]) for dataframe in dataframes if dataframe[1][-len("Combined.csv"):] != "Combined.csv"]
    
    return dataframes


def eff_tup_retriever(combine_data, folders, bh_file, sphal_file):
    data_variables = ["HT", "met", "phi_diff", "ptmax", "stuff_amount"]
    dataframes = retriever(data_files)
    dataframes = selector(combine_data, dataframes)
    eff_tups = []

    for variable, dataframe in zip(data_variables, dataframes):
        if combine_data:
            eff_tup = dataframe[folders.index("Sphaleron")][folders.index("BH")]
            eff_tups.append(eff_tup)
        else:
            eff_tup = dataframe[sphal_file][bh_file]
            eff_tups.append(eff_tup)

    return eff_tups, data_variables


def EventDataRetriever(folders, filenames):
    data_path = work_dir + "/Markus/Hub/VariableData/"
    dataframes = []
    for folder in folders:
        data_files = [data_path + folder + "/" + data_file for data_file in os.listdir(data_path + folder)]
        folder_dataframes = [(pd.read_csv(data_file).drop(["Unnamed: 0"], axis = 1), filename) for data_file, filename in zip(data_files, filenames)]
        dataframes.append(folder_dataframes)
    
    return dataframes


def selector(bh_file, sphal_file, dataframes):
    bh_dataframe = [dataframe for dataframe in dataframes if dataframe[1] == bh_file][0]
    sphal_dataframe = [dataframe for dataframe in dataframes if dataframe[1] == sphal_file][0]
    return bh_dataframe, sphal_dataframe


folders = ["BH", "Sphaleron"]
dataframes = EventDataRetriever(folders, filename_list)
def EventEvaluator(dataframes, eff_tups, data_variables):
    bh_dataframe, sphal_dataframe = dataframes

    total = 0
    indeterminate = 0
    correct = 0
    for event in bh_dataframe.iloc[:]:
        sphal_or_bh = []
        for eff_tup, variable in zip(eff_tups, data_variables):
            eff_val = eff_tup[0]
            eff_rel = eff_tup[2]
            event_variable = event[variable]
            if eff_rel == "BH > Sphal":
                if event_variable > eff_val:
                    sphal_or_bh.append(True)
            elif event_variable < eff_val:
                sphal_or_bh.append(True)
        
        if sphal_or_bh.count(True) > len(data_variables) / 2:
            correct += 1
        elif sphal_or_bh.count(True) == len(data_variables) / 2:
            indeterminate += 1
        
        total += 1
    
    for event in sphal_dataframe.iloc[:]:
        sphal_or_bh = []
        for eff_tup, variable in zip(eff_tups, data_variables):
            eff_val = eff_tup[0]
            eff_rel = eff_tup[2]
            event_variable = event[variable]
            if eff_rel == "BH < Sphal":
                if event_variable > eff_val:
                    sphal_or_bh.append(True)
            elif event_variable < eff_val:
                sphal_or_bh.append(True)
        
        if sphal_or_bh.count(True) > len(data_variables) / 2:
            correct += 1
        elif sphal_or_bh.count(True) == len(data_variables) / 2:
            indeterminate += 1
        
        total += 1

    accuracy = np.round(correct / total, 4)
    
    return total, indeterminate, correct, accuracy



def retriever(data_files, filenames):
    dataframes = [(unpacker(pd.read_csv(data_file).drop("Unnamed: 0", axis = 1), [])[0], filename) for data_file, filename in zip(data_files, filenames)]
    return dataframes


def dataframe_retriever(data_files, folders, filename_list):
    dataframes = [(unpacker(pd.read_csv(data_file).drop("Unnamed: 0", axis = 1), [])[0], filename) for data_file, filename in zip(list_unpacker(data_files, []), list_unpacker(filename_list, []))]
    return dataframes