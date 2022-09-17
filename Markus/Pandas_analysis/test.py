from LHCO_reader import partition_problem as pp
from LHCO_reader import LHCO_reader
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

background_path = "C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/Pandas/Background"
bh_path = "C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/Pandas/BH"
sphaleron_path = "C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/Pandas/Sphaleron"
test_path = "C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/Pandas/Test"

background_files = os.listdir(background_path)
bh_files = os.listdir(bh_path)
sphaleron_files = os.listdir(sphaleron_path)
test_files = os.listdir(test_path)

file_list = [
    [background_path + "/" + filename for filename in background_files],
    [bh_path + "/" + filename for filename in bh_files],
    [sphaleron_path + "/" + filename for filename in sphaleron_files],
    [test_path + "/" + filename for filename in test_files]
]

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

