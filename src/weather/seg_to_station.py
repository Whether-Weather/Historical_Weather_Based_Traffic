import sys
from pathlib import Path

from meteostat import Daily, Stations

gen_dir = str(Path(__file__).resolve().parents[2])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)

import time

from geopy.distance import great_circle

from utils import file_helper_functions as fhf

santa_clara_input_coords = (37.3541, -121.9552)



segment_To_Weather = {}
def find_station():
    input_coordinates = santa_clara_input_coords
    # Find 20 closest stations
    stations = Stations()
    nearby_stations = stations.nearby(*input_coordinates)
    closest_20_stations = nearby_stations.fetch(20)

    # Extract station IDs and coordinates into a list
    station_coordinates_list = [
        (station_id, (station_info['latitude'], station_info['longitude']))
        for station_id, station_info in closest_20_stations.iterrows()
    ]
    
    for seg_id in segment_dict:
        closest_station_id = find_closest_station(segment_dict[seg_id], station_coordinates_list)
        segment_To_Weather[seg_id] = closest_station_id
        
# Function to find the closest station from input coordinates
def find_closest_station(input_coords, station_coords_list):
    closest_station = None
    closest_distance = float('inf')

    for station_id, station_coords in station_coords_list:
        distance = great_circle(input_coords, station_coords).km

        if distance < closest_distance:
            closest_distance = distance
            closest_station = station_id

    return closest_station


if __name__ == '__main__':
    segment_dict = fhf.get_dict_from_json(gen_dir + "/data/created_data/inrix/midpoints.json")
    find_station()
    fhf.write_dict_to_json(segment_To_Weather, gen_dir + "/data/created_data/inrix/segid_to_weather.json")