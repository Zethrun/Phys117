def calculate_efficiency(data):
    data = data[0]
    bin_ls = calculate_bin(data, binsize)
    dx = bin_ls[2] - bin_ls[1]
    data_filelist = {}
    file_names = []
    efficiency_list = [] # first index is list of the file_names
    check = len(data[0][0])
    if check > 2:
        print("This only works with a pair of data_file")
        return None
    else:
        for type_data in data:
            file_names.append(type_data[1][0])
            for type_data_file in type_data[0]:
                data_filelist[type_data[1][0]] = type_data_file
        
        count_1, bins_1 = np.histogram(data_filelist[file_names[0]],bin_ls)
        count_2, bins_2 = np.histogram(data_filelist[file_names[1]],bin_ls)
        """ norm_fact_1 = 1/(sum(count_1))
        norm_fact_2 = 1/(sum(count_2))
        count_1 = norm_fact_1 * np.array(count_1)
        count_2 = norm_fact_2 * np.array(count_2)"""

        
        for k_index, k in enumerate(bin_ls[:-1]):
            #1_file left
            area_f_1_l = 0
            area_f_2_l = 0
                        
            for index, i in enumerate(bin_ls[:-1]):
                try:
                    if i < k_index:
                        area_f_1_l += count_1[index]*dx #dont need binsize but i keep cause is pretty
                    elif i >= k_index:
                        area_f_2_l += count_2[index]*dx
                except:
                    pass
            
            #1_file right
            area_f_1_r = 0
            area_f_2_r = 0
            
            for index, i in enumerate(bin_ls[:-1]):
                try:
                    if i < k_index:
                        area_f_2_r += count_2[index]*dx
                    elif i >= k_index:
                        area_f_1_r += count_1[index]*dx
                except:
                    pass
                    
            area_total = area_f_1_l + area_f_1_r + area_f_2_l + area_f_2_r
            print(area_total)
            
            e_1_l = area_f_1_l / area_total
            e_2_l = area_f_2_l / area_total
            e_1_r = area_f_1_r / area_total
            e_2_r = area_f_2_r / area_total
            
            if (e_1_l + e_2_l) < (e_1_r + e_2_r):
                efficiency_list.append([e_1_r, e_2_r])
            elif  (e_1_l + e_2_l) > (e_1_r + e_2_r):
                efficiency_list.append([e_1_l, e_2_l])
            else:
                efficiency_list.append([e_1_l, e_2_l])
    
        return efficiency_list
    
    
    
    
def calculate_efficiency(data, return_list = False, return_sep = False):
    data = data[0]
    bin_ls = calculate_bin(data, binsize)
    dx = bin_ls[2] - bin_ls[1]
    data_filelist = {}
    file_names = []
    efficiency_list = [] # first index is list of the file_names
    efficiency_list_sep = []
    check = len(data[0][0])
    if check > 2:
        print("This only works with a pair of data_file")
        return None
    else:
        for type_data in data:
            file_names.append(type_data[1][0])
            for type_data_file in type_data[0]:
                data_filelist[type_data[1][0]] = type_data_file
        
        count_1, bins_1 = np.histogram(data_filelist[file_names[0]],bin_ls)
        count_2, bins_2 = np.histogram(data_filelist[file_names[1]],bin_ls)
        norm_fact_1 = 1/(sum(count_1))
        norm_fact_2 = 1/(sum(count_2))
        count_1 = norm_fact_1 * np.array(count_1)
        count_2 = norm_fact_2 * np.array(count_2)


        for k_index, k in enumerate(bin_ls[1:-1]):
            A_total = np.sum(count_1) + np.sum(count_2)
            
            A_1_left = 0
            A_1_right = 0
            A_2_left = 0
            A_2_right = 0
            
            """A_1_left = np.sum(count_1[:k_index])
            A_1_right = np.sum(count_1[k_index:-1])
            A_2_left = np.sum(count_2[:k_index])
            A_2_right = np.sum(count_2[k_index:-1])"""
            
            for i in range(len(bin_ls[:-1])):
                if i < k_index:
                    #left
                    A_1_left += count_1[i]
                    A_2_left += count_2[i]
                elif i >= k_index:
                    #right
                    A_1_right += count_1[i]
                    A_2_right += count_2[i]
            
            #file1 left, file2 right, alfa:
            e_1_alfa, e_2_alfa = A_1_left/A_total, A_2_right/A_total
            e_T_alfa = e_1_alfa + e_2_alfa
            
            #file1 right, file left, beta:
            e_1_beta, e_2_beta = A_1_right/A_total, A_2_left/A_total
            e_T_beta = e_1_beta + e_2_beta
             
            if e_T_alfa >= e_T_beta:
                efficiency_list.append(e_T_alfa)
                efficiency_list_sep.append([e_1_alfa, e_2_alfa])
            elif e_T_alfa < e_T_beta:
                efficiency_list.append(e_T_beta)
                efficiency_list_sep.append([e_1_beta, e_2_beta])
            
        if return_list == True:
            if return_sep == True:
                return efficiency_list_sep
            else:
                return efficiency_list
        else:
            max_efficiency = np.max(efficiency_list)
        return max_efficiency
    

def calculate_efficiency(data, return_list = False, return_sep = False, for_itterate = False):
    if for_itterate:
        data = data
    if not for_itterate:
        data = data[0]
    bin_ls = calculate_bin(data, binsize)
    dx = bin_ls[2] - bin_ls[1]
    data_filelist = {}
    file_names = []
    efficiency_list = [] # first index is list of the file_names
    efficiency_list_sep = []
    check = len(data[0][0])
    if check > 2:
        print("This only works with a pair of data_file")
        return None
    else:
        for type_data in data:
            file_names.append(type_data[1][0])
            for type_data_file in type_data[0]:
                data_filelist[type_data[1][0]] = type_data_file
        
        count_1, bins_1 = np.histogram(data_filelist[file_names[0]],bin_ls)
        count_2, bins_2 = np.histogram(data_filelist[file_names[1]],bin_ls)
        norm_fact_1 = 1/(sum(count_1))
        norm_fact_2 = 1/(sum(count_2))
        count_1 = norm_fact_1 * np.array(count_1)
        count_2 = norm_fact_2 * np.array(count_2)


        for k_index, k in enumerate(bin_ls[1:-1]):
            A_total = np.sum(count_1) + np.sum(count_2)   
            A_1_left = np.sum(count_1[:k_index])
            A_1_right = np.sum(count_1[k_index:-1])
            A_2_left = np.sum(count_2[:k_index])
            A_2_right = np.sum(count_2[k_index:-1])
            
            #file1 left, file2 right, alfa:
            e_1_alfa, e_2_alfa = A_1_left/A_total, A_2_right/A_total
            e_T_alfa = e_1_alfa + e_2_alfa
            
            #file1 right, file left, beta:
            e_1_beta, e_2_beta = A_1_right/A_total, A_2_left/A_total
            e_T_beta = e_1_beta + e_2_beta
             
            if e_T_alfa >= e_T_beta:
                efficiency_list.append(e_T_alfa)
                efficiency_list_sep.append([e_1_alfa, e_2_alfa])
            elif e_T_alfa < e_T_beta:
                efficiency_list.append(e_T_beta)
                efficiency_list_sep.append([e_1_beta, e_2_beta])
            
        if return_list == True:
            if return_sep == True:
                return efficiency_list_sep
            else:
                return efficiency_list
        else:
            max_efficiency = np.max(efficiency_list)
        return max_efficiency