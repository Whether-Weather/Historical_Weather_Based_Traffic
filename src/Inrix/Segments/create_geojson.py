import geojson
from shapely.geometry import LineString
import sys
from pathlib import Path
import pickle


gen_dir = str(Path(__file__).resolve().parents[3])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)


# Sample dictionary with segment_id and linegeometry
segment_dict = {}
filename = gen_dir + '/data/created_data/polygon/line_polygon_dict.pkl'
with open(filename, "rb") as f:
    segment_dict = pickle.load(f)


def create_geojson(segment_dict):
    features = []
    
    for segment_id, linegeometry in segment_dict.items():
        feature = geojson.Feature(
            geometry=linegeometry,
            properties={
                'segment_id': segment_id
            }
        )
        features.append(feature)
    
    return geojson.FeatureCollection(features)

geojson_data = create_geojson(segment_dict)

# Save GeoJSON data to a file
with open(gen_dir + '/data/created_data/polygon/output_file.geojson', "w") as f:
    geojson.dump(geojson_data, f)
