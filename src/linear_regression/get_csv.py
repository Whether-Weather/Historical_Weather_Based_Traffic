import os
import json
import datetime
import pandas as pd
from meteostat import Stations, Daily
import sys
from pathlib import Path

gen_dir = str(Path(__file__).resolve().parents[2])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)


from utils import unzip as uz
from utils import file_helper_functions as fhf
from src.weather import getMeteostat as gm

import datetime

weather_dict = fhf.get_dict_from_json(gen_dir + "/data/created_data/weather/meteostat_weather.json")
segment_dict = fhf.get_dict_from_json(gen_dir + "/data/created_data/inrix/midpoints.json")


# Convert Meteostat data to a dictionary with timestamps as keys
def weather_data_update(segment_id):
    coordinates = segment_dict.get(segment_id)

    stations = Stations()
    stations = stations.nearby(coordinates[0], coordinates[1])  # Santa Clara County coordinates
    stations_list = stations.fetch(1)  # Get the 10 closest stations
    station_id = ''
    for station_id, station_info in stations_list.iterrows():
        print(station_id)
        break
    if weather_dict.get(station_id):
        return weather_dict.get(station_id)
    else:
        weather_dict[station_id] = gm.get_weather_dict(station_id, start = datetime.datetime(2022, 3, 1), end = datetime.datetime(2023, 4, 9))
        fhf.write_dict_to_json(weather_dict, gen_dir + "/data/created_data/weather/meteostat_weather.json")
        return weather_dict[station_id]



#weather dict and data.csv and 
# Combine the weather data with the existing data
def combine_data(existing_data, weather_data):
    combined_data = []
    for row in existing_data:
        date_time = row['Date Time']
        timestamp = datetime.datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%SZ')
        if timestamp in weather_data:
            weather_row = weather_data[timestamp]
            combined_row = {**row, **weather_row}
            combined_data.append(combined_row)
    return combined_data

# Example: Fetch weather data for a station
# weather_df = fetch_weather_data(station_id, start, end)

# Example: Convert the fetched weather data to a dictionary
# weather_data_dict = convert_weather_data_to_dict(weather_df)

# Combine the existing data with the weather data
# existing_data = read_csv('your_data.csv')
# combined_data = combine_data(existing_data, weather_data_dict)

a = weather_data_update("441531089")

result = uz.read_and_combine_csvs_from_zips(folder_path=gen_dir + "/data/input_data/inrix/SantaClara")
# Your existing data
big_date = result['Date Time'].tolist()
big_seg_id = result['Segment ID'].tolist()
speed = result['Speed(km/hour)'].tolist()
hist_speed = result['Hist Av Speed(km/hour)'].tolist()
ref_speed = result['Ref Speed(km/hour)'].tolist()
road_closure = result["Road Closure"].tolist()
