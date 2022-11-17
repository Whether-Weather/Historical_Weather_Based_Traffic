#basically asssigns segments to certain weather stations on whether it falls within a polygon

import pandas as pd
import in_polygon as ip
import json
from utils import file_helper_functions as fhf

def new_polygon_dict():
    x = fhf.get_dict_from_json('data/created_data/polygon/formattedpolygondict.json')
    polygon_array = []
    for element in x:
        coordinates_string = element.split(',')
        polygon_array.append(coordinates_string)

    df = pd.read_csv("data/input_data/inrix/washpart1.csv")
    df2 = pd.read_csv("data/input_data/inrix/washpart1.csv")
    frames = [df, df2]
    result = pd.concat(frames)
    result = result.drop_duplicates(subset=['Segment ID'], keep='last').reset_index(drop = True)

    segments = df['jseg_id'].tolist()
    midpoints = df['midpoint'].tolist()
    
    ret_midpoints = []
    for element in midpoints:
        coordinates_str = element.replace(")", "").replace("(", "").split(',')
        coordinates = [float(coordinates_str[0]), float(coordinates_str[1])]
        ret_midpoints.append(coordinates)
    
    new_dict = {}

    j = 0
    for polygon in polygon_array:
        holder_dict = {}
        c_poly = polygon[0] + "," + polygon[1]
        i = 0
        contained_midpoints = []
        contained_segments = []
        while i < len(ret_midpoints):
            if ip.is_it_inside(ret_midpoints[i], x[c_poly]):
                contained_midpoints.append(ret_midpoints.pop(i))
                contained_segments.append(segments.pop(i))
            else:
                i += 1    
        holder_dict['coordinates_inside'] = contained_midpoints
        holder_dict['segments_inside'] = contained_segments
        holder_dict['polygon'] = x[c_poly]
        new_dict[c_poly] = holder_dict
        j += 1
    with open('src/output_data/polygon_with_coordinates.json', 'w') as fp:
        json.dump(new_dict, fp)  


def oct2_get_segment_dict():
    x = titin.get_dict_from_json('src/data/inrix/big_run/sep28_all_segments_dict.json')

    ret_dict = {}
    for element in x:
        break


def seg_geo():
    df = pd.read_csv("src/output_data/sep28testtake2.csv")
    seg_id = df['jseg_id'].tolist()
    date = df['jdate'].tolist()
    midpoints = df['midpoint'].tolist()
    envelope = df['envelope'].tolist()
    speed = df['daily_speed'].tolist()
    speed_ref = df['ref_speed'].tolist()


    ret_midpoints = []
    for element in midpoints:
        coordinates_str = element.replace(")", "").replace("(", "").split(',')
        coordinates = [float(coordinates_str[0]), float(coordinates_str[1])]
        ret_midpoints.append(coordinates)

    ret_dict = {}
    for i in range(0, len(seg_id)):
        holder_dict = {}
        key = str(seg_id[i]) + "," + date[i]
        holder_dict['speed'] = speed[i]
        holder_dict['ref_speed'] = speed_ref[i]
        holder_dict['envelope'] = envelope[i]
        holder_dict['midpoints'] = midpoints[i]
        ret_dict[key] = holder_dict
    with open('src/output_data/segid_date.json', 'w') as fp:
        json.dump(ret_dict, fp)  
    print("hello")

def seg_dates():
    df = pd.read_csv("src/output_data/sep28testtake2.csv")
    seg_id = df['jseg_id'].tolist()
    jdate = df['jdate']
    kdate = jdate.drop_duplicates()
    date = kdate.tolist()
    midpoints = df['midpoint'].tolist()
    envelope = df['envelope'].tolist()
    speed = df['daily_speed'].tolist()
    speed_ref = df['ref_speed'].tolist()

    seg_date_dict = {}
    


    for i in range(0, len(seg_id)):
        holder_dict = {}
        holder_dict['speed'] = speed[i]
        holder_dict['ref_speed'] = speed_ref[i]
        holder_dict['envelope'] = envelope[i]

        dic_key = str(seg_id[i]) + "," + str(date[i])
        seg_date_dict[dic_key] = holder_dict
 
    

if __name__ == "__main__":
    seg_geo()