import osmnx as ox
import pandas as pd
import taxicab as tc
from shapely.geometry import LineString
from shapely.ops import linemerge
import sys
from pathlib import Path
import time
import threading
import queue
import json
import multiprocessing
import pickle

gen_dir = str(Path(__file__).resolve().parents[4])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)


from utils import unzip as uz
from utils import file_helper_functions as fhf

q = queue.Queue()

# xmin, xmax = min(origin[1], destination[1]) - margin, max(origin[1], destination[1]) + margin
# ymin, ymax = min(origin[0], destination[0]) - margin, max(origin[0], destination[0]) + margin
#-122.307497,36.904933,-121.343447,37.510866
xmax = -121.213536
xmin = -122.307497
ymin = 36.894565
ymax = 37.884195

try:
    G = ox.io.load_graphml(filepath=gen_dir + '/data/created_data/polygon/santaclara.osm')
except:
    G = ox.graph_from_bbox(ymax, ymin, xmax, xmin, network_type='drive', simplify=False)
    ox.io.save_graphml(G, filepath=gen_dir + '/data/created_data/polygon/santaclara.osm')

seg_id_off = []

#should write code that if length doesnt match then it should increase margin
def get_route(origin, destination, segment_id, road_distance, plot = 0, margin=0.02):
    # Define the bounding box based on origin and destination coordinates with a margin
    xmin, xmax = min(origin[1], destination[1]) - margin, max(origin[1], destination[1]) + margin
    ymin, ymax = min(origin[0], destination[0]) - margin, max(origin[0], destination[0]) + margin
    
    # Extract the subgraph within the bounding box
    nodes_subset = [node for node, data in G.nodes(data=True) if ymin <= data['y'] <= ymax and xmin <= data['x'] <= xmax]
    G_subgraph = G.subgraph(nodes_subset).copy()

    road_distance = road_distance * 1000
    route_distance = 0
    route = None
    linestrings = []
    # Get the graph within the bounding box
    while route_distance - 4 > road_distance or route_distance + 4 < road_distance:
        if margin > .2:
            seg_id_off.append([segment_id, road_distance, route_distance])
            break

        # Calculate the shortest path
        # 2. Find the shortest path between two nodes
        ori = ox.distance.nearest_nodes(G_subgraph, X=origin[1], Y=origin[0])
        dest = ox.distance.nearest_nodes(G_subgraph, X=destination[1], Y=destination[0])
        shortest_path = ox.shortest_path(G_subgraph, ori, dest)

        # 3. Extract the edges from the graph along the shortest path
        #edges = ox.utils_graph.get_route_edge_attributes(G_subgraph, shortest_path, attribute='geometry')

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
                

        # route = tc.distance.shortest_path(G_subgraph, origin, destination)
        route_distance = total_distance
        margin = margin * 2


    
    merged_line = linemerge(linestrings)
    
    return merged_line

    # Plot the graph with the route
    if plot:
        tc.plot.plot_graph_route(G, route)

    #return route
    merged_line = linemerge(route[2:])
    return LineString(merged_line)
    
    # segment_dict = {}
    # segment_dict[str(segment_id)] = merged_line
    # return segment_dict



def get_polygon_dictionary(filename = gen_dir + '/data/created_data/polygon/line_polygon_dict.json'):
    files = uz.get_zip_files()[:1]
    df = uz.read_csvs_from_zips(name = 'metadata.csv', files=files, 
                                columns_to_keep=['Segment ID', 'Start Latitude', 'Start Longitude', 'End Latitude', 'End Longitude', 'Segment Length(Kilometers)'])[0]
    segments = df['Segment ID'].tolist()
    start_lat = df['Start Latitude'].tolist()
    start_long = df['Start Longitude'].tolist()
    end_lat = df['End Latitude'].tolist()
    end_long = df['End Longitude'].tolist()
    road_distance = df['Segment Length(Kilometers)'].tolist()




#finish filename and clean up this function to work
def segment_line(filename = gen_dir + '/data/created_data/polygon/line_polygon_dict.pkl'):
    files = uz.get_zip_files()[:1]
    df = uz.read_csvs_from_zips(name = 'metadata.csv', files=files, 
                                columns_to_keep=['Segment ID', 'Start Latitude', 'Start Longitude', 'End Latitude', 'End Longitude', 'Segment Length(Kilometers)'])[0]
    segments = df['Segment ID'].tolist()
    start_lat = df['Start Latitude'].tolist()
    start_long = df['Start Longitude'].tolist()
    end_lat = df['End Latitude'].tolist()
    end_long = df['End Longitude'].tolist()
    road_distance = df['Segment Length(Kilometers)'].tolist()
    segment_dict = {}
    with open(filename, "rb") as f:
        segment_dict = pickle.load(f)
    for i in range(0, len(segments)):
        # time1 = time.perf_counter()
        if i % 3000 == 0:
            print("hi")
            # with open(filename, "wb") as f:
            #     pickle.dump(segment_dict, f)
        if str(segments[i]) not in segment_dict:
            line = get_route([start_lat[i], start_long[i]],
                    [end_lat[i], end_long[i]],
                    segments[i],
                    road_distance[i])
            segment_dict[str(segments[i])] = line
        # time2 = time.perf_counter()
        # print(time2- time1)
    
    with open(filename, "wb") as f:
        pickle.dump(segment_dict, f)
    pd.DataFrame(seg_id_off).to_csv(gen_dir + '/data/created_data/polygon/wrong_segments.csv', index=False)

    


if __name__ == '__main__':
   
    segment_line()


    #get_route()

    # origin = (37.46106, -121.90049)
    # destination = (37.46034, -121.89994)

    # result = get_route(origin, destination, 11242, 0.09361)
    # print(result)


    #coords = [(result[1], result[2]) for node in shortest_path]
    # merged_line = linemerge(result[2:])
    # print(LineString(merged_line))



###############
# j = 0
   
    # while j < len(segments):
    #     if len(segments) - j < 3:
    #         the_range = len(segments) - j
    #     else: the_range = 3

    #     with multiprocessing.Pool(processes=the_range) as pool:
    #         results = pool.starmap(get_route, [([start_lat[j+i], start_long[j+i]],
    #                                             [end_lat[j+i], end_long[j+i]],
    #                                             segments[j+i],
    #                                             road_distance[j+i]) for i in range(the_range)])

    #     adder = {}
    #     for result in results:
    #         adder.update(result)

    #     with open(filename, 'r+') as file:
    #         file_data = json.load(file)
    #         file_data.update(adder)
    #         file.seek(0)
    #         json.dump(file_data, file)

    #     j += 3