from LHCO_reader import partition_problem as pp
from LHCO_reader import LHCO_reader
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

#Retrieves all files from data folder
folder_path = "C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/Pandas/"
path_list = [folder_path + folder_name for folder_name in os.listdir(folder_path)]
file_list = [[path + "/" + filename for filename in os.listdir(path)] for path in path_list]

def plot(files):
    figre, axis = plt.subplots(int(np.ceil(len(files)/5)), 5)
    (x_pos, y_pos) = (0, 0)

    for i in range(len(files)):
        file = pd.read_csv(files[i])
        phi = np.array(file["phi"])
        (sumx, sumy) = (0, 0)
        (x, y, z) = ([], [], [])

        for j in range(len(phi)):
            sumx += np.cos(phi[j])
            sumy += np.sin(phi[j])
            x.append(sumx)
            y.append(sumy)
            z.append(j)

        try:
            axis[x_pos, y_pos].plot(x, z)
            axis[x_pos, y_pos].plot(y, z)
            axis[x_pos, y_pos].grid()
            y_pos += 1
            if y_pos % 5 == 0:
                x_pos += 1
                y_pos = 0
        except:
            axis[x_pos].plot(x, y)
            axis[x_pos].plot(y, z)
            axis[x_pos].grid()
            x_pos += 1  

        

    plt.show()

for files in file_list:
    plot(files)

