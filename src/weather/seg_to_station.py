import sys
from pathlib import Path

from meteostat import Daily, Stations

gen_dir = str(Path(__file__).resolve().parents[2])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)

import time

from geopy.distance import great_circle

from utils import file_helper_functions as fhf
import pickle

santa_clara_input_coords = (37.3541, -121.9552)
seattle_input_coords = (47.6062, -122.3321)
harris_county_input_coords = (29.7752, -95.3103)
county = 'HarrisCounty'

segment_To_Weather = {}
def find_station():
    input_coordinates = harris_county_input_coords
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
        closest_station_id = find_closest_stations(segment_dict[seg_id], station_coordinates_list)
        segment_To_Weather[seg_id] = closest_station_id
        
# Function to find the closest station from input coordinates
def find_closest_stations(input_coords, station_coords_list):
    distances = []

    for station_id, station_coords in station_coords_list:
        distance = great_circle(input_coords, station_coords).km
        distances.append((station_id, distance))

    # Sort the list by the distance (element at index 1 in each tuple)
    sorted_distances = sorted(distances, key=lambda x: x[1])

    # Extract station_ids from the sorted list
    sorted_station_ids = [station_id for station_id, _ in sorted_distances]

    return sorted_station_ids


if __name__ == '__main__':
    # segment_dict = fhf.get_dict_from_json(gen_dir + "/data/created_data/input_data/inrix/midpoints_seattle.json")
    segment_dict = {}
    midpoints_file = gen_dir + '/data/created_data/' + county + '/midpoints.pkl'
    with open(midpoints_file, "rb") as f:
        segment_dict = pickle.load(f)

    find_station()
    with open(gen_dir + '/data/created_data/' + county + '/segid_to_weather.pkl', "wb") as f:
        pickle.dump(segment_To_Weather, f)
    #fhf.write_dict_to_json(segment_To_Weather, gen_dir + "/data/created_data/input_data/inrix/Seattle/segid_to_weather.json")