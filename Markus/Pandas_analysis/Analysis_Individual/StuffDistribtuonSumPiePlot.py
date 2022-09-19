import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

#Retrieves all files from data folder
folder_path = "C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/Pandas/Individual/"
path_list = [folder_path + folder_name for folder_name in os.listdir(folder_path)]
file_list = [[path + "/" + filename for filename in os.listdir(path)] for path in path_list]

#Specifies data category to analyse and retrieves only those data files from above
objects = ["electron", "jet", "photon", "tau"]


def specific_files(file_list):
    objects_csv = [object + ".csv" for object in objects]
    specific_file_list = [[file for object in objects_csv for file in files if file[-len(object):] == object] for files in file_list]
    return specific_file_list


#Takes list of datafiles from event type (i.e. background, blackhole etc) and returns a list of lists containing the datafiles pertaining to a specific object in objects_list
#So of the form [[data1jet.csv, data2jet.csv], [data1electron.csv, data2electron.csv]... etc]
def list_categorization(files):
    categorized = [files[i*int(len(files)/len(objects)):(i + 1)*int(len(files)/len(objects))] for i in range(len(objects))]
    return categorized


#Determines the shape of the subplot figure trying to be as square as possible
#Should change it in case the amount of subplots is a prime number
def plot_values(files):
    plot_amount = len(files)
    diff = 200

    for i in range(1, plot_amount + 1):

        for j in range(1, plot_amount + 1):
            
            if i * j == plot_amount and np.abs(i - j) < diff:
                diff = np.abs(i - j)
                (x, y) = (np.min((i, j)), np.max((i, j)))
    
    return (x, y)


#Takes index of subplot and returns the name of folder as title
def subplot_title(index_plot):
    path = path_list[index_plot]
    title = path[len(folder_path):]
    return title


#Takes the categorized datafiles from above and returns the total count of events
#such as jets or electrons from event types and their relative counts for pie plot
def data_pie(files):
    categorized = list_categorization(files)
    data = []

    for category in categorized:
        counts = 0

        for file in category:
            with open(file, 'r') as csv:
                first_line = csv.readline()
                your_data = csv.readlines()
            ncol = first_line.count(',') + 1

            file = pd.read_csv(file)
            counts += int(file.size/ncol)
             
        data.append(counts)
    
    data = np.array(data)
    relative_data = np.round(data*100/np.sum(data), 2)
    return data, relative_data


#Plots the data in a piechart
def plot_pie(data, relative_data, x_len, y_len, index_plot, title):
    style = "seaborn-darkgrid"
    plt.style.use(style)
    plt.subplot(x_len, y_len, index_plot + 1)
    plt.title(title)
    labels = [object + " - " + str(data) + "%" for object, data in zip(objects, relative_data)]
    plt.pie(data, labels = labels)
    plt.grid()


#Takes the data from the file_list and runs it through the functions above plotting the data
def plot(file_list):
    plt.figure()
    (x_len, y_len) = plot_values(file_list)

    for index_plot, files in enumerate(file_list):
        data, relative_data = data_pie(files)
        title = subplot_title(index_plot)
        plot_pie(data, relative_data, x_len, y_len, index_plot, title)
    
    plt.show()

plot(specific_files(file_list))