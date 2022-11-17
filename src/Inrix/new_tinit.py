import json
import numpy as np
import pandas as pd
import ast
import time
from utils import file_helper_functions as fhf


def get_weather_array():
    df_weather = pd.read_csv("src/data/weather/new_weather_data.csv")
    lat_column = df_weather['LATITUDE'].tolist()
    long_column = df_weather['LONGITUDE'].tolist()
    weather_array = []
    for i in range(0,len(lat_column)):
        weather_array.append([long_column[i], lat_column[i]])
    return weather_array

def get_midpoints():
    df = pd.read_csv("src/output_data/sep28testtake2.csv")
    midpoints = df['midpoint'].tolist()
    ret_midpoints = []
    for element in midpoints:
        coordinates_str = element.replace(")", "").replace("(", "").split(',')
        coordinates = [float(coordinates_str[0]), float(coordinates_str[1])]
        ret_midpoints.append(coordinates)
    
    return ret_midpoints

        

def big_result():
    df = pd.read_csv("src/output_data/sep28testtake2.csv")
    seg_id = df['jseg_id'].tolist()
    date = df['jdate'].drop_duplicates().tolist()
    midpoints = df['midpoint'].tolist()
    envelope = df['envelope'].tolist()
    speed = df['daily_speed'].tolist()
    speed_ref = df['ref_speed'].tolist()


    seg_date_dict = fhf.get_dict_from_json('src/output_data/segid_date.json')

    

    df_weather = pd.read_csv("src/data/730_weather_array.csv")
    lat_column = df_weather['lat'].tolist()
    long_column = df_weather['long'].tolist()
    precipitation = df_weather['precip'].tolist()
    weather_date = df_weather['date'].tolist()

    weather_dict = fhf.get_dict_from_json('src/data/weather/all_weather.json')

    polygon_dict = fhf.get_dict_from_json('src/output_data/polygon_with_coordinates.json')

    big_dict = {'type': 'FeatureCollection'}
    features_array = []
    blabla = 0
    print("start")
        
        
    
    features_dict = {'type': 'Feature'}


    #
    count = 0
    total_dict = {}
    for element in polygon_dict:
        new_key = polygon_dict[element] 
        segments_arr = new_key['segments_inside']
        for j in range(0, len(segments_arr)):
            
            for k in range(0, len(date)):
                properties_dict = {}
                seg_key = str(segments_arr[j]) + "," + str(date[k])
                try:
                    properties_dict['speed'] = seg_date_dict[seg_key]['speed']
                    properties_dict['speed_ref'] = seg_date_dict[seg_key]['ref_speed']
                except:
                    print(seg_key)
                properties_dict['closest_weather_station'] = element
                try:
                    properties_dict['rain'] = weather_dict[element + "," + str(date[k])]
                except:
                    properties_dict['rain'] = -1
                total_dict[seg_key] = properties_dict
                count += 1
    with open('src/output_data/oct11_all_data.json', 'w') as fp:
        json.dump(total_dict, fp)
    #
    print(count)
    tic = time.perf_counter()
    for polygon in polygon_dict:
        c_poly = polygon[0] + "," + polygon[1]
        
        for i in range(0,len(coordinates_arr)):
        
            

            
            seg_date_dict[dic_key]
            
            try:
                properties_dict['rain'] = weather_dict[c_poly + "," + date[i]]
        
            except:
                properties_dict['rain'] = -1
                blabla += 1
        features_dict['geometry'] = ast.literal_eval(envelope[i])
        features_dict['properties'] = properties_dict
        break
        toc = time.perf_counter()
        z = toc - tic
        try:
            properties_dict['rain'] = weather_dict[str(x[0]) + "," + str(x[1]) + "," + date[i]]
        except:
            properties_dict['rain'] = -1
            blabla += 1
        features_dict['geometry'] = ast.literal_eval(envelope[i])
        features_dict['properties'] = properties_dict
            # print(coordinates_string[0] + "," + coordinates_string[1] + "," + date[i])
                 
        features_array.append(features_dict)
        if i > 1000:
            t2_stop = time.perf_counter()
            time_count = t2_stop-t1_start
            time_run_all = (len(midpoints) / 1000) * time_count
            print("time " + "0" + ": " + str(time_count) + " : " + str(time_run_all / 60))
        
    big_dict['features'] = features_array
    with open('src/output_data/sep28_big_result.json', 'w') as fp:
        json.dump(big_dict, fp)
    # print(big_dict)

if __name__ == "__main__":
    big_result()