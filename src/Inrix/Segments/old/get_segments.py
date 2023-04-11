#creates the segment dictionary
#now the segments can be loaded using
    #ex: y = fhf.get_dict_from_json('data/created_data/inrix/final_all_segments_dict.json')
###might want to modify r+ for efficiency

import csv
import pandas as pd
import get_segment_coordinates as gsc
import json
import threading
import queue
import time

from utils import file_helper_functions as fhf


q = queue.Queue()

#get segment helper function
#might be from manipulated file
def get_segments(csv_file):
    df = pd.read_csv(csv_file)
    df = df.drop_duplicates(subset=['Segment ID'], keep='last').reset_index(drop = True)
    segments = df['Segment ID']

    segments = segments.values.tolist()
    return segments

#lists out all segments
#washpart1 and 2 are orignal inrix traffic data
def get_all_segments():
    all_segments = []
    for element in get_segments('src/data/inrix/washpart1.csv'):
        all_segments.append(element)
    for element in get_segments('src/data/inrix/washpart2.csv'):
        all_segments.append(element)
    return all_segments


#thread helper function
#ex:
    # "1236897942": {
    #     "envelopeString": "{\"type\":\"LineString\",\"coordinates\":[[-123.706314582595,46.6762053236514],[-123.696127495094,46.6762053236514],[-123.696127495094,46.670113121419],[-123.706314582595,46.670113121419],[-123.706314582595,46.6762053236514]]}",
    #     "startLatitude": 46.67620532365142,
    #     "startLongitude": -123.7063145825951,
    #     "endLatitude": 46.67011312141902,
    #     "endLongitude": -123.69612749509365
    #   },
def add_segment_to_json_dict(segment, filename='src/data/inrix/new_segment_dict.json'):
    adder = {}
    holder = {}
    response = {}
    response = gsc.get_coordinates(segment)
    if not response: return
    holder['envelopeString'] = response['envelopeString']
    holder['startLatitude'] = response['details'][0]['startLatitude']
    holder['startLongitude'] = response['details'][0]['startLongitude']
    holder['endLatitude'] = response['details'][0]['endLatitude']
    holder['endLongitude'] = response['details'][0]['endLongitude']

    adder[segment] = holder
    return adder
   


#probably have to change r+ to just w and write it all as one big data structure -> takes longer and longer to run after around 10k segments
# @95700 because I ran in groups just cause I was busy
# has array of what add_segment_to_json_dict
def segment_json_multithread(filename='src/data/inrix/95700_7pm_new_segment_dict.json'):
    df = pd.read_csv('src/data/inrix/all_segments.csv')
    segments = df.values.tolist()
    j = 95700
    #0,22650,33200,49750,63400, 74400, 85050,95700
    while j < len(segments):
        threads = []
        if len(segments) - j < 50:
            the_range = len(segments) - j
        else: the_range = 50
        for i in range(the_range):
            t = threading.Thread(target=add_segment_to_json_dict, args=(segments[j + i][0],))
            t.daemon = True
            threads.append(t)
        
        for i in range(the_range):
            threads[i].start()
        
        for i in range(the_range):
            threads[i].join()
        
        adder = {}
        for i in range(q.qsize()):
            adder.update(q.get())
        with open(filename,'r+') as file:
            file_data = json.load(file)
            file_data.update(adder) 
            file.seek(0)
            json.dump(file_data, file)
        j += 50

#to help missing segments
def missing_seg_json(filename='src/data/inrix/missed_segments.csv'):
    df = pd.read_csv(filename)
    segments = df.values.tolist()
    adder = {}
    for element in segments:
        add_segment_to_json_dict(element[0])
        adder.update(q.get())
    with open('src/data/inrix/missed_segments.json', 'w') as fp:
        json.dump(adder, fp)
    
# since i used r+ when creating it got really slow after around 10k segments, should just switch to w after getting all segments into {}
def combine_json_files(files=['src/data/inrix/7pm_new_segment_dict.json', 
'src/data/inrix/22650_7pm_new_segment_dict.json', 
'src/data/inrix/33200_7pm_new_segment_dict.json',
'src/data/inrix/49750_7pm_new_segment_dict.json',
'src/data/inrix/63400_7pm_new_segment_dict.json',
'src/data/inrix/74400_7pm_new_segment_dict.json',
'src/data/inrix/85050_7pm_new_segment_dict.json',
'src/data/inrix/95700_7pm_new_segment_dict.json',
'src/data/inrix/missed_segments.json']):
    adder = {}
    for filename in files:
        with open(filename,'r') as file:
            file_data = json.load(file)
            adder.update(file_data)
    with open('src/data/inrix/sep28_all_segments_dict.json', 'w') as fp:
        json.dump(adder, fp)

#missed segment for some reason so i added it manually
def add_segment(filename='src/data/inrix/sep28_all_segments_dict.json'):
    x = add_segment_to_json_dict(1236955410)
    with open(filename,'r+') as file:
        file_data = json.load(file)
        file_data.update(x) 
        file.seek(0)
        json.dump(file_data, file)


if __name__ == '__main__':
    print("main:")

    #reads segment dictionary
    y = fhf.get_dict_from_json('data/created_data/inrix/final_all_segments_dict.json')
    tic = time.perf_counter()
    x = y['1236955410']
    toc = time.perf_counter()
    print(x)
    print(f"Downloaded the tutorial in {toc - tic:0.8f} seconds")

    # count_json_files()
    # segment_count()