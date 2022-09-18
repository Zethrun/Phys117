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

print(file_list)