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


def plot_filter(plot_data, multi_plots, filter_strengths):
    if multi_plots:
        x_limits_min = []
        x_limits_max = []
        plots_min = []
        plots_max = []
        plot_datas = plot_data
        for plot_data in plot_datas:
            variable_data = np.array(plot_data)
            mean = np.mean(variable_data)
            std_dev = np.std(variable_data)
            x_limit_min = mean - filter_strengths[0]*std_dev
            x_limit_max = mean + filter_strengths[1]*std_dev
            x_limits_max.append(x_limit_max)
            x_limits_min.append(x_limit_min)
            plots_min.append(np.min(plot_data))
            plots_max.append(np.max(plot_data))

        if np.min(plots_min) >= np.min(x_limit_min):
            x_limits_min = np.min(plots_min)
        if np.max(plots_max) <= np.max(x_limits_max):
            x_limits_max = np.max(plot_data)
        return [np.min(x_limits_min), np.max(x_limits_max)]
    else:
        variable_data = np.array(plot_data)
        mean = np.mean(variable_data)
        std_dev = np.std(variable_data)
        x_limit_min = mean - filter_strengths[0]*std_dev
        x_limit_max = mean + filter_strengths[1]*std_dev
        if np.min(plot_data) >= 0 and x_limit_min <=0:
            x_limit_min = 0
        if np.max(plot_data) <= x_limit_max:
            x_limit_max = np.max(plot_data)
        return [x_limit_min, x_limit_max]


def efficiency_value(data, binsize):
    bh_data, sphal_data = data
    x_bh, y_bh = data_binner(bh_data, binsize, plot = False)
    x_sphal, y_sphal = data_binner(sphal_data, binsize, plot = False)
    x_interval = np.concatenate((x_bh, x_sphal))
    x_min, x_max = np.min(x_interval), np.max(x_interval)
    bins = int(np.round((x_max - x_min)/binsize))
    efficiencies = []

    for bin in range(bins + 1):
        sphal_left = y_sphal[:bin + 1]
        sphal_right = y_sphal[bin + 1:]
        sphal_split = [sphal_left, sphal_right]

        bh_left = y_bh[:bin + 1]
        bh_right = y_bh[bin + 1:]
        bh_split = [bh_right, bh_left]

        temp_efficiencies = []
        for i in range(len(["left", "right"])):
            sphal_efficiency = np.sum(sphal_split[i])/2
            bh_efficiency = np.sum(bh_split[i])/2
            total_efficiency = sphal_efficiency + bh_efficiency
            temp_efficiencies.append(total_efficiency)
        temp_efficiencies = sorted(temp_efficiencies)
        efficiencies.append((temp_efficiencies[-1], bin))

    sorted_list = sorted(efficiencies, key = lambda x: x[0])
    efficiency_data = sorted_list[-1]
    efficiency = np.round(efficiency_data[0], 3) * 100
    bin = efficiency_data[1]
    efficiency_line = x_min + bin*binsize

    return efficiency, efficiency_line


def MET_dist(folders_data, folders, filename_list, stuffs, binsize, filter_strengths, xlabel, compare, combine_files):
    fig = plt.figure()
    style = "seaborn-darkgrid"
    plt.style.use(style)

    if compare:
        ax = fig.subplots(1, 1)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Frequency of Events")
        title = "MET Distribution"
        ax.set_title(title)
        for folder_index, folder_data in enumerate(folders_data):
            if combine_files:
                multi_plots = True
                interval_data = [unpacker(folder_data, []) for folder_data in folders_data]
                x_interval = plot_filter(interval_data, multi_plots, filter_strengths)
                ax.set_xlim(x_interval)
                data = folder_data
                x, y = data_binner(data, binsize, plot = True)
                labels = folders
                label = labels[folder_index]
                ax.plot(x, y, label = label)
            else:
                multi_plots = True
                interval_data = [unpacker(folder_data, []) for folder_data in folders_data]
                x_interval = plot_filter(interval_data, multi_plots, filter_strengths)
                ax.set_xlim(x_interval)
                labels = filename_list[folder_index]
                for data_index, data in enumerate(folder_data):
                    x, y = data_binner(data, binsize, plot = True)
                    label = labels[data_index]
                    ax.plot(x, y, label = label)
        if compare and combine_files:
            efficiency, efficiency_line = efficiency_value(folders_data, binsize)
            plt.axvline(x = efficiency_line, color = "r", label = str(efficiency_line) + " - " + str(efficiency) + "%")
        ax.legend(prop = {'size': 8})

    else:
        subfigs = fig.subfigures(1, len(folders_data))
        titles = folders
        for folder_index, folder_data in enumerate(folders_data):
            subfig = subfigs[folder_index]
            ax = subfig.subplots(1, 1)
            title = titles[folder_index]
            ax.set_title(title)
            ax.set_xlabel(xlabel)
            ax.set_ylabel("Frequency of Events")
            ax.legend(prop = {'size': 8})
            if combine_files:
                multi_plots = False
                interval_data = [unpacker(folder_data, []) for folder_data in folders_data]
                x_interval = plot_filter(folder_data, multi_plots, filter_strengths)
                ax.set_xlim(x_interval)
                data = folder_data
                x, y = data_binner(data, binsize, plot = True)
                labels = folders
                label = labels[folder_index]
                ax.plot(x, y, label = label)
            else:
                multi_plots = True
                interval_data = [unpacker(folder_data, []) for folder_data in folders_data]
                x_interval = plot_filter(folder_data, multi_plots, filter_strengths)
                ax.set_xlim(x_interval)
                labels = filename_list[folder_index]
                for data_index, data in enumerate(folder_data):
                    x, y = data_binner(data, binsize, plot = True)
                    label = labels[data_index]
                    ax.plot(x, y, label = label)

            ax.legend(prop = {'size': 8})

    plt.show()


