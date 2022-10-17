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


def binfinder(plot_data, binsize):
    data = unpacker(plot_data, [])
    max_value = np.max(data)
    bins = int(np.round(max_value / binsize))
    return bins
    

def data_binner(data, binsize, plot):
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


def plot_filter(interval_data, filter_strengths):
    variable_data = np.array(interval_data)
    mean = np.mean(variable_data)
    std_dev = np.std(variable_data)
    x_limit_min = mean - filter_strengths[0]*std_dev
    x_limit_max = mean + filter_strengths[1]*std_dev
    if np.min(interval_data) >= 0 and x_limit_min <=0:
        x_limit_min = 0
    if np.max(interval_data) <= x_limit_max:
        x_limit_max = np.max(interval_data)
    return [x_limit_min, x_limit_max]


def efficiency_value(data, binsize):
    bh_data, sphal_data = data
    x_bh, y_bh = data_binner(bh_data, binsize, plot = False)
    x_sphal, y_sphal = data_binner(sphal_data, binsize, plot = False)
    x_interval = np.concatenate((x_bh, x_sphal))
    x_min, x_max = np.min(x_interval), np.max(x_interval)
    bins = int(np.round((x_max - x_min)/binsize))
    efficiencies = [[[], []] for i in range(len(["left", "right"]))]
    x = [x_min + (bin + 1)*binsize for bin in range(bins + 1)]

    for bin in range(bins + 1):
        sphal_left = y_sphal[:bin + 1]
        sphal_right = y_sphal[bin + 1:]
        sphal_split = [sphal_left, sphal_right]

        bh_left = y_bh[:bin + 1]
        bh_right = y_bh[bin + 1:]
        bh_split = [bh_left, bh_right]

        for i in range(len(["left", "right"])):
            sphal_efficiency = np.sum(sphal_split[i])/2
            efficiencies[i][0].append(sphal_efficiency)
            bh_efficiency = np.sum(bh_split[i])/2
            efficiencies[i][1].append(bh_efficiency)

    return x, efficiencies


def MET_dist(folders_data, folders, filename_list, stuffs, binsize, filter_strengths, xlabel, compare, combine_files, efficiencies_plot):
    fig = plt.figure()
    style = "seaborn-darkgrid"
    plt.style.use(style)

    if compare:
        if efficiencies_plot:
            subplots = fig.subplots(1, 2)
            data_subplot = subplots[0]
            efficiencies_subplot = subplots[1]
            efficiencies_subplot.set_xlabel(xlabel)
            efficiencies_subplot.set_ylabel("Relative Efficiencies")
            title = "Maximum Measured PT Distribution per event"
            efficiencies_subplot.set_title(title)
        else:
            data_subplot = fig.subplots(1, 1)
        data_subplot.set_xlabel(xlabel)
        data_subplot.set_ylabel("Frequency of Events")
        title = "Maximum Measured PT Distribution per event"
        data_subplot.set_title(title)
        interval_data = unpacker(folders_data, [])
        x_interval = plot_filter(interval_data, filter_strengths)
        data_subplot.set_xlim(x_interval)

        for folder_index, folder_data in enumerate(folders_data):
            if combine_files:
                data = folder_data
                x, y = data_binner(data, binsize, plot = True)
                labels = folders
                label = labels[folder_index]
                data_subplot.plot(x, y, label = label)
            else:
                labels = filename_list[folder_index]
                for data_index, data in enumerate(folder_data):
                    x, y = data_binner(data, binsize, plot = True)
                    label = labels[data_index]
                    data_subplot.plot(x, y, label = label)
        if efficiencies_plot:
            x, efficiencies = efficiency_value(folders_data, binsize)
            sides = ["left", "right"]
            for side_index, side in enumerate(efficiencies):
                for folder_index, folder in enumerate(side):
                    label = "efficiencies for " + folders[folder_index] + " to the " + sides[side_index]
                    efficiencies_subplot.plot(x, folder, label = label)
            x_interval = plot_filter(interval_data, filter_strengths)
            efficiencies_subplot.set_xlim(x_interval)
            efficiencies_subplot.legend(prop = {'size': 8}, loc = "upper right")
        data_subplot.legend(prop = {'size': 8})
    else:
        subfigs = fig.subfigures(1, len(folders_data))
        titles = folders
        for folder_index, folder_data in enumerate(folders_data):
            subfig = subfigs[folder_index]
            data_subplot = subfig.subplots(1, 1)
            title = titles[folder_index]
            data_subplot.set_title(title)
            data_subplot.set_xlabel(xlabel)
            data_subplot.set_ylabel("Frequency of Events")
            interval_data = unpacker(folders_data, [])
            x_interval = plot_filter(interval_data, filter_strengths)
            data_subplot.set_xlim(x_interval)
            if combine_files:
                data = folder_data
                x, y = data_binner(data, binsize, plot = True)
                labels = folders
                label = labels[folder_index]
                data_subplot.plot(x, y, label = label)
            else:
                labels = filename_list[folder_index]
                for data_index, data in enumerate(folder_data):
                    x, y = data_binner(data, binsize, plot = True)
                    label = labels[data_index]
                    data_subplot.plot(x, y, label = label)
            data_subplot.legend(prop = {'size': 8})

    plt.show()


