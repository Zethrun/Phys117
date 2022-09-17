from LHCO_reader import partition_problem as pp
from LHCO_reader import LHCO_reader
import pandas as pd
import numpy as np
import os

background_path = "C:/Users/mhals/AppData/Local/Programs/Programming/Scripts/Python/Prosjekt/Data/Background"
bh_path = "C:/Users/mhals/AppData/Local/Programs/Programming/Scripts/Python/Prosjekt/Data/BH"
sphaleron_path = "C:/Users/mhals/AppData/Local/Programs/Programming/Scripts/Python/Prosjekt/Data/Sphaleron"

background_files = os.listdir(background_path)
bh_files = os.listdir(bh_path)
sphaleron_files = os.listdir(sphaleron_path)

file_list = [
    background_files,
    bh_files,
    sphaleron_files
]

def data_to_pandas(file_list):
    data_list = ["jet", "electron", "tau", "photon", "MET"]

    for file in file_list:
        if file_list == background_files:
            events = LHCO_reader.Events(f_name = background_path + "/" + file)
            filename = background_path[:-10] + "Pandas/Background/" + file[:-5]
        elif file_list == bh_files:
            events = LHCO_reader.Events(f_name = bh_path + "/" + file)
            filename = bh_path[:-2] + "Pandas/BH/" + file[:-5]
        else:
            events = LHCO_reader.Events(f_name = sphaleron_path + "/" + file)
            filename = sphaleron_path[:-9] + "Pandas/Sphaleron/" + file[:-5]

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

