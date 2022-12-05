import pandas as pd
import os
stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
data_variables = ["HT", "met", "phi_diff", "ptmax", "stuff_amount"]
file_amounts = [2, 18, 3]


def work_space(path):
    while True:
        if os.path.split(path)[1] != "Phys117":
            path = os.path.split(path)[0]
        else:
            return path.replace("\\", "/")

work_dir = work_space(os.getcwd())
data_path = work_dir + "/Markus/Hub/VariableData/"
folders = os.listdir(data_path)
data_files = [data_path + data_file for data_file in folders]


def remover(old_list, index):
    new_list = [element for element_index, element in enumerate(old_list) if element_index != index]
    return new_list


def list_unpacker(folder_data, new_folder_data):
    for nested_list in folder_data:
        if type(nested_list) == list:
            list_unpacker(nested_list, new_folder_data)
        else:
            new_folder_data.append(nested_list)
    folder_data = new_folder_data
    return folder_data


def dataframe_retriever(data_path, data_variables):
    folders = os.listdir(data_path)
    folder_filenames = [os.listdir(data_path + folder) for folder in folders]
    folder_filepaths = [[data_path + folder + "/" + filename for filename in folder_filenames[folder_index]] for folder_index, folder in enumerate(folders)]
    dataframes = [[(pd.read_csv(filepath).drop("Unnamed: 0", axis = 1), filename) for filepath, filename in zip(filepaths, filenames)] for filepaths, filenames in zip(folder_filepaths, folder_filenames)]
    return dataframes



def dropper(dataframe, data_variables):
    to_drop = [col for col in dataframe.columns if col not in data_variables]
    dataframe = dataframe.drop(to_drop, axis = 1)
    return dataframe


def sampler(model_dataframes, file_amounts):
    from random import sample
    new_dataframes = []
    for file_amount, dataframes in zip(file_amounts, model_dataframes):
        new_dataframes.append(sample(dataframes, file_amount)) if type(file_amount) == int else new_dataframes.append([dataframe for dataframe in dataframes if dataframe[1] in file_amount])
    return new_dataframes


from FilesFunc import files
from Plotter import plotter
folders = ["Background", "BH", "Sphaleron"]

filenames_dict = {
    "PP13-Sphaleron-THR9-FRZ15-NB0-NSUBPALL": "Sphal1",
    "PP13-Sphaleron-THR9-FRZ15-NB33-60-NSUBP50": "Sphal2",
    "PP13-Sphaleron-THR9-FRZ15-NB33-71-NSUBP5": "Sphal3",
    "BH_n4_M8": "BH1",
    "BH_n4_M9": "BH2",
    "BH_n4_M9_Mpl9": "BH3",
    "BH_n4_M10": "BH4",
    "BH_n4_M11": "BH5",
    "BH_n4_M12": "BH6",
    "BH_n5_M8": "BH7",
    "BH_n5_M9": "BH8",
    "BH_n5_M10": "BH9",
    "BH_n5_M11": "BH10",
    "BH_n5_M12": "BH11",
    "BH_n6_M8": "BH12",
    "BH_n6_M9": "BH13",
    "BH_n6_M10": "BH14",
    "BH_n6_M11": "BH15",
    "BH_n6_M12": "BH16",
    "BlackMaxOutputFirstRun1": "BH17",
    "BlackMaxOutputFirstRun2": "BH18",
    "ttbar": "ttbar1",
    "ttbar_largejet": "ttbar2"
}

folder_dataframes = dataframe_retriever(data_path, data_variables)
file_amounts = [2, 18, 3]
colors = []
for index, file_amount in enumerate(file_amounts):
    temp_list = []
    for amount in range(1, 1 + file_amount):
        rgb = [0, 0, 0]
        rgb[index] = (amount + 3) * 1 / (file_amount + 6)
        rgb[int((index + 2) % 3)] = (amount + 3) * 1 / (file_amount + 6)
        temp_list.append(rgb)
    colors.append(temp_list)
model_dataframes = sampler(folder_dataframes, file_amounts)

model_dataframes = [[(dropper(dataframe[0], data_variables), dataframe[1]) for dataframe in dataframes] for dataframes in model_dataframes]
filenames_input = [[filenames_dict[dataframe[1][:-len(".csv")]] for dataframe in dataframes] for dataframes in model_dataframes]
dataframes_input = [[dataframe[0] for dataframe in dataframes] for dataframes in model_dataframes]
plotter(data_variables, model_dataframes, filenames_input, colors = colors, filter_strengths = [0.99, 0.85, 1, 0.985, 1], binsizes = [50, 15, 0.2, 25, 0.5])
