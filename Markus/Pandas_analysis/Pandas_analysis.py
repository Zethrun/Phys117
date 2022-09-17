import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
    figure, axis = plt.subplots(int(np.ceil(len(files)/5)), 5)
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

        try:
            axis[x_pos, y_pos].plot(x, y)
            axis[x_pos, y_pos].grid()
            axis[x_pos, y_pos].title(files[i])
            y_pos += 1
            if y_pos % 5 == 0:
                x_pos += 1
                y_pos = 0
        except:
            axis[x_pos].plot(x, y)
            axis[x_pos].grid()
            axis[x_pos].title(files[i])
            x_pos += 1  

        

    plt.show()

for files in file_list:
    plot(files)


