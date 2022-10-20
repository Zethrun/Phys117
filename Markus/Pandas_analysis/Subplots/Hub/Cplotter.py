import matplotlib.pyplot as plt
import numpy as np


def unpacker(folder_data, new_folder_data):
    for nested_list in folder_data:
        if type(nested_list) == list:
            unpacker(nested_list, new_folder_data)
        else:
            new_folder_data.append(nested_list)
    folder_data = new_folder_data
    return folder_data


def tuple_unpacker(folder_data, new_folder_data):
    for nested_list in folder_data:
        if type(nested_list) == list or type(nested_list) == tuple:
            tuple_unpacker(nested_list, new_folder_data)
        else:
            new_folder_data.append(nested_list)
    folder_data = new_folder_data
    return folder_data


def binfinder(plot_data, binsize):
    data = unpacker(plot_data, [])
    max_value = np.max(data)
    bins = int(np.round(max_value / binsize))
    return bins
    

def data_binner(data, binsize, plot):
    data = [data for data in tuple_unpacker(data, []) if type(data) != str]

    if len(data) == 0:
        x = [bin * binsize for bin in range(200)]
        y = [0 for bin in range(200)]
        return x, y

    max_value = np.max(data)
    bins = int(np.round(max_value / binsize))
    bins = np.arange(0, bins)
    data = np.array(data)
    x, y = [], []

    if plot == True:
        for bin in range(len(bins)):
            temp = data
            temp = temp[temp <= (bin + 1/2)*binsize]
            temp = temp[(bin - 1/2)*binsize < temp]
            if len(temp) != 0:
                y.append(len(temp))
                x.append(bin*binsize)

        y = y/np.sum(y)

        return x, y

    else:
        for bin in range(len(bins)):
            temp = data
            temp = temp[temp <= (bin + 1/2)*binsize]
            temp = temp[(bin - 1/2)*binsize < temp]
            y.append(len(temp))
            x.append(bin*binsize)

        y = y/np.sum(y)

        return x, y
 

def plot_filter(interval_data, filter_strength):
    interval_data = sorted([data for data in tuple_unpacker(interval_data, []) if type(data) != str])
    cutoff = round((len(interval_data) * filter_strength))
    interval_data = interval_data[:cutoff]
    x_min = np.min(interval_data)
    x_max = np.max(interval_data)
    extra = (x_max - x_min) / 10
    return [x_min - extra, x_max + extra]


def efficiency_value(subplots, data, xlabel, folders, binsize, interval_data, filter_strength):
    bh_data, sphal_data = data
    bh_data = [data for data in tuple_unpacker(bh_data, []) if type(data) != str]
    sphal_data = [data for data in tuple_unpacker(sphal_data, []) if type(data) != str]
    x_bh, y_bh = data_binner(bh_data, binsize, plot = False)
    x_sphal, y_sphal = data_binner(sphal_data, binsize, plot = False)
    x_interval = np.concatenate((x_bh, x_sphal))
    x_min, x_max = np.min(x_interval), np.max(x_interval)
    bins = int(np.round((x_max - x_min)/binsize))
    efficiencies = [[[], []] for i in range(len(["left", "right"]))]
    x = [x_min + (bin + 1)*binsize for bin in range(bins + 1)]
    total_efficiencies = []

    for bin in range(bins + 1):
        bh_left = y_bh[:bin + 1]
        bh_right = y_bh[bin + 1:]
        bh_split = [bh_left, bh_right]
        
        sphal_left = y_sphal[:bin + 1]
        sphal_right = y_sphal[bin + 1:]
        sphal_split = [sphal_right, sphal_left]

        temp_efficiency = []
        for i in range(len(["left", "right"])):
            bh_efficiency = np.sum(bh_split[i])
            efficiencies[i][0].append(bh_efficiency)
            sphal_efficiency = np.sum(sphal_split[i])
            efficiencies[i][1].append(sphal_efficiency)
            total_efficiency = bh_efficiency + sphal_efficiency
            temp_efficiency.append(total_efficiency)

        total_efficiencies.append((np.max(temp_efficiency), bin))
    
    max_efficiency = sorted(total_efficiencies, key = lambda x: x[0])[-1]
    me_value = max_efficiency[0] / 2
    me_bin = max_efficiency[1]
    me_x = x_min + me_bin * binsize
    
    for side_index, side in enumerate(efficiencies):
        subplot = subplots[side_index + 1]
        subplot.axvline(me_x, label = "max efficiency is " + str(int(np.round(me_value * 100)) / 100) + " at " + str(int(np.round(me_x * 100)) / 100))
        subplot.set_xlabel(xlabel)
        subplot.set_ylabel("Relative Efficiencies")
        for folder_index, folder in enumerate(side):
            sides = ["left", "right"] if side_index == 0 else ["right", "left"]
            label = "efficiencies for " + folders[folder_index] + " to the " + sides[folder_index]
            subplot.plot(x, folder, label = label)
        x_interval = plot_filter(interval_data, filter_strength)
        subplot.set_xlim(x_interval)
        subplot.legend(prop = {'size': 8}, loc = "upper right")


