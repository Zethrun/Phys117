import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from difflib import SequenceMatcher as sm

#Retrieves all files from data folder
folder_path = "C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/Pandas/Individual/"
path_list = [folder_path + folder_name for folder_name in os.listdir(folder_path)]
file_list = [[path + "/" + filename for filename in os.listdir(path)] for path in path_list]

#Specifies data category to analyse and retrieves only those data files from above
stuffs = ["electron", "jet", "muon", "photon", "tau"]


def specific_files(file_list):
    stuffs_csv = [stuff + ".csv" for stuff in stuffs]
    specific_file_list = [[file for stuff in stuffs_csv for file in files if file[-len(stuff):] == stuff] for files in file_list]
    return specific_file_list


#Takes list of datafiles from event type (i.e. background, blackhole etc) and returns a list of lists containing the datafiles pertaining to a specific object in objects_list
#So of the form [[data1jet.csv, data2jet.csv], [data1electron.csv, data2electron.csv]... etc]
def list_categorization(files):
    categorized = [files[i*int(len(files)/len(stuffs)):(i + 1)*int(len(files)/len(stuffs))] for i in range(len(stuffs))]
    return categorized


#Determines the shape of the subplot figure trying to be as square as possible
#Should change it in case the amount of subplots is a prime number
def plot_values(files):
    plot_amount = int(len(files)/len(stuffs))
    diff = 200

    for i in range(1, plot_amount + 1):

        for j in range(1, plot_amount + 1):
            
            if i * j == plot_amount and np.abs(i - j) < diff:
                diff = np.abs(i - j)
                (x, y) = (np.min((i, j)), np.max((i, j)))
    
    return (x, y)


#Takes index of subplot and returns the name of folder as title
def subplot_title(filenames):
    for i in range(len(filenames)):
        for j in range(len(filenames)):
            if i != j:
                match = sm(None, filenames[i], filenames[j]).find_longest_match(0, len(filenames[i]), 0, len(filenames[j]))
                title = filenames[i][match.a:match.a + match.size]
    return title


#Takes the categorized datafiles from above and returns the total count of events
#such as jets or electrons from event types and their relative counts for pie plot
def data_pie(files, index):
    data = []

    for category in files:
        file = pd.read_csv(category[index])
        data.append(int(file.size/8))
    
    data = np.array(data)
    relative_data = np.round(data*100/np.sum(data), 2)
    return data, relative_data


#Plots the data in a piechart
def plot_pie(data, relative_data, x_len, y_len, index_plot, title):
    style = "seaborn-darkgrid"
    plt.style.use(style)
    plt.subplot(x_len, y_len, index_plot + 1)
    plt.title(title)
    labels = [object + " - " + str(data) + "%" for object, data in zip(stuffs, relative_data)]
    plt.pie(data, labels = labels)
    plt.grid()


#Takes the data from the file_list and runs it through the functions above plotting the data
def plot(file_list):
    plt.figure()

    for index_folder, files in enumerate(file_list):
        (x_len, y_len) = plot_values(files)
        amount_per_category = int(len(files)/len(stuffs))

        for index_file in range(amount_per_category):        
            categorized = list_categorization(files)
            title = subplot_title([os.path.basename(categorized[i][index_file]) for i in range(len(stuffs))])
            data, relative_data = data_pie(categorized, index_file)
            plot_pie(data, relative_data, x_len, y_len, index_file, title)

        plt.show()

plot(specific_files(file_list))