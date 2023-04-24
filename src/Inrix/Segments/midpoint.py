import csv
import json
import sys
from pathlib import Path

gen_dir = str(Path(__file__).resolve().parents[3])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)

from utils import unzip as uz
import pickle

# Santa_Clara_Path = '/data/input_data/inrix/SantaClara/santa_clara_2022-04-01_to_2022-06-01_60_min_part_1/metadata.csv'
# Seattle_Path = '/data/created_data/input_data/inrix/Seattle/metadata.csv'

county = "HarrisCounty"

files = uz.get_zip_files(folder_path= gen_dir + '/data/input_data/inrix/' + county)
df = uz.read_csvs_from_zips(name = 'metadata.csv', files=files, 
                                columns_to_keep=['Segment ID', 'Start Latitude', 'Start Longitude', 'End Latitude', 'End Longitude', 'Segment Length(Kilometers)'])[0]


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


with open(gen_dir + '/data/created_data/' + county + '/midpoints.pkl', "wb") as f:
    pickle.dump(midpoints, f)