def HT_dist(folders_data, folders, filename_list, stuffs, binsize, filter_strengths, xlabel, compare, combine_files, efficiencies_plot):
    fig = plt.figure()
    style = "seaborn-darkgrid"
    plt.style.use(style)

    if compare:
        if efficiencies_plot:
            subplots = fig.subplots(1, 2)
            data_subplot = subplots[0]
            efficiencies_subplot = subplots[1]
            efficiencies_subplot.set_xlabel(xlabel)
            efficiencies_subplot.set_ylabel("Relative Efficiencies")
            title = "Maximum Measured PT Distribution per event"
            efficiencies_subplot.set_title(title)
        else:
            data_subplot = fig.subplots(1, 1)
        data_subplot.set_xlabel(xlabel)
        data_subplot.set_ylabel("Frequency of Events")
        title = "Maximum Measured PT Distribution per event"
        data_subplot.set_title(title)
        interval_data = unpacker(folders_data, [])
        x_interval = plot_filter(interval_data, filter_strengths)
        data_subplot.set_xlim(x_interval)

        for folder_index, folder_data in enumerate(folders_data):
            if combine_files:
                data = folder_data
                x, y = data_binner(data, binsize, plot = True)
                labels = folders
                label = labels[folder_index]
                data_subplot.plot(x, y, label = label)
            else:
                labels = filename_list[folder_index]
                for data_index, data in enumerate(folder_data):
                    x, y = data_binner(data, binsize, plot = True)
                    label = labels[data_index]
                    data_subplot.plot(x, y, label = label)
        if efficiencies_plot:
            x, efficiencies = efficiency_value(folders_data, binsize)
            sides = ["left", "right"]
            for side_index, side in enumerate(efficiencies):
                for folder_index, folder in enumerate(side):
                    label = "efficiencies for " + folders[folder_index] + " to the " + sides[side_index]
                    efficiencies_subplot.plot(x, folder, label = label)
            x_interval = plot_filter(interval_data, filter_strengths)
            efficiencies_subplot.set_xlim(x_interval)
            efficiencies_subplot.legend(prop = {'size': 8}, loc = "upper right")
        data_subplot.legend(prop = {'size': 8})
    else:
        subfigs = fig.subfigures(1, len(folders_data))
        titles = folders
        for folder_index, folder_data in enumerate(folders_data):
            subfig = subfigs[folder_index]
            data_subplot = subfig.subplots(1, 1)
            title = titles[folder_index]
            data_subplot.set_title(title)
            data_subplot.set_xlabel(xlabel)
            data_subplot.set_ylabel("Frequency of Events")
            interval_data = unpacker(folders_data, [])
            x_interval = plot_filter(interval_data, filter_strengths)
            data_subplot.set_xlim(x_interval)
            if combine_files:
                data = folder_data
                x, y = data_binner(data, binsize, plot = True)
                labels = folders
                label = labels[folder_index]
                data_subplot.plot(x, y, label = label)
            else:
                labels = filename_list[folder_index]
                for data_index, data in enumerate(folder_data):
                    x, y = data_binner(data, binsize, plot = True)
                    label = labels[data_index]
                    data_subplot.plot(x, y, label = label)
            data_subplot.legend(prop = {'size': 8})

    plt.show()


