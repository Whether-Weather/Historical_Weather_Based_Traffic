import pandas as pd
import json


import math

import sys
from pathlib import Path

gen_dir = str(Path(__file__).resolve().parents[3])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)


from utils import unzip as uz
from utils import file_helper_functions as fhf 



def segid_date_jsonfile():
    #get inrix speed data (straight from data downloader)
    result = uz.read_and_combine_csvs_from_zips(folder_path=gen_dir + "/data/input_data/inrix/SantaClara") #currently everything is defaulted

    big_date = result['Date Time'].tolist()
    
    big_seg_id = result['Segment ID'].tolist() 
    
    speed = result['Speed(km/hour)'].tolist()
    
    hist_speed = result['Hist Av Speed(km/hour)'].tolist()
    
    ref_speed = result['Ref Speed(km/hour)'].tolist()
    
    road_closure = result["Road Closure"].tolist()
   
   #weather_id


    #print(result.head()) #to show the headers of the file
    #inrix data in speed segments and dates
    #Date Time  Segment ID  Speed(km/hour)  Hist Av Speed(km/hour)  Ref Speed(km/hour) Road Closure
    # 0  2020-11-03T00:00:00-08:00   
    # 1  2020-11-03T01:00:00-08:00   
    #only want the year_month_day 
    

    result_dict = {}

    for i in range(len(big_seg_id)):
        seg_id = big_seg_id[i]
        date_time = big_date[i]
        speed_value = speed[i]
        hist_speed_value = hist_speed[i]
        ref_speed_value = ref_speed[i]

        if seg_id not in result_dict:
            result_dict[seg_id] = {
                'times': {},
                'ref_speed': ref_speed_value
            }

        result_dict[seg_id]['times'][date_time] = {
            'speed': speed_value,
            'hist_speed': hist_speed_value
        }

    fhf.write_dict_to_json(result_dict, "/Users/joshkelleran/SeniorDesign/Whether-Weather/Historical_Weather_Based_Traffic/data/created_data/inrix/Apr12_dict.json")


        
if __name__ == "__main__":
    segid_date_jsonfile()