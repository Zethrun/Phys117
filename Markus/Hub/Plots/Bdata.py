import pandas as pd
import numpy as np
import os


def remover(list, to_be_removed):
    list = [element for element in list if element != to_be_removed and type(element) == type(to_be_removed)]
    return list


def unpacker(folder_data, new_folder_data):
    for nested_list in folder_data:
        if type(nested_list) == list:
            unpacker(nested_list, new_folder_data)
        else:
            new_folder_data.append(nested_list)
    folder_data = new_folder_data
    return folder_data


def event_data(file_data, stuffs, include_MET):
    event_num = event_num_finder(file_data, stuffs)
    variable_sum = {}
    for i in range(event_num):
        variable_sum[i] = []

    for index, stuff_data in enumerate(file_data):
        if include_MET == True:
            for tuple in stuff_data:
                variable_sum[tuple[-1]].append(tuple[0])
        elif include_MET == False and stuffs[index] != "MET":
            for tuple in stuff_data:
                variable_sum[tuple[-1]].append(tuple[0])

    return list(variable_sum.values())


def event_max(file_data, stuffs, include_MET, by_particle):
    events_list = events(file_data, stuffs, include_MET, by_particle)

    if by_particle:
        max_values = [sorted(event_data, key = lambda x: x[0])[-1] for event_data in events_list if len(event_data) != 0]
    else:
        max_values = [np.max([tuple[0] for tuple in event_data]) for event_data in events_list if len(event_data) != 0]

    return max_values


def events(file_data, stuffs, include_MET, by_particle):
    event_num = event_num_finder(file_data, stuffs)
    file_data = unpacker(file_data, [])
    temp_stuffs = stuffs if include_MET else remover(stuffs, "MET")
    events_list = {i: [] for i in range(event_num)}
    for tuple in file_data:
        events_list[tuple[-2]].append(tuple) if tuple[-1] in temp_stuffs else None

    return list(events_list.values())


def by_particle_func(file_data, include_MET, stuffs):
    file_data = unpacker(file_data, [])
    temp_stuffs = stuffs if include_MET else remover(stuffs, "MET")
    particle_counts = {stuff: [] for stuff in temp_stuffs}
    for tuple in file_data:
        particle_counts[tuple[-1]].append(tuple[0]) if tuple[-1] in temp_stuffs else None
    return list(particle_counts.values())


def phi_diff_finder(file_data, stuffs):
    new_file_data = []
    for event in file_data:
        if len(event) > 1:
            max_tuple = sorted(event, key = lambda x: x[1])[-1] if sorted(event, key = lambda x: x[1])[-1][-1] != "MET" else sorted(event, key = lambda x: x[1])[-2]
        ang, stuff = max_tuple[0], max_tuple[-1]
        for tuple in event:
            if tuple[-1] == "MET":
                met_ang = tuple[0]
                new_file_data.append(((ang - met_ang) % np.pi, stuff))

    temp_stuffs = remover(stuffs, "MET")
    particle_counts = {stuff: [] for stuff in temp_stuffs}
    for tuple in new_file_data:
        particle_counts[tuple[-1]].append(tuple[0])
    
    return list(particle_counts.values())


def event_num_finder(file_data, stuffs):
    for stuff_index, stuff_data in enumerate(file_data):
        filename = stuffs[stuff_index]
        if filename == "MET":
            event_num = len(stuff_data)

    return event_num





def MET_data(folder, stuffs, data_variable, combine_files):
    folder_data = []
    for file in folder:
        file_data = []
        for stuff_data in file:
            stuff_name = os.path.split(stuff_data)[1]
            if stuff_name[:-len(".csv")] in stuffs:
                data = pd.read_csv(stuff_data)
                variable_data = data[data_variable]
                event_num = data["event#"]
                particle_name = [stuff_name[:-len(".csv")] for i in range(len(event_num))]
                data_tuple_list = tuple(zip(variable_data, event_num, particle_name))
                data_tuple_list = [data_tuple[0] for data_tuple in data_tuple_list]
                file_data.append(data_tuple_list)
        folder_data.append(file_data)

    if combine_files:
        folder_data = unpacker(folder_data, [])
    
    return folder_data
    


def HT_data(folder, stuffs, data_variable, combine_files):
    folder_data = []
    for file in folder:
        file_data = []
        for stuff_data in file:
            stuff_name = os.path.split(stuff_data)[1]
            if stuff_name[:-len(".csv")] in stuffs:
                data = pd.read_csv(stuff_data)
                variable_data = data[data_variable]
                event_num = data["event#"]
                particle_name = [stuff_name[:-len(".csv")] for i in range(len(event_num))]
                data_tuple_list = tuple(zip(variable_data, event_num, particle_name))
                data_tuple_list = [(data_tuple[0], data_tuple[1]) for data_tuple in data_tuple_list]
                file_data.append(data_tuple_list)
        include_MET = False
        file_data = [np.sum(pt_list) for pt_list in event_data(file_data, stuffs, include_MET)]
        folder_data.append(file_data)

    if combine_files:
        folder_data = unpacker(folder_data, [])
    
    return folder_data
         


