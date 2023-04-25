import pickle
import sys
from pathlib import Path

import geojson
from shapely.geometry import LineString

gen_dir = str(Path(__file__).resolve().parents[3])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)


# Sample dictionary with segment_id and linegeometry
segment_dict = {}
filename = gen_dir + '/data/created_data/input_data/inrix/SantaClaraLines.pkl'
with open(filename, "rb") as f:
    segment_dict = pickle.load(f)

def swap_coordinates(linegeometry):
    return LineString([(coord[1], coord[0]) for coord in list(linegeometry.coords)])


def create_geojson(segment_dict):
    features = []
    i = 0
    for segment_id, linegeometry in segment_dict.items():
        if linegeometry:
            feature = geojson.Feature(
                geometry=  swap_coordinates(linegeometry),
                properties={
                    'segment_id': segment_id
                }
            )
        else:
            
            i += 1
        features.append(feature)
        
    
    return geojson.FeatureCollection(features)

geojson_data = create_geojson(segment_dict)

# Save GeoJSON data to a file
with open(gen_dir + '/data/created_data/input_data/output_file.geojson', "w") as f:
    geojson.dump(geojson_data, f)