def MET_dist(folders_data, folders, filename_list, stuffs, binsize, filter_strength, xlabel, combine_files, efficiencies_plot):
    fig = plt.figure()
    style = "seaborn-darkgrid"
    plt.style.use(style)
    title = "MET Distribution"
    fig.suptitle(title)

    if efficiencies_plot:
        subplots = fig.subplots(1, 3)
        efficiency_data = []
        data_subplot = subplots[0]
    else:
        data_subplot = fig.subplots(1, 1)

    data_subplot.set_xlabel(xlabel)
    data_subplot.set_ylabel("Frequency of Events")
    interval_data = unpacker(folders_data, [])
    x_interval = plot_filter(interval_data, filter_strength)
    data_subplot.set_xlim(x_interval)

    for folder_index, folder_data in enumerate(folders_data):

        if combine_files:
            plot_data = folder_data
            efficiency_data.append(plot_data) if efficiencies_plot else None
            x, y = data_binner(plot_data, binsize, plot = True)
            labels = folders
            label = labels[folder_index]
            data_subplot.plot(x, y, label = label)
        else:
            labels = filename_list[folder_index]
            for file_index, file_data in enumerate(folder_data):
                plot_data = file_data
                efficiency_data.append(plot_data) if efficiencies_plot else None
                x, y = data_binner(plot_data, binsize, plot = True)
                label = labels[file_index]
                data_subplot.plot(x, y, label = label)

    if efficiencies_plot:
        efficiency_value(subplots, efficiency_data, xlabel, folders, binsize, interval_data, filter_strength)
    data_subplot.legend(prop = {'size': 8})
    plt.show()


def HT_dist_plot(folders_data, folders, filename_list, stuffs, binsize, filter_strength, xlabel, combine_files, efficiencies_plot):
    fig = plt.figure()
    style = "seaborn-darkgrid"
    plt.style.use(style)
    title = "HT Distribution"
    fig.suptitle(title)

    if efficiencies_plot:
        subplots = fig.subplots(1, 3)
        efficiency_data = []
        data_subplot = subplots[0]
    else:
        data_subplot = fig.subplots(1, 1)

    data_subplot.set_xlabel(xlabel)
    data_subplot.set_ylabel("Frequency of Events")
    interval_data = unpacker(folders_data, [])
    x_interval = plot_filter(interval_data, filter_strength)
    data_subplot.set_xlim(x_interval)

    for folder_index, folder_data in enumerate(folders_data):
        if combine_files:
            plot_data = folder_data
            efficiency_data.append(plot_data) if efficiencies_plot else None
            x, y = data_binner(plot_data, binsize, plot = True)
            labels = folders
            label = labels[folder_index]
            data_subplot.plot(x, y, label = label)
        else:
            labels = filename_list[folder_index]
            for file_index, file_data in enumerate(folder_data):
                plot_data = file_data
                efficiency_data.append(plot_data) if efficiencies_plot else None
                x, y = data_binner(plot_data, binsize, plot = True)
                label = labels[file_index]
                data_subplot.plot(x, y, label = label)
    
    if efficiencies_plot:
        efficiency_value(subplots, efficiency_data, xlabel, folders, binsize, interval_data, filter_strength)
    data_subplot.legend(prop = {'size': 8})
    plt.show()


