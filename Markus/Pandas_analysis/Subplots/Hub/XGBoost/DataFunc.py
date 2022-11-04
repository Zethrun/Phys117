import pandas as pd
import os

def remover(old_list, index):
    new_list = [element for element_index, element in enumerate(old_list) if element_index != index]
    return new_list


def unpacker(data_list, new_folder_data):
    for nested_list in data_list:
        if type(nested_list) == list:
            unpacker(nested_list, new_folder_data)
        else:
            new_folder_data.append(nested_list)
    data_list = new_folder_data
    return data_list


def event_categorizer(file_data, stuffs, event_num_index):
    event_num = len(file_data[stuffs.index("MET")])
    events_dict = {event: [] for event in range(event_num)}
    for stuff_data in file_data:
        for particle in stuff_data:
            event_num = particle[event_num_index]
            particle = tuple(remover(list(particle), event_num_index))
            events_dict[event_num].append(particle)
    
    events_data = [tuple(event) for event in list(events_dict.values())]
    return events_data


def data(file, stuffs, data_variables):
    file_data = []
    for stuff_data in file:
        stuff_name = os.path.split(stuff_data)[1]
        if stuff_name[:-len(".csv")] in stuffs:
            data = pd.read_csv(stuff_data)
            variable_data = [data[data_variable] for data_variable in data_variables]
            particle_name = [stuff_name[:-len(".csv")] for i in range(len(variable_data[0]))]
            data_tuple_list = list(zip(particle_name, *variable_data))
            file_data.append(data_tuple_list)
    
    file_data = event_categorizer(file_data, stuffs, event_num_index = 8)
    return file_data
