import shutil
import pandas as pd
import os, re


directory = os.getcwd()+"/data/fakenews_tw_output/take_off_0510"

print(directory)

df = pd.read_csv("data/fakenews_sources/all_politifact_1210nodup.csv")

df = df.reset_index()
lst_of_indexes = list(df['Unnamed: 0'])
set_of_indexes = set(df['Unnamed: 0'])

#print(set_of_indexes)



for filename in os.listdir(directory):
    
    index_of_file = re.search(r"_\d*_", filename)[0].split("_")[1]

    if int(index_of_file) in set_of_indexes:
        source = directory+"/"+filename
        destination = os.getcwd()+"/data/fakenews_tw_output/nodub_take_off_0510/"+filename
        shutil.copy(source, destination)
        