def stuff_amount_data(folder, stuffs, data_variable, combine_files):
    folder_data = []
    for file in folder:
        file_data = []
        for stuff_data in file:
            stuff_name = os.path.split(stuff_data)[1]
            if stuff_name[:-len(".csv")] in stuffs:
                data = pd.read_csv(stuff_data)
                variable_data = data[data_variable]
                event_num = data["event#"]
                particle_name = [stuff_name[:-len(".csv")] for i in range(len(event_num))]
                data_tuple_list = tuple(zip(variable_data, event_num, particle_name))
                data_tuple_list = [(data_tuple[2], data_tuple[1]) for data_tuple in data_tuple_list]
                file_data.append(data_tuple_list)
        include_MET = False
        file_data = [len(event) for event in event_data(file_data, stuffs, include_MET)]
        folder_data.append(file_data)

    if combine_files:
        folder_data = [stuff_amount for file_data in folder_data for stuff_amount in file_data]

    return folder_data



def stuff_counts_data(folder, stuffs, data_variable, combine_files):
    folder_data = []
    for file in folder:
        file_data = []
        for stuff_data in file:
            stuff_name = os.path.split(stuff_data)[1]
            if stuff_name[:-len(".csv")] in stuffs:
                data = pd.read_csv(stuff_data)
                variable_data = data[data_variable]
                event_num = data["event#"]
                particle_name = [stuff_name[:-len(".csv")] for i in range(len(event_num))]
                data_tuple_list = list(zip(variable_data, event_num, particle_name))
                data_tuple_list = [(data_tuple[2], data_tuple[1]) for data_tuple in data_tuple_list]
                file_data.append(data_tuple_list)
        include_MET = False
        file_data = stuff_counter(event_data(file_data, stuffs, include_MET), stuffs)
        folder_data.append(file_data)

    if combine_files:
        temp_data = [[] for i in range(len(stuffs) - 1)]
        for file_data in folder_data:
            for stuff_index, stuff_counts in enumerate(file_data):
                for count in stuff_counts:
                    temp_data[stuff_index].append(count)
        folder_data = temp_data

    return folder_data

def stuff_counter(file_data, stuffs):
    stuff_counts = {}
    for stuff in stuffs:
        if stuff != "MET":
            stuff_counts[stuff] = []
    for event in file_data:
        for stuff in stuffs:
            if stuff != "MET":
                stuff_count = event.count(stuff)
                stuff_counts[stuff].append(stuff_count)
    return list(stuff_counts.values())



def PT_max_data(folder, stuffs, by_particle, data_variable, combine_files):
    folder_data = []
    for file in folder:
        file_data = []
        for stuff_data in file:
            stuff_name = os.path.split(stuff_data)[1]
            if stuff_name[:-len(".csv")] in stuffs:
                data = pd.read_csv(stuff_data)
                variable_data = data[data_variable]
                event_num = data["event#"]
                particle_name = [stuff_name[:-len(".csv")] for i in range(len(event_num))]
                data_tuple_list = list(zip(variable_data, event_num, particle_name))
                data_tuple_list = [data_tuple for data_tuple in data_tuple_list]
                file_data.append(data_tuple_list)
        include_MET = False
        file_data = event_max(file_data, stuffs, include_MET, by_particle)
        folder_data.append(file_data)

    if combine_files:
        folder_data = unpacker(folder_data, [])
    
    return folder_data


def phi_data(folder, stuffs, by_particle, data_variable, combine_files):
    folder_data = []
    for file in folder:
        file_data = []
        for stuff_data in file:
            stuff_name = os.path.split(stuff_data)[1]
            if stuff_name[:-len(".csv")] in stuffs:
                data = pd.read_csv(stuff_data)
                variable_data = data[data_variable]
                event_num = data["event#"]
                particle_name = [stuff_name[:-len(".csv")] for i in range(len(event_num))]
                data_tuple_list = list(zip(variable_data, event_num, particle_name))
                data_tuple_list = [(data_tuple[0] + 3.142, data_tuple[1], data_tuple[2]) for data_tuple in data_tuple_list]
                file_data.append(data_tuple_list)
        include_MET = True
        file_data = by_particle_func(file_data, include_MET, stuffs) if by_particle else unpacker(file_data, [])
        folder_data.append(file_data)

    if combine_files:
        folder_data = [[unpacker(stuff_data, [])] for stuff_data in list(zip(*folder_data,))] if by_particle else unpacker(folder_data, [])

    return folder_data


def phi_diff_data(folder, stuffs, by_particle, data_variable, combine_files):
    folder_data = []
    for file in folder:
        file_data = []
        for stuff_data in file:
            stuff_name = os.path.split(stuff_data)[1]
            if stuff_name[:-len(".csv")] in stuffs:
                data = pd.read_csv(stuff_data)
                variable_data = data[data_variable]
                pt_data = data["PT"]
                event_num = data["event#"]
                particle_name = [stuff_name[:-len(".csv")] for i in range(len(event_num))]
                data_tuple_list = list(zip(variable_data, pt_data, event_num, particle_name))
                data_tuple_list = [data_tuple for data_tuple in data_tuple_list]
                file_data.append(data_tuple_list)
        include_MET = True
        file_data = phi_diff_finder(events(file_data, stuffs, include_MET, by_particle), stuffs)
        folder_data.append(file_data)

    if combine_files:
        folder_data = [[unpacker(stuff_data, [])] for stuff_data in list(zip(*folder_data,))] if by_particle else unpacker(folder_data, [])
    
    return folder_data



