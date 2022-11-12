import csv
from itertools import count
import pandas as pd
import get_segment_coordinates as gsc
import json
import threading
import queue
import time

q = queue.Queue()

def get_segments(csv_file):
    df = pd.read_csv(csv_file)
    df = df.drop_duplicates(subset=['Segment ID'], keep='last').reset_index(drop = True)
    segments = df['Segment ID']

    segments = segments.values.tolist()
    return segments

def get_all_segments():
    all_segments = []
    for element in get_segments('src/data/inrix/washpart1.csv'):
        all_segments.append(element)
    for element in get_segments('src/data/inrix/washpart2.csv'):
        all_segments.append(element)
    return all_segments


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
    #q.put(adder)
    return adder
    # with open(filename,'r+') as file:
    #     file_data = json.load(file)
    #     file_data.update(adder)
    # with open(filename, 'w') as fp:
    #     json.dump(file_data, fp)


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


def get_size_of_json(filename='src/data/inrix/segment_dict.json'):
    with open(filename,'r') as file:
        file_data = json.load(file)
    
    # for element in file_data:
    #     print(element)
    return len(file_data)

def missing_seg_json(filename='src/data/inrix/missed_segments.csv'):
    df = pd.read_csv(filename)
    segments = df.values.tolist()
    adder = {}
    for element in segments:
        add_segment_to_json_dict(element[0])
        adder.update(q.get())
    with open('src/data/inrix/missed_segments.json', 'w') as fp:
        json.dump(adder, fp)
    

def count_json_files(files=['src/data/inrix/7pm_new_segment_dict.json', 
'src/data/inrix/22650_7pm_new_segment_dict.json', 
'src/data/inrix/33200_7pm_new_segment_dict.json',
'src/data/inrix/49750_7pm_new_segment_dict.json',
'src/data/inrix/63400_7pm_new_segment_dict.json',
'src/data/inrix/74400_7pm_new_segment_dict.json',
'src/data/inrix/85050_7pm_new_segment_dict.json',
'src/data/inrix/95700_7pm_new_segment_dict.json',
'src/data/inrix/missed_segments.json']):
    counter = 0
    for element in files:
        counter += get_size_of_json(filename=element)
    print(counter)

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

def get_segment_def(segment=0, filename='src/data/inrix/sep28_all_segments_dict.json'):
    with open(filename,'r') as file:
        file_data = json.load(file)
    return file_data
    # try:
    #     return file_data[segment]
    # except:
    #     print("ERROR :" + segment)

def add_segment(filename='src/data/inrix/sep28_all_segments_dict.json'):
    x = add_segment_to_json_dict(1236955410)
    with open(filename,'r+') as file:
        file_data = json.load(file)
        file_data.update(x) 
        file.seek(0)
        json.dump(file_data, file)


if __name__ == '__main__':
    print("main:")


    y = get_segment_def()
    tic = time.perf_counter()
    x = y['1236955410']
    toc = time.perf_counter()
    print(x)
    print(f"Downloaded the tutorial in {toc - tic:0.8f} seconds")

    # count_json_files()
    # segment_count()