import pickle
import subprocess
import sys
from pathlib import Path
import json
import pandas as pd

gen_dir = str(Path(__file__).resolve().parents[2])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)



county = 'SantaClara'
models_directory = gen_dir + "/data/created_data/" + county  + "/"
models_filename = models_directory + "santaclara.pkl"

with open(models_filename, "rb") as f:
    loaded_models_dict = pickle.load(f)

from utils import unzip as uz

county = "SantaClara"
columns_to_keep = ['Segment ID', 'Start Latitude', 'Start Longitude', 'End Latitude', 'End Longitude', 'Segment Length(Kilometers)', 'Road', 'Direction']

input_folder_path = gen_dir + '/data/input_data/inrix/' + county



output_folder_path = gen_dir + '/data/created_data/' + county


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
road_list = df['Road'].tolist()
direct_list = df['Direction'].tolist()


data = {}

for sla, slo, ela, elo, seg_id,road,direct in zip(start_lat_list, start_long_list, end_lat_list, end_long_list, seg_id_list, road_list, direct_list):
    data[str(seg_id)] = [seg_id, road, direct, sla, ela, slo, elo]


differences = []
for segment_id in loaded_models_dict:
    #segment_data[['temp', 'dwpt', 'rhum', 'prcp_log', 'is_raining', 'wdir', 'wspd', 'pres', 'Hour']]
    X_test_max = [[40, 100, 0,    0,     0, 180, 100, 1100, 10]]
    X_test_min = [[0, 0, 100, 2.0,  1, 180,   100,  900, 18]]
    
    # Predict the speed using the linear regression model and the feature vector
    y_pred_max = loaded_models_dict[segment_id]['model'].predict(X_test_max)[0]
    y_pred_min = loaded_models_dict[segment_id]['model'].predict(X_test_min)[0]
    
    diff = y_pred_max - y_pred_min
    differences.append((segment_id, diff))

# Sort the list by the differences in descending order
differences.sort(key=lambda x: x[1], reverse=True)

# Get the top 10 segments with the greatest differences
top_30_differences = differences[:30]

for diff in top_30_differences:
    data[str(diff[0])].append(diff[1] * 16.66666666)
    print(data[str(diff[0])])

# for diff in top_10_differences:
#     print(diff[0] + f": {1/diff[1] * 100 }")
    