def HT_dist(folders_data, folders, filename_list, stuffs, binsize, filter_strengths, xlabel, compare, combine_files):
    fig = plt.figure()
    style = "seaborn-darkgrid"
    plt.style.use(style)

    if compare:
        ax = fig.subplots(1, 1)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Frequency of Events")
        title = "HT Distribution"
        ax.set_title(title)
        for folder_index, folder_data in enumerate(folders_data):
            if combine_files:
                multi_plots = True
                interval_data = [unpacker(folder_data, []) for folder_data in folders_data]
                x_interval = plot_filter(interval_data, multi_plots, filter_strengths)
                ax.set_xlim(x_interval)
                data = folder_data
                x, y = data_binner(data, binsize, plot = True)
                labels = folders
                label = labels[folder_index]
                ax.plot(x, y, label = label)
            else:
                multi_plots = True
                interval_data = [unpacker(folder_data, []) for folder_data in folders_data]
                x_interval = plot_filter(interval_data, multi_plots, filter_strengths)
                ax.set_xlim(x_interval)
                labels = filename_list[folder_index]
                for data_index, data in enumerate(folder_data):
                    x, y = data_binner(data, binsize, plot = True)
                    label = labels[data_index]
                    ax.plot(x, y, label = label)
        if compare and combine_files:
            efficiency, efficiency_line = efficiency_value(folders_data, binsize)
            plt.axvline(x = efficiency_line, color = "r", label = str(efficiency_line) + " - " + str(efficiency) + "%")
        ax.legend(prop = {'size': 8})

    else:
        subfigs = fig.subfigures(1, len(folders_data))
        titles = folders
        for folder_index, folder_data in enumerate(folders_data):
            subfig = subfigs[folder_index]
            ax = subfig.subplots(1, 1)
            title = titles[folder_index]
            ax.set_title(title)
            ax.set_xlabel(xlabel)
            ax.set_ylabel("Frequency of Events")
            ax.legend(prop = {'size': 8})
            if combine_files:
                multi_plots = False
                interval_data = [unpacker(folder_data, []) for folder_data in folders_data]
                x_interval = plot_filter(folder_data, multi_plots, filter_strengths)
                ax.set_xlim(x_interval)
                data = folder_data
                x, y = data_binner(data, binsize, plot = True)
                labels = folders
                label = labels[folder_index]
                ax.plot(x, y, label = label)
            else:
                multi_plots = True
                interval_data = [unpacker(folder_data, []) for folder_data in folders_data]
                x_interval = plot_filter(folder_data, multi_plots, filter_strengths)
                ax.set_xlim(x_interval)
                labels = filename_list[folder_index]
                for data_index, data in enumerate(folder_data):
                    x, y = data_binner(data, binsize, plot = True)
                    label = labels[data_index]
                    ax.plot(x, y, label = label)

            ax.legend(prop = {'size': 8})

    plt.show()


