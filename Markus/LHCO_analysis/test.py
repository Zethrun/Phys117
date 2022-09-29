from random import sample
from selectors import EVENT_READ
from LHCO_reader import partition_problem as pp
from LHCO_reader import LHCO_reader
import matplotlib.pyplot as plt
import numpy as np
import os
from tqdm import tqdm

folder_path = "Data/LHCO/"
path_list = [folder_path + folder_name for folder_name in os.listdir(folder_path)]
file_list = [[path + "/" + filename for filename in os.listdir(path)] for path in path_list]

# for files in file_list:
#     for file in files:
#         events = LHCO_reader.Events(f_name = file)
#         (sumx, sumy) = (0, 0)
#         for event in events:
#             phi = event["MET"][0]["phi"]
#             sumx += np.cos(phi)
#             sumy += np.sin(phi)
            
#         print(sumx, sumy)

file = "Data/LHCO/Background/ttbar_largejet.lhco"

events = LHCO_reader.Events(f_name = file)
for index, event in enumerate(events):
    if event.number()["electron"] >= 2:
        print(index)
        print(event)