import enum
from fileinput import filename
from LHCO_reader import partition_problem as pp
from LHCO_reader import LHCO_reader
import pandas as pd
import numpy as np
import os

#Retrieves all files from data folder
folder_path = "Data/LHCO/"
path_list = [folder_path + folder_name for folder_name in os.listdir(folder_path)]
file_list = [[path + "/" + filename for filename in os.listdir(path)] for path in path_list]
folder_names = os.listdir(folder_path)
file_names = [os.listdir(folder_name) for folder_name in path_list]

def data_to_pandas(file_list):
    stuffs = ["electron", "jet", "MET", "muon", "photon", "tau"]
    for index_folder, files in enumerate(file_list):

        for index_file, file in enumerate(files):
            foldername = os.path.dirname(os.path.dirname(folder_path)) + "/Pandas/" + folder_names[index_folder] + "/" + file_names[index_folder][index_file][:-len(".lhco")] + "/"

            events = LHCO_reader.Events(f_name = file)

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
                try:
                    os.makedirs(foldername)
                except:
                    pass
                data.to_csv(path_or_buf = foldername + stuff + ".csv")


data_to_pandas(file_list)