def stuff_amount_plot(folders_data, folders, filename_list, stuffs, binsize, filter_strength, xlabel, combine_files, efficiencies_plot):
    fig = plt.figure()
    style = "seaborn-darkgrid"
    plt.style.use(style)
    title = "Total Particle Type Distribution"
    fig.suptitle(title)

    if efficiencies_plot:
        subplots = fig.subplots(1, 3)
        efficiency_data = []
        data_subplot = subplots[0]
    else:
        data_subplot = fig.subplots(1, 1)

    data_subplot.set_xlabel(xlabel)
    data_subplot.set_ylabel("Frequency of Events")
    interval_data = unpacker(folders_data, [])
    x_interval = plot_filter(interval_data, filter_strength)
    data_subplot.set_xlim(x_interval)
    
    for folder_index, folder_data in enumerate(folders_data):
        if combine_files:
            plot_data = unpacker(folder_data, [])
            efficiency_data.append(plot_data) if efficiencies_plot else None
            x, y = data_binner(plot_data, binsize, plot = True)
            labels = folders
            label = labels[folder_index]
            data_subplot.plot(x, y, alpha = 0.75, label = label)
        else:
            labels = filename_list[folder_index]
            for file_index, file_data in enumerate(folder_data):
                plot_data = unpacker(file_data, [])
                efficiency_data.append(plot_data) if efficiencies_plot else None
                x, y = data_binner(plot_data, binsize, plot = True)
                label = labels[file_index]
                data_subplot.plot(x, y, alpha = 0.75, label = label)

    if efficiencies_plot:
        efficiency_value(subplots, efficiency_data, xlabel, folders, binsize, interval_data, filter_strength)
    data_subplot.legend(prop = {'size': 8})    
    plt.show()


def stuff_counts_plot(folders_data, folders, filename_list, stuffs, binsize, filter_strength, xlabel, combine_files, efficiencies_plot):
    fig = plt.figure()
    style = "seaborn-darkgrid"
    plt.style.use(style)
    subfigs_y = fig.subfigures(2, 1)
    subfigs_1 = subfigs_y[0].subfigures(1, 2)
    subfigs_2 = subfigs_y[1].subfigures(1, 3)
    subfigs = [*subfigs_1, *subfigs_2]
    stuffs = [stuff for stuff in stuffs if stuff != "MET"]

    for stuff_index, stuff in enumerate(stuffs):
        subfig = subfigs[stuff_index]
        title = "Particle Type Distribution for " + stuff
        subfig.suptitle(title)

        if efficiencies_plot:
            subplots = subfig.subplots(1, 3)
            efficiency_data = []
            data_subplot = subplots[0]
        else:
            data_subplot = subfig.subplots(1, 1)

        data_subplot.set_xlabel(xlabel)
        data_subplot.set_ylabel("Frequency of Events")
        interval_data = unpacker(folders_data, [])
        x_interval = plot_filter(interval_data, filter_strength)
        data_subplot.set_xlim(x_interval)

        for folder_index, folder_data in enumerate(folders_data):
            if combine_files:
                plot_data = unpacker(folder_data[stuff_index], [])
                efficiency_data.append(plot_data) if efficiencies_plot else None
                x, y = data_binner(plot_data, binsize, plot = True)
                labels = folders
                label = labels[folder_index]
                data_subplot.plot(x, y, alpha = 0.75, label = label)
            else:
                labels = filename_list[folder_index]
                for file_index, file_data in enumerate(folder_data):
                    plot_data = file_data[stuff_index]
                    efficiency_data.append(plot_data) if efficiencies_plot else None
                    x, y = data_binner(plot_data, binsize, plot = True)
                    label = labels[file_index]
                    data_subplot.plot(x, y, alpha = 0.75, label = label)
        
        if efficiencies_plot:
            efficiency_value(subplots, efficiency_data, xlabel, folders, binsize, interval_data, filter_strength)
        data_subplot.legend(prop = {'size': 8})
    plt.show()
    
    
