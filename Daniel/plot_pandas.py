import matplotlib.pyplot as plt
import numpy as np
from LHCO_reader import LHCO_reader
import pandas as pd
import os
import tqdm

background_path = "C:/Users/danie/OneDrive/Dokumenter/Studie/phys117/coding/data_pandas/background"
blackhole_path = "C:/Users/danie/OneDrive/Dokumenter/Studie/phys117/coding/data_pandas/BH"
sphaleron_path = "C:/Users/danie/OneDrive/Dokumenter/Studie/phys117/coding/data_pandas/sphaleron"


binwidth = 20
def hist_data(data, binwidth):
    plt.hist(data, bins=range(int(min(data)), int(max(data)) + binwidth, binwidth), density = True)
    plt.show()

data = pd.read_csv(blackhole_path + "/" + "MET.csv")["PT"]
hist_data(data, binwidth)

