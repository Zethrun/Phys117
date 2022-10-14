import pandas as pd
import numpy as np
import os


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
                variable_sum[tuple[1]].append(tuple[0])
        elif include_MET == False and stuffs[index] != "MET":
            for tuple in stuff_data:
                variable_sum[tuple[1]].append(tuple[0])

    return list(variable_sum.values())

def event_max(file_data, stuffs, include_MET, by_particle):
    event_num = event_num_finder(file_data, stuffs)
    max_lists = {}
    for i in range(event_num):
        max_lists[i] = []

    for index, stuff_data in enumerate(file_data):
        if include_MET == True:
            for tuple in stuff_data:
                max_lists[tuple[1]].append((tuple[0], tuple[-1]))
        elif include_MET == False and stuffs[index] != "MET":
            for tuple in stuff_data:
                max_lists[tuple[1]].append((tuple[0], tuple[-1]))
    
    max_values = []
    for event_data in list(max_lists.values()):
        if len(event_data) == 0:
            pass
        elif by_particle == True:
            max_value = sorted(event_data, key = lambda x: x[0])[-1]
            max_values.append(max_value)
        else:
            max_value = np.max([tuple[0] for tuple in event_data])
            max_values.append(max_value)

    return max_values

def event_num_finder(file_data, stuffs):
    for stuff_index, stuff_data in enumerate(file_data):
        filename = stuffs[stuff_index]
        if filename == "MET":
            event_num = len(stuff_data)

    return event_num

def by_particle_func(data, include_MET, stuffs):
    particle_counts = {}
    if include_MET == True:
        for stuff in stuffs:
            particle_counts[stuff] = []
        for tuple in data:
            if tuple != 0:
                particle_counts[tuple[-1]].append(tuple[0])
    elif include_MET == False:
        for stuff in stuffs:
            if stuff != "MET":
                particle_counts[stuff] = []
        for tuple in data:
            if tuple != 0:
                particle_counts[tuple[-1]].append(tuple[0])
    
    return list(particle_counts.values())





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
                data_tuple_list = tuple(zip(variable_data, event_num, particle_name))
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
                data_tuple_list = tuple(zip(variable_data, event_num, particle_name))
                data_tuple_list = [data_tuple for data_tuple in data_tuple_list]
                file_data.append(data_tuple_list)
        include_MET = False
        file_data = event_max(file_data, stuffs, include_MET, by_particle)
        folder_data.append(file_data)

    if combine_files:
        folder_data = unpacker(folder_data, [])
    
    return folder_data





