from LHCO_reader import partition_problem as pp
from LHCO_reader import LHCO_reader
import os






data_path = "Data/LHCO/Original/BH/"
files = [data_path + filename for filename in os.listdir(data_path)]

for index, file in enumerate(files):
    if index == 2:
        events = LHCO_reader.Events(f_name = file)
        print(events[684])