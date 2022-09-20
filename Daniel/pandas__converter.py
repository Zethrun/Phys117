import numpy as np
from LHCO_reader import LHCO_reader
import pandas as pd
import os

#########
background_path = "C:/Users/danie/OneDrive/Dokumenter/Studie/phys117/coding/data/background"
blackhole_path = "C:/Users/danie/OneDrive/Dokumenter/Studie/phys117/coding/data/BH"
sphalerion_path = "C:/Users/danie/OneDrive/Dokumenter/Studie/phys117/coding/data/sphaleron"

new_background_path = "C:/Users/danie/OneDrive/Dokumenter/Studie/phys117/coding/data_pandas/background"
new_blackhole_path = "C:/Users/danie/OneDrive/Dokumenter/Studie/phys117/coding/data_pandas/BH"
new_sphaleron_path = "C:/Users/danie/OneDrive/Dokumenter/Studie/phys117/coding/data_pandas/sphaleron"
#########


columns = ["event", "eta", "phi", "PT", "jmass", "ntrk", "btag", "hadem"]
particle_list = ["photon", "electron", "muon", "tau", "jet", "MET"]


def convert_file_pandas(data_folder, output_folder, file):
    pass

def sort_files_particles(data_folder_path, output_folder_path): #folder variable means folders path
    file_list = [data_folder_path + "/" + filename for filename in os.listdir(data_folder_path)]

    count_dict = {
        "photon" : {
            "event" : [],
            "eta" : [],
            "phi" : [],
            "PT" : [],
            "jmass" : [],
            "ntrk" : [],
            "btag" : [],
            "hadem" : []
        },
        "electron" : {
            "event" : [],
            "eta" : [],
            "phi" : [],
            "PT" : [],
            "jmass" : [],
            "ntrk" : [],
            "btag" : [],
            "hadem" : []
        },
        "muon" : {
            "event" : [],
            "eta" : [],
            "phi" : [],
            "PT" : [],
            "jmass" : [],
            "ntrk" : [],
            "btag" : [],
            "hadem" : []
        },
        "tau" : {
            "event" : [],
            "eta" : [],
            "phi" : [],
            "PT" : [],
            "jmass" : [],
            "ntrk" : [],
            "btag" : [],
            "hadem" : []
        },
        "jet" : {
            "event" : [],
            "eta" : [],
            "phi" : [],
            "PT" : [],
            "jmass" : [],
            "ntrk" : [],
            "btag" : [],
            "hadem" : []
        },
        "MET" : {
            "event" : [],
            "eta" : [],
            "phi" : [],
            "PT" : [],
            "jmass" : [],
            "ntrk" : [],
            "btag" : [],
            "hadem" : []
        }
    }

    for file in file_list:
        events = LHCO_reader.Events(file)
        event_nr = 0
        
        for event in events:
            for i in particle_list:
                particles = event[i]
                size = len(particles)
                for j in range(size):
                    particle = particles[j]

                    count_dict[i]["event"].append(event_nr)
                    count_dict[i]["eta"].append(particle["eta"])
                    count_dict[i]["phi"].append(particle["phi"])
                    count_dict[i]["PT"].append(particle["PT"])
                    count_dict[i]["jmass"].append(particle["jmass"])
                    count_dict[i]["ntrk"].append(particle["ntrk"])
                    count_dict[i]["btag"].append(particle["btag"])
                    count_dict[i]["hadem"].append(particle["hadem"])


            event_nr += 1 

    for particle in particle_list:
        csv_file = pd.DataFrame(count_dict[particle])
        csv_file.to_csv(output_folder_path + "/" + particle + ".csv")

sort_files_particles(sphalerion_path, new_sphaleron_path)