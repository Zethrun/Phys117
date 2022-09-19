import enum
from LHCO_reader import partition_problem as pp
from LHCO_reader import LHCO_reader
import pandas as pd
import numpy as np
import os

#Retrieves all files from data folder
folder_path = "C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/LHCO/"
path_list = [folder_path + folder_name for folder_name in os.listdir(folder_path)]
file_list = [[path + "/" + filename for filename in os.listdir(path)] for path in path_list]
folder_names = os.listdir(folder_path)
file_names = [os.listdir(folder_name) for folder_name in path_list]

def data_to_pandas(file_list):
    data_list = ["electron", "jet", "MET", "photon", "tau"]
    for index_folder, files in enumerate(file_list):

        for index_file, file in enumerate(files):
            filename = os.path.dirname(os.path.dirname(folder_path)) + "/Pandas/Individual/" + folder_names[index_folder] + "/" + file_names[index_folder][index_file][:-len(".lhco")]

            events = LHCO_reader.Events(f_name = file)

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


#data_to_pandas(file_list)