def stuff_amount_plot(folders_data, folders, filename_list, stuffs, binsize, filter_strengths, xlabel, compare, combine_files, efficiencies_plot):
    fig = plt.figure()
    style = "seaborn-darkgrid"
    plt.style.use(style)
    if efficiencies_plot:
        subplots = fig.subplots(1, 2)
        data_subplot = subplots[0]
        efficiencies_subplot = subplots[1]
        efficiencies_subplot.set_xlabel(xlabel)
        efficiencies_subplot.set_ylabel("Relative Efficiencies")
        title = "Maximum Measured PT Distribution per event"
        efficiencies_subplot.set_title(title)
    else:
        data_subplot = fig.subplots(1, 1)
    data_subplot.set_xlabel(xlabel)
    data_subplot.set_ylabel("Frequency of Events")
    title = "Maximum Measured PT Distribution per event"
    data_subplot.set_title(title)
    interval_data = unpacker(folders_data, [])
    x_interval = plot_filter(interval_data, filter_strengths)
    data_subplot.set_xlim(x_interval)
    bins = binfinder(folders_data, binsize)
    
    if combine_files:
        amount_data = [unpacker(folder_data, []) for folder_data in folders_data]
        labels = folders
        data_subplot.hist(amount_data, bins = bins, alpha = 0.75, label = labels, density = True)
        if efficiencies_plot:
            x, efficiencies = efficiency_value(folders_data, binsize)
            sides = ["left", "right"]
            for side_index, side in enumerate(efficiencies):
                for folder_index, folder in enumerate(side):
                    label = "efficiencies for " + folders[folder_index] + " to the " + sides[side_index]
                    efficiencies_subplot.plot(x, folder, label = label)
            x_interval = plot_filter(interval_data, filter_strengths)
            efficiencies_subplot.set_xlim(x_interval)
            efficiencies_subplot.legend(prop = {'size': 8}, loc = "upper right")
        
    else:
        for folder_index, folder_data in enumerate(folders_data):
            labels = filename_list[folder_index]
            for file_index, file_data in enumerate(folder_data):
                amount_data = file_data
                label = labels[file_index]
                data_subplot.hist(amount_data, bins = bins, alpha = 0.75, label = label, density = True)
        if efficiencies_plot:
            x, efficiencies = efficiency_value(folders_data, binsize)
            sides = ["left", "right"]
            for side_index, side in enumerate(efficiencies):
                for folder_index, folder in enumerate(side):
                    label = "efficiencies for " + folders[folder_index] + " to the " + sides[side_index]
                    efficiencies_subplot.plot(x, folder, label = label)
            x_interval = plot_filter(interval_data, filter_strengths)
            efficiencies_subplot.set_xlim(x_interval)
            efficiencies_subplot.legend(prop = {'size': 8}, loc = "upper right")

    data_subplot.legend(prop = {'size': 8})    
    plt.show()


