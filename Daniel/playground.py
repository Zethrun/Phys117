import pandas as pd
import os

new_folder_path = "subfolder/"
filename = "test.csv"

data = {
    0 : ["Hei", "Hallo"],
    1 : ["Nei", "No"],
    2 : ["Ja", "Yes"]
}

df = pd.DataFrame(data)
"""
def compress_to_zip():
    compression_opts = dict(method="zip", archive_name="out.csv")

    df.to_csv("out.zip", index=False, compression=compression_opts)

def create_file():
    os.makedirs(new_folder_path, exist_ok = True)
    df.to_csv(new_folder_path + filename)
"""

path = "C:/Users/danie/OneDrive/Dokumenter/Studie/phys117/coding/data_pandas/BH"
print(pd.read_csv(path + "/" + "MET.csv"))


#os.makedirs for lage folder
#to_csv(file path + )

def org_files_folder(path_list_tuple):
    path_list = path_list_tuple[0]
    org_dict = {
        "background" : [[],[]],
        "BH" : [[],[]],
        "sphaleron" : [[],[]],
        "test" : []
    }

    if path_list_tuple[1] == "sep":
        for index, path in enumerate(path_list):
            path_file_list = [path + "/" + files for files in os.listdir(path)]
            for file in path_file_list:
                path_particle_list = [file + "/" + particle_file for particle_file in os.listdir(file)]
                org_dict[path_names[index]].append(path_particle_list)

        return org_dict
    
    elif path_list_tuple[1] == "sum":
        for index, path in enumerate(path_list):
            file_list = [path + "/" + file for file in os.listdir(path)]
            for file in os.listdir(path):
                org_dict[path_names[index]].append(path + "/" + file)

        return org_dict
    else:
        print("Have to sepcify sep or sum..")
        
        
def HT_dist(org_files_folder, plot_comparison, multiple = False, random_pick = False):
    HT_list_1 = []
    HT_list_2 = []
    
    file_1, file_2, file_1_path, file_2_path = find_files_for_analysis(org_files_folder, plot_comparison)
    
    max_event_list = []
    for particle_file_1 in file_1:
        if particle_file_1 == file_1_path + "/MET.csv":
            pass
        else:
            file_csv = pd.read_csv(particle_file_1)
            nr_events = max(file_csv["event#"])
            max_event_list.append(nr_events)
    nr_events = max(max_event_list)
    
    event_dict = None
    event_dict = dict.fromkeys(range(nr_events+1)) #from 0 to nr_event-1
    for event in event_dict:
        event_dict[event] = 0
    
    for particle_file_1 in file_1:
        if particle_file_1 == file_1_path + "/MET.csv":
            pass
        else:
            PT_list = file_csv["PT"]
            EVENT_list = file_csv["event#"]
            count = 0
            for pt in PT_list:
                event_dict[EVENT_list[count]] += pt
                count += 1
            
    for event in range(nr_events):
        HT_list_1.append(event_dict[event])
    HT_list_1 = [i for i in HT_list_1 if i != 0]
    
    return HT_list_1







def HT_dist(org_files_folder, plot_comparison, multiple = False, random_pick = False):
    HT_list_1 = []
    HT_list_2 = []
    file_1, file_2, file_1_path, file_2_path = find_files_for_analysis(org_files_folder, plot_comparison)
    
    particle_dict = {
        "electron" : [],
        "jet" : [],
        "muon" : [],
        "photon" : [],
        "tau" : []
    }

    for particle_file_1 in file_1:
        if particle_file_1 == file_1_path + "/MET.csv":
            pass
        else:
            file_name = (particle_file_1.removeprefix(file_1_path + "/")).removesuffix(".csv")
            file_csv = pd.read_csv(particle_file_1)
            for index, row in file_csv.iterrows():
                pt, event = row["PT"], row["event#"]
                particle_dict[file_name].append([event, pt])
                
    # Transpose the lists for particles in dist
    for particle in particle_list:
        try:
            ht_list = particle_dict[particle]
            new_ht_list = list(map(list, zip(*ht_list)))
            particle_dict[particle] = new_ht_list
        except:
            pass
    
    #combining same evnet pt etc...
    for particle in particle_list:
        try:
            ht_list = particle_dict[particle]
            new_ht_list = [[],[]]
            temp_nr_event = None
            temp_pt = 0
            for i in range(ht_list[1]):
                if ht_list[0][i] == temp_nr_event:
                    temp_pt += ht_list[1][i]
                    continue
                else:
                    if temp_pt != 0:
                        new_ht_list[1].append(temp_pt)
                        new_ht_list[0].append(temp_nr_event)
                    temp_nr_event = ht_list[0][i]
                    temp_pt = ht_list[1][i]
            particle_dict[particle] = new_ht_list
        except:
            pass
    
    print(len(particle_dict["jet"][0]))



def HT_dist(org_files_folder, plot_comparison, multiple = False, random_pick = False):
    HT_list = [[], []]
    
    file_1, file_2, file_1_path, file_2_path = find_files_for_analysis(org_files_folder, plot_comparison, multiple, random_pick)
    files = [(file_1, file_1_path), (file_2, file_2_path)]
    
    for i, file_i in enumerate(files):
        nr_events = max(pd.read_csv(file_i[1] + "/MET.csv")["event#"])
        
        event_dict = dict.fromkeys(range(nr_events+1)) #from 0 to nr_event-1
        for event in event_dict:
            event_dict[event] = 0
        
        for particle_file in file_i[0]:
            if particle_file == file_i[1] + "/MET.csv":
                pass
            else:
                file_csv = pd.read_csv(particle_file)
                for index, row in file_csv.iterrows():
                    event_nr = row["event#"]
                    PT = row["PT"]
                    event_dict[event_nr] += PT
                
        for event in range(nr_events):
            HT_list[i].append(event_dict[event]) 
            
    return HT_list[0], HT_list[1]