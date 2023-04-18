import csv
import json
import sys
from pathlib import Path

gen_dir = str(Path(__file__).resolve().parents[3])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)

Santa_Clara_Path = '/data/input_data/inrix/SantaClara/santa_clara_2022-04-01_to_2022-06-01_60_min_part_1/metadata.csv'
Seattle_Path = '/data/created_data/input_data/inrix/Seattle/metadata.csv'
# Open the CSV file and read the data
with open(gen_dir + Seattle_Path, 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Create a dictionary with the midpoint of each segment as the value
midpoints = {}
for row in data:
    start_lat, end_lat = float(row['Start Latitude']), float(row['End Latitude'])
    start_lon, end_lon = float(row['Start Longitude']), float(row['End Longitude'])
    mid_lat = (start_lat + end_lat) / 2
    mid_lon = (start_lon + end_lon) / 2
    midpoint = (mid_lat, mid_lon)
    midpoints[row['Segment ID']] = midpoint

with open(gen_dir + '/data/created_data/input_data/inrix/midpoints_seattle.json', 'w') as fp:
        json.dump(midpoints, fp)

