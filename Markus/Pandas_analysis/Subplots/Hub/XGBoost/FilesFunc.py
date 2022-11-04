import random
import os

def files(individual, data_path, folders, stuffs, file_amounts):
    stuffs = [stuff + ".csv" for stuff in stuffs]

    def retrieve_folder_paths(data_path):
        folder_paths = []
        for folder_name in os.listdir(data_path):
            if folder_name in folders:
                folder_path = data_path + folder_name + "/"
                folder_paths.append(folder_path)
        return folder_paths

    def retrieve_file_paths(folder_paths, file_amounts):
        folder_file_paths = []
        folder_file_names = []
        for folder_index, folder_path in enumerate(folder_paths):
            file_amount = file_amounts[folder_index]
            file_names = random_files_selector(os.listdir(folder_path), file_amount)
            folder_file_names.append(file_names)
            file_paths = []
            for file_name in file_names:
                file_paths.append(folder_path + file_name + "/")
            folder_file_paths.append(file_paths)
        return folder_file_paths, folder_file_names
    
    def retrieve_file_data_paths(folder_file_paths):
        data_folders = [] 
        for file_paths in folder_file_paths:
            data_folder = []
            for file_path in file_paths:
                data_files = []
                for stuff_data in os.listdir(file_path):
                    if stuff_data in stuffs:
                        data_files.append(file_path + stuff_data)
                data_folder.append(data_files)
            data_folders.append(data_folder)
        return data_folders

    def random_files_selector(file_names, file_amount):
        file_number = len(file_names)
        new_file_names = []
        file_indices = random.sample(range(0, file_number), file_amount)
        for file_index in file_indices:
            plucked_file = file_names[file_index]
            new_file_names.append(plucked_file)
        return new_file_names
    
    if individual:
        folder_paths = retrieve_folder_paths(data_path)
        folder_file_paths, folder_file_names = retrieve_file_paths(folder_paths, file_amounts)
        data_folders = retrieve_file_data_paths(folder_file_paths)
        return data_folders, folder_file_names
    else:
        folder_paths = retrieve_folder_paths(data_path)
        folder_file_paths, folder_file_names = retrieve_file_paths(folder_paths, file_amounts)
        return folder_file_paths, folder_file_names