def stuff_counts_plot(folders_data, folders, filename_list, stuffs, binsize, filter_strengths, xlabel, compare, combine_files, efficiencies_plot):
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
        if efficiencies_plot:
            subplots = subfig.subplots(1, 2)
            data_subplot = subplots[0]
            efficiencies_subplot = subplots[1]
            efficiencies_subplot.set_xlabel(xlabel)
            efficiencies_subplot.set_ylabel("Relative Efficiencies")
            title = "Maximum Measured PT Distribution per event"
            efficiencies_subplot.set_title(title)
        else:
            data_subplot = subfig.subplots(1, 1)
        data_subplot.set_xlabel(xlabel)
        data_subplot.set_ylabel("Frequency of Events")
        title = "Maximum Measured PT Distribution per event"
        data_subplot.set_title(title)
        interval_data = unpacker(folders_data, [])
        x_interval = plot_filter(interval_data, filter_strengths)
        data_subplot.set_xlim(x_interval)
        bins = binfinder(folders_data, binsize)

        if combine_files:
            plot_data = [unpacker(folder_data[stuff_index], []) for folder_data in folders_data]
            labels = folders
            data_subplot.hist(plot_data, bins = bins, alpha = 0.75, label = labels, density = True)
            if efficiencies_plot:
                x, efficiencies = efficiency_value(folders_data, binsize)
                sides = ["left", "right"]
                for side_index, side in enumerate(efficiencies):
                    for folder_index, folder in enumerate(side):
                        label = "efficiencies for " + folders[folder_index] + " to the " + sides[side_index]
                        efficiencies_subplot.plot(x, folder, label = label)
                x_interval = plot_filter(interval_data, filter_strengths)
                efficiencies_subplot.set_xlim(x_interval)
                efficiencies_subplot.legend(prop = {'size': 8}, loc = "upper right")
        else:
            for folder_index, folder_data in enumerate(folders_data):
                labels = filename_list[folder_index]
                for file_index, file_data in enumerate(folder_data):
                    for count_index, count_data in enumerate(file_data):
                        if count_index == stuff_index:
                            label = labels[file_index]
                            data_subplot.hist(count_data, bins = bins, alpha = 0.75, label = label, density = True)
            if efficiencies_plot:
                x, efficiencies = efficiency_value(folders_data, binsize)
                sides = ["left", "right"]
                for side_index, side in enumerate(efficiencies):
                    for folder_index, folder in enumerate(side):
                        label = "efficiencies for " + folders[folder_index] + " to the " + sides[side_index]
                        efficiencies_subplot.plot(x, folder, label = label)
                x_interval = plot_filter(interval_data, filter_strengths)
                efficiencies_subplot.set_xlim(x_interval)
                efficiencies_subplot.legend(prop = {'size': 8}, loc = "upper right")
        data_subplot.legend(prop = {'size': 8})
    plt.show()
    
    
