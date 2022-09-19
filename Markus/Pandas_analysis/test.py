import pandas as pd
import numpy as np
import os

file = "C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/Pandas/Individual/Background/ttbar_largejetjet.csv"

with open(file, 'r') as csv:
     first_line = csv.readline()
     your_data = csv.readlines()

ncol = first_line.count(',') + 1 

print(ncol)