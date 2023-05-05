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
import pickle



weather_dict = {}
county = 'HarrisCounty'

county_path = gen_dir + '/data/created_data/' + county + '/'

try:
    with open(county_path + county + 'Weather.pkl', "rb") as f:
        weather_dict = pickle.load(f)
except:
    weather_dict = {}
    with open(county_path + county + 'Weather.pkl', "wb") as f:
        pickle.dump(weather_dict, f)



#fhf.get_dict_from_json(gen_dir + "/data/created_data/weather/meteostat_weather_part2.json")
# segment_dict = fhf.get_dict_from_json(gen_dir + "/data/created_data/inrix/midpoints.json")
# seg_to_station = fhf.get_dict_from_json(gen_dir + "/data/created_data/inrix/segid_to_weather.json")
with open(county_path + 'midpoints.pkl', "rb") as f:
    segment_dict = pickle.load(f)

with open(county_path + 'segid_to_weather.pkl', "rb") as f:
    seg_to_station = pickle.load(f)

fault_segments = []

# Convert Meteostat data to a dictionary with timestamps as keys
def weather_data_update(segment_id, i):
    try:
        station_id = seg_to_station[segment_id][i]

        if station_id in weather_dict:
            return weather_dict.get(station_id)
        else:
            weather_dict[station_id] = gm.get_weather_dict(station_id, start = datetime.datetime(2022, 3, 1), end = datetime.datetime(2023, 4, 15))
            with open(county_path + county + 'Weather.pkl', "wb") as f:
                pickle.dump(weather_dict, f)

            return weather_dict[station_id]
    except:
        fault_segments.append(segment_id)

# Convert the date string to a datetime object rounded to the nearest hour
def round_to_nearest_hour(date_str):
    
    dt = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    dt = dt.replace(minute=0, second=0)
    
    return dt

def get_file_name_without_extension(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]
# .replace('_combined', '')

def combine_data():
    header_written = False
    input_path = gen_dir + "/data/input_data/inrix/" + county
    zip_files = uz.get_zip_files(folder_path=input_path)
    # what files do i have already
    output_folder_path = gen_dir + '/data/created_data/' + county + "/combined_data"
    existing_files = uz.get_combined_files(output_folder_path)


    existing_files_names = [get_file_name_without_extension(file_path).replace('_combined', '') for file_path in existing_files]
   
    filtered_zip_files = [file_path for file_path in zip_files if get_file_name_without_extension(file_path) not in existing_files_names]
    
    chunk_size = 20000000  # 5 million rows
    

    for file in filtered_zip_files:
        df = uz.read_csvs_from_zips(files=[file])[0]
        date_list = df['Date Time'].tolist()
        seg_id_list = df['Segment ID'].tolist()
        speed_list = df['Speed(km/hour)'].tolist()
        hist_speed_list = df['Hist Av Speed(km/hour)'].tolist()
        ref_speed_list = df['Ref Speed(km/hour)'].tolist()
        df = None

        combined_data = []

        count = 0
        for date, seg_id, speed, hist_speed, ref_speed in zip(date_list, seg_id_list, speed_list, hist_speed_list, ref_speed_list):
            date_time = round_to_nearest_hour(date)
            date_time_str = date_time.strftime('%Y-%m-%d %H:%M:%S')
            segment_id = str(seg_id)
            
                            
            for i in range(0, len(seg_to_station[segment_id])):

                segment_weather_dict = weather_data_update(segment_id, i)
                if segment_weather_dict:
                    station_data = segment_weather_dict['times']
                    if date_time_str in station_data:

                        weather_data = station_data[date_time_str]
                        combined_data.append({
                            'Date Time': date,
                            'Segment ID': seg_id,
                            'Speed(km/hour)': speed,
                            'Hist Av Speed(km/hour)': hist_speed,
                            'Ref Speed(km/hour)': ref_speed,
                            **weather_data
                        })
                        
                        break
            
            
            
            count += 1
            

            if count % chunk_size == 0:
                combined_df = pd.DataFrame(combined_data)
                output_file_name = f"{file.split('/')[-1].split('.')[0]}_combined.pkl"
                output_file_path = f"{output_folder_path}/{output_file_name}"
                if os.path.isfile(output_file_path):
                    existing_df = pd.read_pickle(output_file_path)
                    combined_df = pd.concat([existing_df, combined_df], ignore_index=True)
                combined_df.to_pickle(output_file_path)
                combined_data = []
                combined_df = None

        if combined_data:
            combined_df = pd.DataFrame(combined_data)
            output_file_name = f"{file.split('/')[-1].split('.')[0]}_combined.pkl"
            output_file_path = f"{output_folder_path}/{output_file_name}"
            if os.path.isfile(output_file_path):
                existing_df = pd.read_pickle(output_file_path)
                combined_df = pd.concat([existing_df, combined_df], ignore_index=True)
            combined_df.to_pickle(output_file_path)



if __name__ == "__main__":
    combine_data()