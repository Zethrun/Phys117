from random import sample
from selectors import EVENT_READ
from LHCO_reader import partition_problem as pp
from LHCO_reader import LHCO_reader
import matplotlib.pyplot as plt
import numpy as np
import os
from tqdm import tqdm

background_path = "C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/LHCO/Background"
bh_path = "C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/LHCO/BH"
sphaleron_path = "C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/LHCO/Sphaleron"
test_path = "C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/LHCO/Test"

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

for files in file_list:
    for file in files:
        events = LHCO_reader.Events(f_name = file)
        (sumx, sumy) = (0, 0)
        for event in events:
            phi = event["MET"][0]["phi"]
            sumx += np.cos(phi)
            sumy += np.sin(phi)
            
        print(sumx, sumy)