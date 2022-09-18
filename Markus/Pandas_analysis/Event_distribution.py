import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

path_list = [
"C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/Pandas/Background",
"C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/Pandas/BH",
"C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/Pandas/Sphaleron",
"C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/Pandas/Test"
]

objects = ["jet", "electron", "tau", "photon"]

def file_list_func(path_list):
    file_list = []

    for path in path_list:
        files = [path + "/" + filename for filename in os.listdir(path)]
        file_list.append(files)

    return file_list

file_list = file_list_func(path_list)

def specific_file_list_func(file_list):
    objects_csv = [object + ".csv" for object in objects]
    specific_file_list = [[file for object in objects_csv for file in files if file[-len(object):] == object] for files in file_list]
    
    return specific_file_list

specific_file_list = specific_file_list_func(file_list)

def list_categorization(files):
    categorized = [files[i*int(len(files)/len(objects)):(i + 1)*int(len(files)/len(objects))] for i in range(len(objects))]
    return categorized

def data_and_plot(file_list):
    plt.figure()
    (x_len, y_len) = plot_values(file_list)
    
    for index_plot, files in enumerate(file_list):
        categorized = list_categorization(files)
        data = []

        for index_category, category in enumerate(categorized):
            counts = 0

            for file in category:
                file = pd.read_csv(file)
                counts += int(file.size/8)
            
            data.append(counts)
        
        parent_path = "C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/Pandas/"
        path = path_list[index_plot]
        title = path[len(parent_path):]
        data = np.array(data)
        relative_data = np.round(data*100/np.sum(data), 2)
        plot_style(data, relative_data, x_len, y_len, index_plot, title)
    
    plt.show()

def plot_values(files):
    plot_amount = len(files)
    diff = 200

    for i in range(1, plot_amount + 1):

        for j in range(1, plot_amount + 1):
            
            if i * j == plot_amount and np.abs(i - j) < diff:
                diff = np.abs(i - j)
                (x, y) = (np.min((i, j)), np.max((i, j)))
    
    return (x, y)

def plot_style(data, relative_data, x_len, y_len, index_plot, title):
    style = "seaborn-darkgrid"
    plt.style.use(style)
    plt.subplot(x_len, y_len, index_plot + 1)
    plt.title(title)
    labels = [object + " - " + str(data) + "%" for object, data in zip(objects, relative_data)]
    plt.pie(data, labels = labels)
    plt.grid()

data_and_plot(specific_file_list)