def PT_max_plot(folders_data, folders, filename_list, stuffs, by_particle, binsize, filter_strengths, xlabel, compare, combine_files, efficiencies_plot):
    fig = plt.figure()
    style = "seaborn-darkgrid"
    plt.style.use(style)
    stuffs = [stuff for stuff in stuffs if stuff != "MET"]
    
    if by_particle:
        subfigs_y = fig.subfigures(2, 1)
        subfigs_1 = subfigs_y[0].subfigures(1, 2)
        subfigs_2 = subfigs_y[1].subfigures(1, 3)
        subfigs = [*subfigs_1, *subfigs_2]
    else:
        fig = fig
    
    if by_particle:
        for stuff_index, stuff in enumerate(stuffs):
            subfig = subfigs[stuff_index]
            if efficiencies_plot:
                subplots = subfig.subplots(1, 2)
                data_subplot = subplots[0]
                efficiencies_subplot = subplots[1]
                efficiencies_subplot.set_xlabel(xlabel)
                efficiencies_subplot.set_ylabel("Relative Efficiencies")
                title = "Maximum Measured PT Distribution per event"
                efficiencies_subplot.set_title(title)
            else:
                data_subplot = subfig.subplots(1, 1)
            data_subplot.set_xlabel(xlabel)
            data_subplot.set_ylabel("Frequency of Events")
            title = "Maximum Measured PT Distribution per event"
            data_subplot.set_title(title)
            interval_data = unpacker(folders_data, [])
            x_interval = plot_filter(interval_data, filter_strengths)
            data_subplot.set_xlim(x_interval)
            bin_data = [unpacker(folder_data, []) for folder_data in folders_data]
            bin_data = [event_data[0] for folder_data in bin_data for event_data in folder_data if event_data[-1] == stuff]
            bins = binfinder(bin_data, binsize)
            
            if combine_files:
                plot_data = [unpacker(folder_data, []) for folder_data in folders_data]
                plot_data = [[event_data[0] for event_data in folder_data if event_data[-1] == stuff] for folder_data in plot_data]
                labels = folders
                data_subplot.hist(plot_data, bins = bins, alpha = 0.75, label = labels, density = True)
                if efficiencies_plot:
                    x, efficiencies = efficiency_value(folders_data, binsize)
                    sides = ["left", "right"]
                    for side_index, side in enumerate(efficiencies):
                        for folder_index, folder in enumerate(side):
                            label = "efficiencies for " + folders[folder_index] + " to the " + sides[side_index]
                            efficiencies_subplot.plot(x, folder, label = label)
                efficiencies_subplot.set_xlim(x_interval)
                efficiencies_subplot.legend(prop = {'size': 8}, loc = "upper right")
            else:
                for folder_index, folder_data in enumerate(folders_data):
                    labels = filename_list[folder_index]
                    for file_index, file_data in enumerate(folder_data):
                        plot_data = [event_data[0] for event_data in file_data if event_data[-1] == stuff]
                        label = labels[file_index]
                        data_subplot.hist(plot_data, bins = bins, alpha = 0.75, label = label, density = True)
            if efficiencies_plot:
                x, efficiencies = efficiency_value(folders_data, binsize)
                sides = ["left", "right"]
                for side_index, side in enumerate(efficiencies):
                    for folder_index, folder in enumerate(side):
                        label = "efficiencies for " + folders[folder_index] + " to the " + sides[side_index]
                        efficiencies_subplot.plot(x, folder, label = label)
                efficiencies_subplot.set_xlim(x_interval)
                efficiencies_subplot.legend(prop = {'size': 8}, loc = "upper right")
            data_subplot.legend(prop = {'size': 8})
    else:
        if efficiencies_plot:
            subplots = fig.subplots(1, 2)
            data_subplot = subplots[0]
            efficiencies_subplot = subplots[1]
            efficiencies_subplot.set_xlabel(xlabel)
            efficiencies_subplot.set_ylabel("Relative Efficiencies")
            title = "Maximum Measured PT Distribution per event"
            efficiencies_subplot.set_title(title)
        else:
            data_subplot = fig.subplots(1, 1)
        data_subplot.set_xlabel(xlabel)
        data_subplot.set_ylabel("Frequency of Events")
        title = "Maximum Measured PT Distribution per event"
        data_subplot.set_title(title)
        interval_data = unpacker(folders_data, [])
        x_interval = plot_filter(interval_data, filter_strengths)
        data_subplot.set_xlim(x_interval)
        bin_data = [unpacker(folder_data, []) for folder_data in folders_data]
        bins = binfinder(bin_data, binsize)
        
        if combine_files:
            plot_data = [unpacker(folder_data, []) for folder_data in folders_data]
            labels = folders
            data_subplot.hist(plot_data, bins = bins, alpha = 0.75, label = labels, density = True)
            if efficiencies_plot:
                x, efficiencies = efficiency_value(folders_data, binsize)
                sides = ["left", "right"]
                for side_index, side in enumerate(efficiencies):
                    for folder_index, folder in enumerate(side):
                        label = "efficiencies for " + folders[folder_index] + " to the " + sides[side_index]
                        efficiencies_subplot.plot(x, folder, label = label)
                efficiencies_subplot.set_xlim(x_interval)
                efficiencies_subplot.legend(prop = {'size': 8}, loc = "upper right")
        else:
            for folder_index, folder_data in enumerate(folders_data):
                labels = filename_list[folder_index]
                for file_index, file_data in enumerate(folder_data):
                    label = labels[file_index]
                    data_subplot.hist(file_data, bins = bins, alpha = 0.5, label = label, density = True)
            if efficiencies_plot:
                x, efficiencies = efficiency_value(folders_data, binsize)
                sides = ["left", "right"]
                for side_index, side in enumerate(efficiencies):
                    for folder_index, folder in enumerate(side):
                        label = "efficiencies for " + folders[folder_index] + " to the " + sides[side_index]
                        efficiencies_subplot.plot(x, folder, label = label)
                efficiencies_subplot.set_xlim(x_interval)
                efficiencies_subplot.legend(prop = {'size': 8}, loc = "upper right")
        data_subplot.legend(prop = {'size': 8})

    plt.show()
    
    
    
    
    
    
