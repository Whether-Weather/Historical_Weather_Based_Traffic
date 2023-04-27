import osmnx as ox
import pandas as pd
import taxicab as tc
import sys
from pathlib import Path
import pickle
from shapely.geometry import LineString
from shapely.ops import linemerge
import random


gen_dir = str(Path(__file__).resolve().parents[4])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)

from utils import unzip as uz

county = 'HarrisCounty'
input_path = gen_dir + '/data/created_data/' + county + '/'
output_path = gen_dir + '/data/created_data/' + county + '/'

osm_path = gen_dir + '/data/created_data/polygon/harriscounty.osm'
missing_segment_dict = {}


try:
    G = ox.io.load_graphml(filepath=osm_path)
except:
    harris_county = ox.geocode_to_gdf("Harris County, Texas")

# Get the street network for Harris County, Texas
    G = ox.graph_from_polygon(harris_county.unary_union, network_type='drive', simplify=False)
    # G = ox.graph_from_bbox(ymax, ymin, xmax, xmin, network_type='drive', simplify=False)
    ox.io.save_graphml(G, filepath=osm_path)



def get_route(origin, destination, segment_id, road_distance, plot=0, margin=0.02, max_attempts=10):
    def apply_offset(coord, offset):
        return coord[0] + random.uniform(-offset, offset), coord[1] + random.uniform(-offset, offset)

    road_distance = road_distance * 1000
    attempt = 0
    offset = 0.001

    while attempt < max_attempts:
        attempt += 1

        # Apply a random offset to the origin and destination coordinates
        offset_origin = apply_offset(origin, offset)
        offset_destination = apply_offset(destination, offset)

        # Calculate the mid-point of the offset origin and destination coordinates
        mid_point = ((offset_origin[0] + offset_destination[0]) / 2, (offset_origin[1] + offset_destination[1]) / 2)

        # Define the bounding box based on the mid-point coordinates with a fixed margin
        xmin, xmax = mid_point[1] - margin, mid_point[1] + margin
        ymin, ymax = mid_point[0] - margin, mid_point[0] + margin

        # Extract the subgraph within the bounding box
        nodes_subset = [node for node, data in G.nodes(data=True) if ymin <= data['y'] <= ymax and xmin <= data['x'] <= xmax]
        G_subgraph = G.subgraph(nodes_subset).copy()

        # Calculate the shortest path using A* algorithm
        ori = ox.distance.nearest_nodes(G_subgraph, X=offset_origin[1], Y=offset_origin[0])
        dest = ox.distance.nearest_nodes(G_subgraph, X=offset_destination[1], Y=offset_destination[0])
        shortest_path = ox.shortest_path(G_subgraph, ori, dest, weight='length')

        linestrings = []
        total_distance = 0
        if shortest_path:
            for i in range(len(shortest_path) - 1):
                u, v = shortest_path[i], shortest_path[i + 1]
                u_coord = G_subgraph.nodes[u]['y'], G_subgraph.nodes[u]['x']
                v_coord = G_subgraph.nodes[v]['y'], G_subgraph.nodes[v]['x']
                linestring = LineString([u_coord, v_coord])
                linestrings.append(linestring)

                edge_data = G.get_edge_data(u, v)
                for _, data in edge_data.items():
                    total_distance += data['length']

        # Check if the total distance is within 30 meters of the road_distance
        if abs(total_distance - road_distance) <= 30:
            print(f'Measured: {total_distance} Actual: {road_distance}')
            merged_line = linemerge(linestrings)
            return merged_line

        # Increase the offset for the next attempt
        offset *= 1.5

    print(f"Could not find a path within 30 meters after {max_attempts} attempts.")
    return None



def correct_lines(filename = output_path + 'wrong_segment_line_dict'):
    df2 = pd.read_csv(input_path + 'wrong_segments.csv')
    segments = df2['0'].tolist()
    road = df2['1'].tolist()
    route = df2['2'].tolist()


    files = uz.get_zip_files(folder_path= gen_dir + '/data/input_data/inrix/HarrisCounty')
    df = uz.read_csvs_from_zips(name = 'metadata.csv', files=files, 
                                columns_to_keep=['Segment ID', 'Start Latitude', 'Start Longitude', 'End Latitude', 'End Longitude', 'Segment Length(Kilometers)'])[0]
    segment_data = {
    segment_id: {
        'Start Latitude': start_lat,
        'Start Longitude': start_long,
        'End Latitude': end_lat,
        'End Longitude': end_long,
        'Segment Length(Kilometers)': road_dist
    }
    for segment_id, start_lat, start_long, end_lat, end_long, road_dist in zip(
        df['Segment ID'],
        df['Start Latitude'],
        df['Start Longitude'],
        df['End Latitude'],
        df['End Longitude'],
        df['Segment Length(Kilometers)']
    )
    }

    for i in range(0, len(segments)):
        # time1 = time.perf_counter()
        if route[i] > (road[i] + 30):
            line = get_route([segment_data[segments[i]]['Start Latitude'], segment_data[segments[i]]['Start Longitude']],
                    [segment_data[segments[i]]['End Latitude'], segment_data[segments[i]]['End Longitude']],
                    segments[i],
                    segment_data[segments[i]]['Segment Length(Kilometers)'])
            missing_segment_dict[str(segments[i])] = line
        
    
    with open(filename, "wb") as f:
        pickle.dump(missing_segment_dict, f)

if __name__ == '__main__':
    correct_lines()