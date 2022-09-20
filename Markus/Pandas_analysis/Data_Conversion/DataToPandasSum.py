from LHCO_reader import partition_problem as pp
from LHCO_reader import LHCO_reader
import pandas as pd
import numpy as np
import os

objects = ["electron", "jet", "MET", "photon", "tau"]

#Retrieves all files from data folder
folder_path = "C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Data/LHCO/"
path_list = [folder_path + folder_name for folder_name in os.listdir(folder_path)]
file_list = [[path + "/" + filename for filename in os.listdir(path)] for path in path_list]
file_names = os.listdir(folder_path)

def data_to_pandas(file_list):
    stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]

    for index, files in enumerate(file_list):
        filename = os.path.dirname(os.path.dirname(folder_path)) + "/Pandas/Sum/" + file_names[index] + "/"

        for stuff in stuffs:
            data = {
                "eta":[],
                "phi":[],
                "PT":[],
                "jmass":[],
                "ntrk":[],
                "btag":[],
                "hadem":[],
                "event#":[]
            }

            (eta, phi, PT, jmass, ntrk, btag, hadem, event_num) = ([], [], [], [], [], [], [], [])

            for file in files:
                
                events = LHCO_reader.Events(f_name = file)


                for event_index, event in enumerate(events):
                    try:
                        for i in range(event.number()[stuff]):
                            eta.append(event[stuff][i]["eta"])
                            phi.append(event[stuff][i]["phi"])
                            PT.append(event[stuff][i]["PT"])
                            jmass.append(event[stuff][i]["jmass"])
                            ntrk.append(event[stuff][i]["ntrk"])
                            btag.append(event[stuff][i]["btag"])
                            hadem.append(event[stuff][i]["hadem"])
                            event_num.append(event_index)
                    except:
                        pass
            
            data["eta"] = eta
            data["phi"] = phi
            data["PT"] = PT
            data["jmass"] = jmass
            data["ntrk"] = ntrk
            data["btag"] = btag
            data["hadem"] = hadem
            data["event#"] = event_num
            data = pd.DataFrame(data)
            data.to_csv(path_or_buf = filename + stuff + ".csv")

data_to_pandas(file_list)