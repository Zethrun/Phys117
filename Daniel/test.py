import pandas as pd
import os

new_folder_path = "subfolder/"
filename = "test.csv"

data = {
    0 : ["Hei", "Hallo"],
    1 : ["Nei", "No"],
    2 : ["Ja", "Yes"]
}

df = pd.DataFrame(data)
"""
def compress_to_zip():
    compression_opts = dict(method="zip", archive_name="out.csv")

    df.to_csv("out.zip", index=False, compression=compression_opts)

def create_file():
    os.makedirs(new_folder_path, exist_ok = True)
    df.to_csv(new_folder_path + filename)
"""

path = "C:/Users/danie/OneDrive/Dokumenter/Studie/phys117/coding/data_pandas/BH"
print(pd.read_csv(path + "/" + "MET.csv"))


#os.makedirs for lage folder
#to_csv(file path + )