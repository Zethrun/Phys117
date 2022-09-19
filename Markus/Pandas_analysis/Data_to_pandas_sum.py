from LHCO_reader import partition_problem as pp
from LHCO_reader import LHCO_reader
import pandas as pd
import numpy as np
import os

#Retrieves all files from data folder
folder_path = "C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/Pandas/"
path_list = [folder_path + folder_name for folder_name in os.listdir(folder_path)]
file_list = [[path + "/" + filename for filename in os.listdir(path)] for path in path_list]

def data_to_pandas(file_list):
    data_list = ["electron", "jet", "MET", "photon", "tau"]

    for index, file in enumerate(file_list):
        if index == 0:
            events = LHCO_reader.Events(f_name = path_list[0] + "/" + file)
            filename = path_list[0][:-15] + "Pandas/Background/" + file[:-5]
        elif index == 1:
            events = LHCO_reader.Events(f_name = path_list[1] + "/" + file)
            filename = path_list[1][:-7] + "Pandas/BH/" + file[:-5]
        elif index == 2:
            events = LHCO_reader.Events(f_name = path_list[2] + "/" + file)
            filename = path_list[2][:-14] + "Pandas/Sphaleron/" + file[:-5]
        else:
            events = LHCO_reader.Events(f_name = path_list[3] + "/" + file)
            filename = path_list[3][:-9] + "Pandas/Test/" + file[:-5]                

        for object in data_list:
            data = {
                "eta":[],
                "phi":[],
                "PT":[],
                "jmass":[],
                "ntrk":[],
                "btag":[],
                "hadem":[]
            }
            (eta, phi, PT, jmass, ntrk, btag, hadem) = ([], [], [], [], [], [], [])

            for event in events:
                try:
                    for i in range(event.number()[object]):
                        eta.append(event[object][i]["eta"])
                        phi.append(event[object][i]["phi"])
                        PT.append(event[object][i]["PT"])
                        jmass.append(event[object][i]["jmass"])
                        ntrk.append(event[object][i]["ntrk"])
                        btag.append(event[object][i]["btag"])
                        hadem.append(event[object][i]["hadem"])
                except:
                    pass
            
            data["eta"] = eta
            data["phi"] = phi
            data["PT"] = PT
            data["jmass"] = jmass
            data["ntrk"] = ntrk
            data["btag"] = btag
            data["hadem"] = hadem
            data = pd.DataFrame(data)
            data.to_csv(path_or_buf = filename + object + ".csv")

for file in file_list:
    data_to_pandas(file)