def stuff_amount_plot(folders_data, folders, filename_list, stuffs, binsize, filter_strengths, xlabel, compare, combine_files):
    fig = plt.figure()
    style = "seaborn-darkgrid"
    plt.style.use(style)
    ax = fig.subplots(1, 1)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Frequency of Events")
    title = "Distribution of Total Amount of Particles per Event"
    ax.set_title(title)
    bins = binfinder(folders_data, binsize)
    
    if combine_files:
        amount_data = [unpacker(folder_data, []) for folder_data in folders_data]
        labels = folders
        ax.hist(amount_data, bins = bins, alpha = 0.75, label = labels, density = True)
        efficiency, efficiency_line = efficiency_value(amount_data, binsize)
        plt.axvline(x = efficiency_line, color = "r", label = str(efficiency_line) + " - " + str(efficiency) + "%")
        ax.legend(prop = {'size': 8})
        
    else:
        efficiency_data = []
        for folder_index, folder_data in enumerate(folders_data):
            labels = filename_list[folder_index]
            if len(folder_data) == 1:
                efficiency_line = True
            else:
                efficiency_line = False
            for file_index, file_data in enumerate(folder_data):
                amount_data = file_data
                efficiency_data.append(amount_data)
                label = labels[file_index]
                ax.hist(amount_data, bins = bins, alpha = 0.75, label = label, density = True)
                ax.legend(prop = {'size': 8})
        if efficiency_line:
            efficiency, efficiency_line = efficiency_value(efficiency_data, binsize)
            plt.axvline(x = efficiency_line, color = "r", label = str(efficiency_line) + " - " + str(efficiency) + "%")
            ax.legend(prop = {'size': 8})
        
    plt.show()


def stuff_counts_plot(folders_data, folders, filename_list, stuffs, binsize, filter_strengths, xlabel, compare, combine_files):
    fig = plt.figure()
    style = "seaborn-darkgrid"
    plt.style.use(style)
    subfigs_y = fig.subfigures(2, 1)
    subfigs_1 = subfigs_y[0].subfigures(1, 2)
    subfigs_2 = subfigs_y[1].subfigures(1, 3)
    subfigs = [*subfigs_1, *subfigs_2]
    stuffs = [stuff for stuff in stuffs if stuff != "MET"]

    for stuff_index, stuff in enumerate(stuffs):
        bins = binfinder(folders_data, binsize)
        subfig = subfigs[stuff_index]
        ax = subfig.subplots(1, 1)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Frequency of Events")
        title = "Distribution of " + stuff + "s"
        ax.set_title(title)
        if combine_files:
            # multi_plots = True
            # interval_data = [unpacker(folder_data[stuff_index], []) for folder_data in folders_data]
            # x_interval = plot_filter(interval_data, multi_plots, filter_strengths)
            # ax.set_xlim(x_interval)
            plot_data = [unpacker(folder_data[stuff_index], []) for folder_data in folders_data]
            labels = folders
            ax.hist(plot_data, bins = bins, alpha = 0.75, label = labels, density = True)
            efficiency, efficiency_line = efficiency_value(plot_data, binsize)
            plt.axvline(x = efficiency_line, color = "r", label = str(efficiency_line) + " - " + str(efficiency) + "%")
            ax.legend(prop = {'size': 8})
        else:
            # multi_plots = True
            # interval_data = [unpacker(data[stuff_index], []) for folder_data in folders_data for data in folder_data]
            # x_interval = plot_filter(interval_data, multi_plots, filter_strengths)
            # ax.set_xlim(x_interval)
            efficiency_data = []
            for folder_index, folder_data in enumerate(folders_data):
                labels = filename_list[folder_index]
                if len(folder_data) == 1:
                    efficiency_line = True
                    efficiency_data.append(folder_data[0])
                else:
                    efficiency_line = False
                for file_index, file_data in enumerate(folder_data):
                    for count_index, count_data in enumerate(file_data):
                        if count_index == stuff_index:
                            label = labels[file_index]
                            ax.hist(count_data, bins = bins, alpha = 0.75, label = label, density = True)
                            ax.legend(prop = {'size': 8})
            if efficiency_line:
                efficiency, efficiency_line = efficiency_value(efficiency_data, binsize)
                plt.axvline(x = efficiency_line, color = "r", label = str(efficiency_line) + " - " + str(efficiency) + "%")
                ax.legend(prop = {'size': 8})

    plt.show()
    
    
