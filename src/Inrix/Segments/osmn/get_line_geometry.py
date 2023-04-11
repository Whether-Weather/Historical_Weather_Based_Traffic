import osmnx as ox
import taxicab as tc
from shapely.geometry import LineString
from shapely.ops import linemerge

#should write code that if length doesnt match then it should increase margin
def get_route(origin, destination, plot = 1, margin=0.02):
    # Define the bounding box based on origin and destination coordinates with a margin
    xmin, xmax = min(origin[1], destination[1]) - margin, max(origin[1], destination[1]) + margin
    ymin, ymax = min(origin[0], destination[0]) - margin, max(origin[0], destination[0]) + margin

    # Get the graph within the bounding box
    G = ox.graph_from_bbox(ymax, ymin, xmax, xmin, network_type='drive', simplify=True)

    # Calculate the shortest path
    route = tc.distance.shortest_path(G, origin, destination)

    # Plot the graph with the route
    if plot:
        tc.plot.plot_graph_route(G, route)

    return route

origin = (37.46106, -121.90049)
destination = (37.46034, -121.89994)

result = get_route(origin, destination)
print(result)


#coords = [(result[1], result[2]) for node in shortest_path]
merged_line = linemerge(result[2:])
print(LineString(merged_line))
