from rtree import index
from shapely.geometry import Point, LineString
from shapely.ops import linemerge
import osmnx as ox
import pandas as pd
import pickle

import time
import sys
from pathlib import Path

gen_dir = str(Path(__file__).resolve().parents[4])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)
from utils import unzip as uz

county = "CookCounty"

try:
    G = ox.io.load_graphml(filepath=gen_dir + "/data/created_data/polygon/" + county + ".osm")
except:
    cook_county = ox.geocode_to_gdf("Cook County, Illinois")

# Build a spatial index for the OSM graph
idx = index.Index()
edge_dict = {}
for i, (u, v, key, data) in enumerate(G.edges(keys=True, data=True)):
    if 'geometry' in data:
        edge_line = data['geometry']
        idx.insert(i, edge_line.bounds)
        edge_dict[i] = (edge_line, (u, v, key))
    else:
        p1 = Point(G.nodes[u]['x'], G.nodes[u]['y'])
        p2 = Point(G.nodes[v]['x'], G.nodes[v]['y'])
        edge_line = LineString([p1, p2])
        idx.insert(i, edge_line.bounds)
        edge_dict[i] = (edge_line, (u, v, key))

def get_route(origin, destination, road_distance):
    # Build a LineString from the origin to the destination
    segment_line = LineString([Point(origin[::-1]), Point(destination[::-1])])

    # Use the spatial index to find intersecting edges
    intersecting_edges = list(idx.intersection(segment_line.bounds))

    # Filter the list by actually checking the intersection of the edges and the segment line
    intersecting_lines = [edge_dict[edge][0] for edge in intersecting_edges if segment_line.intersects(edge_dict[edge][0])]

    # Here you need to decide what to return. It could be the list of intersecting edges,
    # the list of intersecting Lines, or you could try to build a new LineString representing
    # the route by merging the intersecting lines.
    return linemerge(intersecting_lines)

#finish filename and clean up this function to work
def segment_line(filename = gen_dir + '/data/created_data/CookCounty/CookCountyLines.pkl'):
    files = uz.get_zip_files(folder_path= gen_dir + '/data/input_data/inrix/CookCounty')
    dfs = uz.read_csvs_from_zips(name = 'metadata.csv', files=files, 
                                columns_to_keep=['Segment ID', 'Start Latitude', 'Start Longitude', 'End Latitude', 'End Longitude', 'Segment Length(Kilometers)'])
    combined_df = pd.concat(dfs, ignore_index=True)
    df = combined_df.drop_duplicates()
    segments = df['Segment ID'].tolist()
    start_lat = df['Start Latitude'].tolist()
    start_long = df['Start Longitude'].tolist()
    end_lat = df['End Latitude'].tolist()
    end_long = df['End Longitude'].tolist()
    road_distance = df['Segment Length(Kilometers)'].tolist()
    segment_dict = {}
    # try:
    #     with open(filename, "rb") as f:
    #         segment_dict = pickle.load(f)
    # except:
    #     segment_dict = {}
    for i in range(0, len(segments)):
        time1 = time.perf_counter()
        if i % 3000 == 0:
            print(i)
            with open(filename, "wb") as f:
                pickle.dump(segment_dict, f)
        if str(segments[i]) not in segment_dict:
            line = get_route([start_lat[i], start_long[i]],
                    [end_lat[i], end_long[i]],
                    road_distance[i])
            segment_dict[str(segments[i])] = line
        time2 = time.perf_counter()
        print(time2- time1)
    
    with open(filename, "wb") as f:
        pickle.dump(segment_dict, f)   


if __name__ == '__main__':
    segment_line()