def PT_max_plot(folders_data, folders, filename_list, stuffs, by_particle, binsize, filter_strengths, xlabel, compare, combine_files):
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
            bin_data = [unpacker(folder_data, []) for folder_data in folders_data]
            bin_data = [event_data[0] for folder_data in bin_data for event_data in folder_data if event_data[-1] == stuff]
            bins = binfinder(bin_data, binsize)
            subfig = subfigs[stuff_index]
            ax = subfig.subplots(1, 1)
            ax.set_xlabel(xlabel)
            ax.set_ylabel("Frequency of Events")
            title = "Maximum Measured PT  Distribution of " + stuff + "s per event"
            ax.set_title(title)
            
            if combine_files:
                # multi_plots = True
                # interval_data = [unpacker(folder_data, []) for folder_data in folders_data]
                # interval_data = [event_data[0] for folder_data in interval_data for event_data in folder_data if event_data[-1] == stuff]
                # x_interval = plot_filter(interval_data, multi_plots, filter_strengths)
                # ax.set_xlim(x_interval)
                plot_data = [unpacker(folder_data, []) for folder_data in folders_data]
                plot_data = [[event_data[0] for event_data in folder_data if event_data[-1] == stuff] for folder_data in plot_data]
                labels = folders
                ax.hist(plot_data, bins = bins, alpha = 0.75, label = labels, density = True)
                efficiency, efficiency_line = efficiency_value(plot_data, binsize)
                plt.axvline(x = efficiency_line, color = "r", label = str(efficiency_line) + " - " + str(efficiency) + "%")
                ax.legend(prop = {'size': 8})
            else:
                # multi_plots = True
                # interval_data = [unpacker(folder_data, []) for folder_data in folders_data]
                # interval_data = [event_data[0] for folder_data in interval_data for event_data in folder_data if event_data[-1] == stuff]
                # x_interval = plot_filter(interval_data, multi_plots, filter_strengths)
                # ax.set_xlim(x_interval)
                efficiency_data = []
                for folder_index, folder_data in enumerate(folders_data):
                    labels = filename_list[folder_index]
                    if len(folder_data) == 1:
                        efficiency_line = True
                        efficiency_data.append(folder_data[0])
                    else:
                        efficiency_line = False
                    for file_index, file_data in enumerate(folder_data):
                        plot_data = [event_data[0] for event_data in file_data if event_data[-1] == stuff]
                        label = labels[file_index]
                        ax.hist(plot_data, bins = bins, alpha = 0.75, label = label, density = True)
                        ax.legend(prop = {'size': 8})
                if efficiency_line:
                    efficiency, efficiency_line = efficiency_value(efficiency_data, binsize)
                    plt.axvline(x = efficiency_line, color = "r", label = str(efficiency_line) + " - " + str(efficiency) + "%")
                    ax.legend(prop = {'size': 8})

    else:
        bin_data = [unpacker(folder_data, []) for folder_data in folders_data]
        bins = binfinder(bin_data, binsize)
        ax = fig.subplots(1, 1)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Frequency of Events")
        title = "Maximum Measured PT Distribution per event"
        ax.set_title(title)
        
        if combine_files:
            # multi_plots = True
            # interval_data = [unpacker(folder_data, []) for folder_data in folders_data]
            # x_interval = plot_filter(interval_data, multi_plots, filter_strengths)
            # ax.set_xlim(x_interval)
            plot_data = [unpacker(folder_data, []) for folder_data in folders_data]
            labels = folders
            ax.hist(plot_data, bins = bins, alpha = 0.75, label = labels, density = True)
            efficiency, efficiency_line = efficiency_value(plot_data, binsize)
            plt.axvline(x = efficiency_line, color = "r", label = str(efficiency_line) + " - " + str(efficiency) + "%")
            ax.legend(prop = {'size': 8})
        else:
            # multi_plots = True
            # interval_data = [unpacker(folder_data, []) for folder_data in folders_data]
            # x_interval = plot_filter(interval_data, multi_plots, filter_strengths)
            # ax.set_xlim(x_interval)
            efficiency_data = []
            for folder_index, folder_data in enumerate(folders_data):
                labels = filename_list[folder_index]
                if len(folder_data) == 1:
                    efficiency_line = True
                    efficiency_data.append(folder_data[0])
                else:
                    efficiency_line = False
                for file_index, file_data in enumerate(folder_data):
                    label = labels[file_index]
                    ax.hist(file_data, bins = bins, alpha = 0.5, label = label, density = True)
                    ax.legend(prop = {'size': 8})
            if efficiency_line:
                efficiency, efficiency_line = efficiency_value(efficiency_data, binsize)
                plt.axvline(x = efficiency_line, color = "r", label = str(efficiency_line) + " - " + str(efficiency) + "%")
                ax.legend(prop = {'size': 8})
    plt.show()
    
    
    
    
    
    
