import random
import os

def files(data_path, folders, file_amounts):

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
                file_paths.append(folder_path + file_name)
            folder_file_paths.append(file_paths)
        return folder_file_paths, folder_file_names


    def random_files_selector(file_names, file_amount):
        file_number = len(file_names)
        new_file_names = []
        file_indices = random.sample(range(0, file_number), file_amount)
        for file_index in file_indices:
            plucked_file = file_names[file_index]
            new_file_names.append(plucked_file)
        return new_file_names

    folder_paths = retrieve_folder_paths(data_path)
    folder_file_paths, folder_file_names = retrieve_file_paths(folder_paths, file_amounts)
    return folder_file_paths, folder_file_names