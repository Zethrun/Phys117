import numpy as np
from LHCO_reader import LHCO_reader
import pandas as pd
import os

#########
background_path = "Daniel/data/data_lhco/background"
blackhole_path = "Daniel/data/data_lhco/BH"
sphaleron_path = "Daniel/data/data_lhco/sphaleron"

new_sep_background_path = "Daniel/data/data_pandas/gathered_seperated/background"
new_sep_blackhole_path = "Daniel/data/data_pandas/gathered_seperated/BH"
new_sep_sphaleron_path = "Daniel/data/data_pandas/gathered_seperated/sphaleron"

new_norm_background_path = "Daniel/data/data_pandas/normal/background"
new_norm_blackhole_path = "Daniel/data/data_pandas/normal/BH"
new_norm_sphaleron_path = "Daniel/data/data_pandas/normal/sphaleron"
#########


columns = ["event", "eta", "phi", "PT", "jmass", "ntrk", "btag", "hadem"]
particle_list = ["photon", "electron", "muon", "tau", "jet", "MET"]


def conv_singlefile(data_folder_path, output_folder_path, file):

    count_dict = {
        "event" : [],
        "particle" : [],
        "eta" : [],
        "phi" : [],
        "PT" : [],
        "jmass" : [],
        "ntrk" : [],
        "btag" : [],
        "hadem" : []
    }

    try:
        events = LHCO_reader.Events(data_folder_path + "/" + file)
        event_nr = 0
        
        for event in events:
            for i in particle_list:
                particles = event[i]
                size = len(particles)
                for j in range(size):
                    particle = particles[j]

                    count_dict["event"].append(event_nr)
                    count_dict["particle"].append(i)
                    count_dict["eta"].append(particle["eta"])
                    count_dict["phi"].append(particle["phi"])
                    count_dict["PT"].append(particle["PT"])
                    count_dict["jmass"].append(particle["jmass"])
                    count_dict["ntrk"].append(particle["ntrk"])
                    count_dict["btag"].append(particle["btag"])
                    count_dict["hadem"].append(particle["hadem"])


            event_nr += 1 
        
    except:
        print("")
        print(f"Error: (Probably '{file}' has a wrong format.)")
        print("List of file:")
        print(file)
        print("Is there a file too much with wrong format?")
        print("")
    
    csv_file = pd.DataFrame(count_dict)
    csv_file.to_csv(output_folder_path + "/" + file.removesuffix(".lhco") + ".csv")

def conv_files_normally(data_folder_path, output_folder_path):
    file_list = [filename for filename in os.listdir(data_folder_path)]

    for file in file_list:
        conv_singlefile(data_folder_path, output_folder_path, file)

def conv_seperate_gather_particles(data_folder_path, output_folder_path): #folder variable means folders path
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
        try:
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
        
        except:
            print("")
            print(f"Error: (Probably '{file}' has a wrong format.)")
            print("List of file:")
            print(file_list)
            print("Is there a file too much with wrong format?")
            print("")

    for particle in particle_list:
        csv_file = pd.DataFrame(count_dict[particle])
        csv_file.to_csv(output_folder_path + "/" + particle + ".csv")

#conv_singlefile(background_path, new_norm_background_path, "ttbar.lhco")
conv_files_normally(background_path,new_norm_background_path)
#conv_seperate_gather_particles(sphaleron_path, new_sep_sphaleron_path)