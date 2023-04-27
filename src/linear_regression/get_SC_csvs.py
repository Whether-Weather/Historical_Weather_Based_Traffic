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
def weather_data_update(segment_id):
    try:
        station_id = seg_to_station[segment_id]

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
    time1 = time.perf_counter()
    dt = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    dt = dt.replace(minute=0, second=0)
    time2 = time.perf_counter()
    print(f"round hour: {time2 - time1}")
    return dt

def combine_data():
    #output_file_path = gen_dir + '/data/created_data/SantaClara/combined_data.csv'
    header_written = False
    input_path = gen_dir + "/data/input_data/inrix/" + county
    #maybe change to read one dataframe at a time
    zip_files = uz.get_zip_files(folder_path= input_path)
    # zip_files = [zip_files[2]]

    
    #'/Users/joshkelleran/SeniorDesign/Whether-Weather/Historical_Weather_Based_Traffic/data/input_data/inrix/SantaClara/santa_clara_2022-12-01_to_2023-03-01_60_min_part_1.zip'
    #zip_files = zip_files[2:]
    output_folder_path = gen_dir + '/data/created_data/' + county  # Replace with your output folder path

    for file in zip_files:
        df = uz.read_csvs_from_zips(files=[file])[0]
        date_list = df['Date Time'].tolist()
        seg_id_list = df['Segment ID'].tolist()
        speed_list = df['Speed(km/hour)'].tolist()
        hist_speed_list = df['Hist Av Speed(km/hour)'].tolist()
        ref_speed_list = df['Ref Speed(km/hour)'].tolist()
        
        combined_data = []
        i = 0
        for date, seg_id, speed, hist_speed, ref_speed in zip(date_list, seg_id_list, speed_list, hist_speed_list, ref_speed_list):
            date_time = round_to_nearest_hour(date)
            date_time_str = date_time.strftime('%Y-%m-%d %H:%M:%S')

            segment_weather_dict = weather_data_update(str(seg_id))
            if segment_weather_dict:
                station_data = segment_weather_dict['times']
                if date_time_str in station_data:
                    time1 = time.perf_counter()
                    weather_data = station_data[date_time_str]
                    combined_data.append({
                        'Date Time': date,
                        'Segment ID': seg_id,
                        'Speed(km/hour)': speed,
                        'Hist Av Speed(km/hour)': hist_speed,
                        'Ref Speed(km/hour)': ref_speed,
                        **weather_data
                    })
                    time2 = time.perf_counter()
                    print(f"combinerow: {time2 - time1}")
            i += 1

        # Write the combined data to a separate CSV file in the output folder
        combined_df = pd.DataFrame(combined_data)
        
        # Create a unique file name using the input file's name
        output_file_name = f"{file.split('/')[-1].split('.')[0]}_combined.pkl"
        output_file_path = f"{output_folder_path}/{output_file_name}"
        
        combined_df.to_pickle(output_file_path)
        combined_df = None


if __name__ == "__main__":
    combine_data()