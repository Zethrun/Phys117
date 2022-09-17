import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

background_path = "C:/Users/mhals/AppData/Local/Programs/Programming/Scripts/Python/Prosjekt/Markus/Data/Pandas/Background"
bh_path = "C:/Users/mhals/AppData/Local/Programs/Programming/Scripts/Python/Prosjekt/Markus/Data/Pandas/BH"
sphaleron_path = "C:/Users/mhals/AppData/Local/Programs/Programming/Scripts/Python/Prosjekt/Markus/Data/Pandas/Sphaleron"

background_files = os.listdir(background_path)
bh_files = os.listdir(bh_path)
sphaleron_files = os.listdir(sphaleron_path)

file_list = [
    [background_path + "/" + filename for filename in background_files],
    [bh_path + "/" + filename for filename in bh_files],
    [sphaleron_path + "/" + filename for filename in sphaleron_files]
]

def plot(files):
    print(files)
    figre, axis = plt.subplots(int(np.ceil(len(files)/5)), 5)
    (x_pos, y_pos) = (0, 0)
    for i in range(len(files)):
        file = pd.read_csv(files[i])
        PT = np.array(file["PT"])
        phi = np.array(file["phi"])
        (PTx, PTy) = (0, 0)
        (x, y) = ([], [])

        for j in range(len(PT)):
            PTx += PT[j]*np.cos(phi[j])
            PTy += PT[j]*np.sin(phi[j])
            energy = np.sqrt(np.square(PTx) + np.square(PTy))
            x.append(energy)
            y.append(j)

        axis[x_pos, y_pos].plot(x, y)
        axis[x_pos, y_pos].grid()

        if x_pos == 0:
            plt.ylabel(ylabel = "Events")
        if y_pos == 4:
            plt.xlabel(xlabel = "MET")

        y_pos += 1
        if y_pos % 5 == 0:
            x_pos += 1
            y_pos = 0

    plt.show()

for files in file_list:
    plot(files)


