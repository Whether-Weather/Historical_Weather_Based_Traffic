import os
import json
import datetime
import pandas as pd
from meteostat import Stations, Daily
import sys
from pathlib import Path
import time

gen_dir = str(Path(__file__).resolve().parents[2])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)


from utils import unzip as uz
from utils import file_helper_functions as fhf
from src.weather import getMeteostat as gm

import datetime

weather_dict = fhf.get_dict_from_json(gen_dir + "/data/created_data/weather/meteostat_weather.json")
segment_dict = fhf.get_dict_from_json(gen_dir + "/data/created_data/inrix/midpoints.json")
seg_to_station = fhf.get_dict_from_json(gen_dir + "/data/created_data/inrix/segid_to_weather.json")

fault_segments = []

# Convert Meteostat data to a dictionary with timestamps as keys
def weather_data_update(segment_id):
    try:
        station_id = seg_to_station[segment_id]

        if station_id in weather_dict:
            return weather_dict.get(station_id)
        else:
            weather_dict[station_id] = gm.get_weather_dict(station_id, start = datetime.datetime(2022, 3, 1), end = datetime.datetime(2023, 4, 9))
            fhf.write_dict_to_json(weather_dict, gen_dir + "/data/created_data/weather/meteostat_weather.json")
            return weather_dict[station_id]
    except:
        fault_segments.append(segment_id)


# Convert the date string to a datetime object rounded to the nearest hour
def round_to_nearest_hour(date_str):
    dt = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    dt = dt.replace(minute=0, second=0)
    return dt

def combine_data():
    result = uz.read_and_combine_csvs_from_zips(folder_path=gen_dir + "/data/input_data/inrix/SantaClara")
    # Your existing data
    date_list = result['Date Time'].tolist()
    seg_id_list = result['Segment ID'].tolist()
    speed_list = result['Speed(km/hour)'].tolist()
    # Combine the traffic data with the weather data from weather_dict
    combined_data = []
    i = 0
    for date, seg_id, speed in zip(date_list, seg_id_list, speed_list):
        i += 1
        date_time = round_to_nearest_hour(date)
        date_time_str = date_time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Get the weather data for the current segment_id
        
        segment_weather_dict = weather_data_update(str(seg_id))
        
    
        if segment_weather_dict:
            station_data = segment_weather_dict['times']
            if date_time_str in station_data:
                weather_data = station_data[date_time_str]
                combined_data.append({
                    'Date Time': date,
                    'Segment ID': seg_id,
                    'Speed(km/hour)': speed,
                    **weather_data
                })        

    # Write the combined data to a CSV file
    combined_df = pd.DataFrame(combined_data)
    combined_df.to_csv(gen_dir + '/data/created_data/combined_data.csv', index=False)
    fault_segments.to_csv(gen_dir + '/data/created_data/fault_segments.csv', index=False)



if __name__ == "__main__":
    combine_data()