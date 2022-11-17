#creates json file which can be displayed through deck.gl

import json
import pandas as pd
from utils import file_helper_functions as fhf

def make_json():


    #get inrix speed data (straight from data downloader)
    df = pd.read_csv("data/input_data/inrix/washpart1.csv")
    df2 = pd.read_csv("data/input_data/inrix/washpart2.csv")


    frames = [df, df2]
    result = pd.concat(frames)

    #print(result.head()) #to show the headers of the file
    #inrix data in speed segments and dates
    #Date Time  Segment ID  Speed(km/hour)  Hist Av Speed(km/hour)  Ref Speed(km/hour) Road Closure
    # 0  2020-11-03T00:00:00-08:00   
    # 1  2020-11-03T01:00:00-08:00   
    #only want the year_month_day 
    seg_id = result['Segment ID'].tolist() 
    date = result['Date Time'].str[:10].tolist()

    #segment dictionary
    segment_dict = fhf.get_dict_from_json('data/created_data/inrix/final_all_segments_dict.json')

    #weather dictionary
    weather_dict = fhf.get_dict_from_json('data/created_data/weather/all_weather.json')

    #polygons with segments inside dictionary
    polygon_dict = fhf.get_dict_from_json('data/created_data/polygon_with_coordinates.json')


    


    big_dict = {'type': 'FeatureCollection'}
    features_array = []
    blabla = 0
    print("start")
    features_dict = {'type': 'Feature'}


    #
    count = 0
    total_dict = {}
        
    big_dict['features'] = features_array

    fhf.write_dict_to_json()
    with open('src/output_data/sep28_big_result.json', 'w') as fp:
        json.dump(big_dict, fp)
    # print(big_dict)

if __name__ == "__main__":
    make_json()