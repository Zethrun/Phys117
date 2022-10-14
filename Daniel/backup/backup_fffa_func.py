def find_files_for_analysis(org_files_folder, plot_comparison, picking_file_order, random_pick = False, multiple_amount_tuple = None):
    folder_path = "Data/Pandas/Individual/"
    #pick_file_order is a list if not single
    pick_file_order_multiple = picking_file_order
        
    files_1 = org_files_folder[plot_comparison[0]][0]
    files_2 = org_files_folder[plot_comparison[1]][0]
    amount_1, amount_2 = len(files_1), len(files_2)
    picks_file_1 = pick_file_order_multiple[0]
    picks_file_2 = pick_file_order_multiple[1]
    
    if random_pick:
        #willpick same amount as specified
        if pick_file_order_multiple != None and multiple_amount_tuple == None:
            len_picks_1 = len(picks_file_1)
            len_picks_2 = len(picks_file_2)
        elif multiple_amount_tuple != None: # if we dont specify what files
            len_picks_1 = multiple_amount_tuple[0]
            len_picks_2 = multiple_amount_tuple[1]
        picks_1 = [random.randint(0, amount_1-1) for i in range(len_picks_1)]
        picks_2 = [random.randint(0, amount_2-1) for i in range(len_picks_2)]
        picks_1_names = [org_files_folder[plot_comparison[0]][1][index] for index in picks_1]
        picks_2_names = [org_files_folder[plot_comparison[1]][1][index] for index in picks_2]
    
    else:
        picks_1 = []
        picks_2 = []
        picks_1_names = []
        picks_2_names = []
        
        for picked_file in picks_file_1:
            pick_1 = org_files_folder[plot_comparison[0]][1].index(picked_file)
            picks_1_names.append(picked_file)
            picks_1.append(pick_1) 
                        
        for picked_file in picks_file_2:
            pick_2 = org_files_folder[plot_comparison[1]][1].index(picked_file)
            picks_2_names.append(picked_file)
            picks_2.append(pick_2)
    
    picked_files_1 = [files_1[i] for i in picks_1]
    picked_files_2 = [files_2[i] for i in picks_2]
    files_1_path = [file[0].removesuffix("/electron.csv") for file in picked_files_1]
    files_2_path = [file[0].removesuffix("/electron.csv") for file in picked_files_2]
    return picked_files_1, picked_files_2, files_1_path, files_2_path, picks_1_names, picks_2_names