def PT_max_plot(folders_data, folders, filename_list, stuffs, by_particle, binsize, filter_strength, xlabel, combine_files, efficiencies_plot):
    fig = plt.figure()
    style = "seaborn-darkgrid"
    plt.style.use(style)
    stuffs = [stuff for stuff in stuffs if stuff != "MET"]
    
    if by_particle:
        subfigs_y = fig.subfigures(2, 1)
        subfigs_1 = subfigs_y[0].subfigures(1, 2)
        subfigs_2 = subfigs_y[1].subfigures(1, 3)
        subfigs = [*subfigs_1, *subfigs_2]

        for stuff_index, stuff in enumerate(stuffs):
            subfig = subfigs[stuff_index]
            title = "Maximum PT per event for " + stuff + "s"
            subfig.suptitle(title)

            if efficiencies_plot:
                subplots = subfig.subplots(1, 3)
                efficiency_data = []
                data_subplot = subplots[0]
            else:
                data_subplot = subfig.subplots(1, 1)

            data_subplot.set_xlabel(xlabel)
            data_subplot.set_ylabel("Frequency of Events")
            interval_data = [event_data[0] for event_data in unpacker(folders_data, []) if event_data[-1] == stuff]
            x_interval = plot_filter(interval_data, filter_strength)
            data_subplot.set_xlim(x_interval)

            for folder_index, folder_data in enumerate(folders_data):
                if combine_files:
                    plot_data = [event_data[0] for event_data in folder_data if event_data[-1] == stuff]
                    efficiency_data.append(plot_data) if efficiencies_plot else None
                    x, y = data_binner(plot_data, binsize, plot = True)
                    labels = folders
                    label = labels[folder_index]
                    data_subplot.plot(x, y, alpha = 0.75, label = label)
                else:
                    for file_index, file_data in enumerate(folder_data):
                        plot_data = [event_data[0] for event_data in file_data if event_data[-1] == stuff]
                        efficiency_data.append(plot_data) if efficiencies_plot else None
                        x, y = data_binner(plot_data, binsize, plot = True)
                        labels = filename_list[folder_index]
                        label = labels[file_index]
                        data_subplot.plot(x, y, alpha = 0.75, label = label)
            
            if efficiencies_plot:
                efficiency_value(subplots, efficiency_data, xlabel, folders, binsize, interval_data, filter_strength)
            data_subplot.legend(prop = {'size': 8})
    else:
        title = "Maximum Measured PT Distribution per event"
        fig.suptitle(title)

        if efficiencies_plot:
            subplots = fig.subplots(1, 3)
            efficiency_data = []
            data_subplot = subplots[0]
        else:
            data_subplot = fig.subplots(1, 1)

        data_subplot.set_xlabel(xlabel)
        data_subplot.set_ylabel("Frequency of Events")
        interval_data = unpacker(folders_data, [])
        x_interval = plot_filter(interval_data, filter_strength)
        data_subplot.set_xlim(x_interval)
        
        for folder_index, folder_data in enumerate(folders_data):
            if combine_files:
                plot_data = unpacker(folder_data, [])
                efficiency_data.append(plot_data) if efficiencies_plot else None
                x, y = data_binner(plot_data, binsize, plot = True)
                labels = folders
                label = labels[folder_index]
                data_subplot.plot(x, y, alpha = 0.75, label = label)
            else:
                labels = filename_list[folder_index]
                for file_index, file_data in enumerate(folder_data):
                    plot_data = file_data
                    efficiency_data.append(plot_data) if efficiencies_plot else None
                    x, y = data_binner(plot_data, binsize, plot = True)
                    label = labels[file_index]
                    data_subplot.plot(x, y, alpha = 0.75, label = label)

        if efficiencies_plot:    
            efficiency_value(subplots, efficiency_data, xlabel, folders, binsize, interval_data, filter_strength)
        data_subplot.legend(prop = {'size': 8})

    plt.show()
    

