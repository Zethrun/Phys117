import matplotlib.pyplot as plt
import numpy as np
from LHCO_reader import LHCO_reader
import pandas as pd
import os
import tqdm

background_path = "Daniel/data/data_lhco/background"
blackhole_path = "Daniel/data/data_lhco/BH"
sphaleron_path = "Daniel/data/data_lhco/sphaleron"

### Accessing data ###

events = LHCO_reader.Events(blackhole_path + "\BH_n4_M8.lhco")
print(events)
print(events[4]["jet"][0]["eta"])

count_dict = {
    "photon" : 0,
    "electron" : 0,
    "muon" : 0,
    "tau" : 0,
    "jet" : 0,
    "MET" : 0
}

labels = [i for i in count_dict]

l_photon, l_electron, l_muon, l_tau, l_jet, l_MET = [],[],[],[],[],[]

for event in events:
    num_p = event.number()["photon"]
    count_dict["photon"] += num_p
    l_photon.append(num_p)

    num_e = event.number()["electron"]
    count_dict["electron"] += num_e
    l_electron.append(num_e)
    
    num_m = event.number()["muon"]
    count_dict["muon"] += num_m
    l_muon.append(num_m)

    num_t = event.number()["tau"]
    count_dict["tau"] += num_t
    l_tau.append(num_t)

    num_j = event.number()["jet"]
    count_dict["jet"] += num_j
    l_jet.append(num_j)
    
    num_MET = event.number()["MET"]
    count_dict["MET"] += num_MET
    l_MET.append(num_MET)


### Pie chart ###

remove_met = True

values = [count_dict[i] for i in labels]
if remove_met:
    values.remove(count_dict["MET"])
    pie_labels = labels
    pie_labels.remove("MET")
    explode = [0,0,0,0,0.15]
else:
    explode = [0,0,0,0,0.15,0]   #this is to get the pieces out and being highlighted

fig1, ax1 = plt.subplots()
ax1.pie(values, explode = explode, labels = labels, autopct = "%1.1f%%", shadow = True, startangle = 45)
ax1.axis("equal")

plt.show()


### hist of events ##

binwidth = 1
def hist_data(data, binwidth):
    plt.hist(data, histtype = "bar", bins=range(min(data), max(data) + binwidth, binwidth), density = True)
    plt.show()

data = l_photon #change this for type of particle
hist_data(data, binwidth)


### continous dist of events ###








