import pandas as pd
from src.polygon import in_polygon as ip
import json
from utils import file_helper_functions as fhf
import get_segment_coordinates as gsc
import math


def segid_date_jsonfile():
     #get inrix speed data (straight from data downloader)
    df = pd.read_csv("data/input_data/inrix/washpart1.csv")
    df2 = pd.read_csv("data/input_data/inrix/washpart2.csv")


    frames = [df, df2]
    result = pd.concat(frames)

    big_date = result['Date Time'].str[:10].tolist()
    big_seg_id = result['Segment ID'].tolist() 
    speed = result['Speed(km/hour)'].tolist()
    hist_speed = result['Hist Av Speed(km/hour)'].tolist()
    ref_speed = result['Ref Speed(km/hour)'].tolist()

    #print(result.head()) #to show the headers of the file
    #inrix data in speed segments and dates
    #Date Time  Segment ID  Speed(km/hour)  Hist Av Speed(km/hour)  Ref Speed(km/hour) Road Closure
    # 0  2020-11-03T00:00:00-08:00   
    # 1  2020-11-03T01:00:00-08:00   
    #only want the year_month_day 
    result['Date Time'] = pd.DataFrame(big_date)
    result = result.drop_duplicates(subset = ['Segment ID', 'Date Time'], keep = 'last').reset_index(drop = True)

    date_holder = ""
    seg_id_holder = ""
    
    #0 count
    #1 speed
    #2 hist speed
    #3 ref_speed
    speeds = [0,0,0,0] 
    
    speed_date_dict = {}

    speed_nan = 0
    hist_speed_nan = 0
    ref_speed_nan = 0
    for i in range(0, len(big_seg_id)):
        if not date_holder and not seg_id_holder:
            date_holder = big_date[i]
            seg_id_holder = big_seg_id[i]
        elif big_date[i] != date_holder or big_seg_id[i] != seg_id_holder:
        
            speed_dict = {}
            
            if (speeds[0] - speed_nan) == 0: speed_dict['speed'] = -1
            else: speed_dict['speed'] = speeds[1]/(speeds[0] - speed_nan)

            if (speeds[0] - hist_speed_nan) == 0: speed_dict['hist_speed'] = -1
            else: speed_dict['hist_speed'] = speeds[2]/(speeds[0] - hist_speed_nan)

            if (speeds[0] - ref_speed_nan) == 0: speed_dict['ref_speed'] = -1
            else: speed_dict['ref_speed'] = speeds[3]/(speeds[0] - ref_speed_nan)
        


            dict_key = str(seg_id_holder) + "," + str(date_holder)
            speed_date_dict[dict_key] = speed_dict

            date_holder = None
            seg_id_holder = None
            speeds = [0,0,0,0]
            speed_nan = 0
            hist_speed_nan = 0
            ref_speed_nan = 0
        
        
        if math.isnan(speed[i]):
            speed_nan += 1
        else:
            speeds[1] += speed[i] #df['Speed(km/hour)'][i]
        if math.isnan(hist_speed[i]):
            hist_speed_nan += 1
        else:
            speeds[2] += hist_speed[i] #df['Hist Av Speed(km/hour)'][i]
        if math.isnan(ref_speed[i]):
            ref_speed_nan += 1
        else:
            speeds[3] += ref_speed[i] #df['Ref Speed(km/hour)'][i]
        
        speeds[0] += 1
            

    fhf.write_dict_to_json(speed_date_dict, "data/created_data/inrix/seg_date_dict.json")



    #run through all entries in segment_dict to get midpoints
    #ex: print(gsc.get_midpoint(segment_dict[segment]))
    # midpoints = []
    # for segment in segment_dict:
    #     coordinates_str = gsc.get_midpoint(segment_dict[segment]).replace(")", "").replace("(", "").split(',')
    #     coordinates = [float(coordinates_str[0]), float(coordinates_str[1])]
    #     midpoints.append(coordinates)
    
    # ret_dict = {}
    # for i in range(0, len(seg_id)):
    #     holder_dict = {}
    #     key = str(seg_id[i]) + "," + date[i]
    #     holder_dict['speed'] = speed[i]
    #     holder_dict['ref_speed'] = speed_ref[i]
    #     holder_dict['envelope'] = envelope[i]
    #     holder_dict['midpoints'] = midpoints[i]
    #     ret_dict[key] = holder_dict
    # with open('src/output_data/segid_date.json', 'w') as fp:
    #     json.dump(ret_dict, fp)  

        
if __name__ == "__main__":
    segid_date_jsonfile()