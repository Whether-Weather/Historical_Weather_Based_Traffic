import csv
import json
import sys
import zipfile

from pathlib import Path

gen_dir = str(Path(__file__).resolve().parents[3])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)

from utils import unzip as uz
import pickle
import pandas as pd
import argparse
import os
import io

parser = argparse.ArgumentParser(description='Process input and output data folders.')
parser.add_argument('--input_data', type=str, required=False, help='Path to the input data folder')
parser.add_argument('--output_data', type=str, required=False, help='Path to the output data folder')

args = parser.parse_args()

input_data_folder = args.input_data
output_data_folder = args.output_data

# Santa_Clara_Path = '/data/input_data/inrix/SantaClara/santa_clara_2022-04-01_to_2022-06-01_60_min_part_1/metadata.csv'
# Seattle_Path = '/data/created_data/input_data/inrix/Seattle/metadata.csv'

county = "HarrisCounty"
columns_to_keep = ['Segment ID', 'Start Latitude', 'Start Longitude', 'End Latitude', 'End Longitude', 'Segment Length(Kilometers)']
if not input_data_folder:
    input_folder_path = gen_dir + '/data/input_data/inrix/' + county
else:
    input_folder_path = input_data_folder

if not output_data_folder:
    output_folder_path = gen_dir + '/data/created_data/' + county
else:
    output_folder_path = output_data_folder


files = uz.get_zip_files(folder_path= input_folder_path)
dfs = uz.read_csvs_from_zips(name = 'metadata.csv', files=files, 
                                columns_to_keep=columns_to_keep)

combined_df = pd.concat(dfs, ignore_index=True)
df = combined_df.drop_duplicates()
# Create a dictionary with the midpoint of each segment as the value

start_lat_list = df['Start Latitude'].tolist()
start_long_list = df['Start Longitude'].tolist()
end_lat_list = df['End Latitude'].tolist()
end_long_list = df['End Longitude'].tolist()
seg_id_list = df['Segment ID'].tolist()


midpoints = {}

for sla, slo, ela, elo, seg_id in zip(start_lat_list, start_long_list, end_lat_list, end_long_list, seg_id_list):
    start_lat, end_lat = float(sla), float(ela)
    start_lon, end_lon = float(slo), float(elo)
    mid_lat = (start_lat + end_lat) / 2
    mid_lon = (start_lon + end_lon) / 2
    midpoint = (mid_lat, mid_lon)
    midpoints[str(seg_id)] = midpoint


print(output_folder_path  + '/midpoints.pkl')
with open( output_folder_path  + '/midpoints.pkl', "wb") as f:
    pickle.dump(midpoints, f)


print("done")

