import json
import pandas as pd
import ast
import threading
import queue
import time
import file_helper_functions as fhp
from ..polygon import in_polygon as ip

q = queue.Queue()
weather_dict = fhp.get_dict_from_json('src/data/weather/all_weather.json')



def multithread_helper(coord_element, x, seg_id, speed, speed_ref, lat_column, long_column, weather_date, date, precipitation, envelope):
    properties_dict = {}
    features_dict = {'type': 'Feature'}
    coordinates_str = coord_element.replace(")", "").replace("(", "").split(',')
    coordinates = [float(coordinates_str[0]), float(coordinates_str[1])]
    for thing in x:
        coordinates_string = thing.split(',')
        test = x[thing]
        if ip.is_it_inside(coordinates, x[thing]):
            properties_dict['seg_id'] = seg_id
            properties_dict['speed'] = speed
            properties_dict['speed_ref'] = speed_ref
            features_dict['geometry'] = ast.literal_eval(envelope)
            features_dict['properties'] = properties_dict
            try:
                    properties_dict['rain'] = weather_dict[coordinates_string[0] + "," + coordinates_string[1] + "," + date[i]]
                    break
            except:
                properties_dict['rain'] = -1
                break
    q.put(features_dict)
    #features_array.append(features_dict)

def final_func_multithread(filename='src/output_data/sep28_big_result.json'):
    df = pd.read_csv("src/output_data/sep28testtake2.csv")
    seg_id = df['jseg_id'].tolist()
    date = df['jdate'].tolist()
    midpoints = df['midpoint'].tolist()
    envelope = df['envelope'].tolist()
    speed = df['daily_speed'].tolist()
    speed_ref = df['ref_speed'].tolist()

    df_weather = pd.read_csv("src/data/730_weather_array.csv")
    lat_column = df_weather['lat'].tolist()
    long_column = df_weather['long'].tolist()
    precipitation = df_weather['precip'].tolist()
    weather_date = df_weather['date'].tolist()

    weather_array = []
    # weather_dict = titin.get_dict_from_json('src/data/weather/all_weather.json')


    tester = len(weather_array)
    tester2 = len(long_column)

    x = titin.get_dict_from_json('src/data/weather/formattedpolygondict.json')

    big_dict = {'type': 'FeatureCollection'}
    features_array = []
    j = 0
    thread_count = 3
    t1_start = time.perf_counter()
    while j < len(midpoints):
        
        threads = []
        if len(midpoints) - j < thread_count:
            the_range = len(midpoints) - j
        else: the_range = thread_count
        for i in range(the_range):
            t = threading.Thread(target=multithread_helper, args=(midpoints[j+i], 
                        x, seg_id[j+i], speed[j+i], speed_ref[j+i], lat_column, long_column, 
                        weather_date, date[j+i], precipitation, envelope[j+i],))
            t.daemon = True
            threads.append(t)
        
        for i in range(the_range):
            threads[i].start()
        
        for i in range(the_range):
            threads[i].join()
        
        adder = {}
        for i in range(q.qsize()):
            features_array.append(q.get())
        j += thread_count
        if j > 1000:
            t2_stop = time.perf_counter()
            time_count = t2_stop-t1_start
            time_run_all = (len(midpoints) / 1000) * time_count
            print("time " + str(thread_count) + ": " + str(time_count) + " : " + str(time_run_all / 60))
             #+ " : " + str((t2_stop-t1_start)/ thread_count))

    big_dict['features'] = features_array
    with open('src/output_data/sep28_big_result.json', 'w') as fp:
        json.dump(big_dict, fp)

if __name__ == '__main__':
    final_func_multithread()