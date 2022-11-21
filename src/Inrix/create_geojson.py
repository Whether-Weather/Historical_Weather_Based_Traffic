#creates json file which can be displayed through deck.gl

import json
import pandas as pd
from utils import file_helper_functions as fhf

def make_json():
     #get inrix speed data (straight from data downloader)
    # df = pd.read_csv("data/input_data/inrix/washpart1.csv")
    # df2 = pd.read_csv("data/input_data/inrix/washpart2.csv")


    # frames = [df, df2]
    # result = pd.concat(frames)

    # big_date = result['Date Time'].str[:10].tolist()
    # big_seg_id = result['Segment ID'].tolist() 
    # speed = result['Speed(km/hour)'].tolist()
    # hist_speed = result['Hist Av Speed(km/hour)'].tolist()
    # ref_speed = result['Ref Speed(km/hour)'].tolist()

    # total_dates = result['Date Time'].str[:10].drop_duplicates().tolist()
    # fhf.list_to_csv(total_dates, "data/created_data/inrix/list_of_dates.csv")

    total_dates = fhf.csv_to_list("data/created_data/inrix/list_of_dates.csv")

    for i in range(0,len(total_dates)):
        total_dates[i] = total_dates[i][0]

    #print(result.head()) #to show the headers of the file
    #inrix data in speed segments and dates
    #Date Time  Segment ID  Speed(km/hour)  Hist Av Speed(km/hour)  Ref Speed(km/hour) Road Closure
    # 0  2020-11-03T00:00:00-08:00   
    # 1  2020-11-03T01:00:00-08:00   
    #only want the year_month_day 
    # result['Date Time'] = pd.DataFrame(big_date)
    # result = result.drop_duplicates(subset = ['Segment ID', 'Date Time'], keep = 'last').reset_index(drop = True)
    # small_seg_id = result['Segment ID'].tolist() 
    # small_date = result['Date Time'].tolist()

    #segment dictionary
    segment_dict = fhf.get_dict_from_json('data/created_data/inrix/final_all_segments_dict.json')
    #segment date dictionary
    segment_date_dict = fhf.get_dict_from_json('data/created_data/inrix/seg_date_dict.json')
    #weather dictionary
    weather_dict = fhf.get_dict_from_json('data/created_data/weather/all_weather.json')
    #polygons with segments inside dictionary
    polygon_dict = fhf.get_dict_from_json('data/created_data/polygon/polygon_with_coordinates.json')


    big_dict = {'type': 'FeatureCollection'}
    features_array = []

    # error at : "-122.5964,48.1303,2020-12-08": 0.0, so this value was manually added
    #'-122.5964,48.1303,2020-12-17'
    i = 0
    for weather_station in polygon_dict:
        i += 1
        for segment in polygon_dict[weather_station]['segments_inside']:
            features_dict = {'type': 'Feature'}
            speed_list = []
            hist_speed_list = []
            ref_speed_list = []
            weather_list = []
            for date in total_dates:
                properties_dict = {}

                seg_key = str(segment) + "," + str(date)
                weather_key = str(weather_station) + "," + str(date)

                # get values -> should match up by index
                try:
                    speed_list.append(segment_date_dict[seg_key]['speed'])
                    hist_speed_list.append(segment_date_dict[seg_key]['hist_speed'])
                    ref_speed_list.append(segment_date_dict[seg_key]['ref_speed'])
                except:
                    speed_list.append(-1)
                    hist_speed_list.append(-1)
                    ref_speed_list.append(-1)

                try:
                    weather_list.append(weather_dict[weather_key])
                except:
                    weather_list.append(-1)
            properties_dict = {"speeds": speed_list, "hist_speeds": hist_speed_list, 
                "ref_speeds": ref_speed_list, "closest_weather_station": weather_station}
            features_dict['geometry'] = segment_dict[str(segment)]['envelopeString']
            features_dict['properties'] = properties_dict
            features_array.append(features_dict)
    
    big_dict['features'] = features_array

    fhf.write_dict_to_json(big_dict, "data/created_data/create_geojson.json")
            
            



 

if __name__ == "__main__":
    make_json()