def phi_plot(folders_data, folders, filename_list, stuffs, binsize, filter_strength, xlabel, combine_files, efficiencies_plot):
    stuffs = [stuff for stuff in stuffs if stuff != "MET"]
    for stuff_index, stuff in enumerate(stuffs):
        subfig = plt.figure()
        style = "seaborn-darkgrid"
        plt.style.use(style)
        title = "Phi Distribution for " + stuff + "s"
        subfig.suptitle(title)

        if efficiencies_plot:
            subplots = subfig.subplots(1, 3)
            efficiency_data = []
            data_subplot = subplots[0]
        else:
            data_subplot = subfig.subplots(1, 1)

        data_subplot.set_xlabel(xlabel)
        data_subplot.set_ylabel("Frequency of Events")
        interval_data = unpacker(folders_data, [])
        x_interval = plot_filter(interval_data, filter_strength)
        data_subplot.set_xlim(x_interval)

        for folder_index, folder_data in enumerate(folders_data):
            if combine_files:
                plot_data = folder_data[stuff_index]
                efficiency_data.append(plot_data) if efficiencies_plot else None
                x, y = data_binner(plot_data, binsize, plot = True)
                labels = folders
                label = labels[folder_index]
                data_subplot.plot(x, y, alpha = 0.75, label = label)
            else:
                labels = filename_list[folder_index]
                for file_index, file_data in enumerate(folder_data):
                    plot_data = file_data[stuff_index]
                    efficiency_data.append(plot_data) if efficiencies_plot else None
                    x, y = data_binner(plot_data, binsize, plot = True)
                    label = labels[file_index]
                    data_subplot.plot(x, y, alpha = 0.75, label = label)

        if efficiencies_plot:
            efficiency_value(subplots, efficiency_data, xlabel, folders, binsize, interval_data, filter_strength)
        data_subplot.legend(prop = {'size': 8})
        plt.show()

    
def phi_diff_plot(folders_data, folders, filename_list, stuffs, binsize, filter_strength, xlabel, combine_files, efficiencies_plot):
    stuffs = [stuff for stuff in stuffs if stuff != "MET"]
    for stuff_index, stuff in enumerate(stuffs):
        subfig = plt.figure()
        style = "seaborn-darkgrid"
        plt.style.use(style)
        title = "Phi Between Biggest PT and MET for " + stuff + "s"
        subfig.suptitle(title)

        if efficiencies_plot:
            subplots = subfig.subplots(1, 3)
            efficiency_data = []
            data_subplot = subplots[0]
        else:
            data_subplot = subfig.subplots(1, 1)

        data_subplot.set_xlabel(xlabel)
        data_subplot.set_ylabel("Frequency of Events")
        interval_data = unpacker(folders_data, [])
        x_interval = plot_filter(interval_data, filter_strength)
        data_subplot.set_xlim(x_interval)

        for folder_index, folder_data in enumerate(folders_data):
            if combine_files:
                plot_data = folder_data[stuff_index]
                efficiency_data.append(plot_data) if efficiencies_plot else None
                x, y = data_binner(plot_data, binsize, plot = True)
                labels = folders
                label = labels[folder_index]
                data_subplot.plot(x, y, alpha = 0.75, label = label)
            else:
                labels = filename_list[folder_index]
                for file_index, file_data in enumerate(folder_data):
                    plot_data = file_data[stuff_index]
                    efficiency_data.append(plot_data) if efficiencies_plot else None
                    x, y = data_binner(plot_data, binsize, plot = True)
                    label = labels[file_index]
                    data_subplot.plot(x, y, alpha = 0.75, label = label)

        if efficiencies_plot:
            efficiency_value(subplots, efficiency_data, xlabel, folders, binsize, interval_data, filter_strength)
        data_subplot.legend(prop = {'size': 8})
        plt.show()
























