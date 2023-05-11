import csv
import json
import sys
from pathlib import Path

gen_dir = str(Path(__file__).resolve().parents[3])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)

import pickle

import pandas as pd

from utils import unzip as uz

# Santa_Clara_Path = '/data/input_data/inrix/SantaClara/santa_clara_2022-04-01_to_2022-06-01_60_min_part_1/metadata.csv'
# Seattle_Path = '/data/created_data/input_data/inrix/Seattle/metadata.csv'

county = "HarrisCounty"
columns_to_keep = ['Segment ID', 'Hist Av Speed(km/hour)', 'Ref Speed(km/hour)']
files = uz.get_zip_files(folder_path= gen_dir + '/data/input_data/inrix/' + county)
files = files[:2]
dfs = uz.read_csvs_from_zips(name = 'data.csv', files=files, 
                                columns_to_keep=columns_to_keep)

combined_df = pd.concat(dfs, ignore_index=True)
df = combined_df.drop_duplicates()

seg_id_list = df['Segment ID'].tolist()
ref_speed_list = df['Ref Speed(km/hour)'].tolist()
hist_speed_list = df['Hist Av Speed(km/hour)'].tolist()

seg_to_reference_speed = {}

for ref, hist, seg_id in zip(ref_speed_list, hist_speed_list, seg_id_list):
    seg_to_reference_speed[str(seg_id)] = {'Ref Speed(km/hour)' : ref, 'Hist Av Speed(km/hour)': hist}


with open(gen_dir + '/data/created_data/' + county + '/segid_to_refspeed.pkl', "wb") as f:
    pickle.dump(seg_to_reference_speed, f)


