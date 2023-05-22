import json
import sys
from pathlib import Path

import get_colors as gc
from flask_cors import CORS

from flask import Flask, jsonify, request
import pickle


gen_dir = str(Path(__file__).resolve().parents[2])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)



app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/*": {"origins": "https://whether-weather.github.io"}})
  


def get_files(model_county):
    print(model_county)
    if model_county == "San Jose, CA":
        county = "SantaClara"
    elif model_county == "Harris County, Texas":
        county = "HarrisCounty"
    models_directory = gen_dir + "/data/created_data/" + county  + "/"
    models_filename = models_directory + county + "_model.pkl"
    with open(models_filename, "rb") as f:
        loaded_models_dict = pickle.load(f)

    filename = gen_dir + '/data/created_data/' + county + '/' + county + '.json'
    with open(filename, "rb") as f:
        geojson = json.load(f)

    fn = gen_dir + '/data/created_data/' + county + '/segid_to_refspeed.pkl'
    with open(fn, "rb") as f:
        segid_speeds = pickle.load(f)   

    county_data = {
        "model": loaded_models_dict,
        "segid_speeds": segid_speeds,
        "geojson": geojson
    }
    return county_data


data_dict = get_files("San Jose, CA")


@app.route('/get-model', methods=['POST'])
def get_model():
    data = request.get_json()
    data_dict = get_files(data['county'])

    if set(data.keys()) != {'county'}:
        print(set(data.keys()))
        response = gc.get_colors(data_dict['geojson'], data_dict['model'], data_dict['segid_speeds'], data['rain'], data['temperature'], data['humidity'], data['time'], data['dew'], data['direction'], data['speed'], data['pressure'])
    else: 
        print("else")
        response = gc.get_colors_LM(data_dict['geojson'], data_dict['model'], data_dict['segid_speeds'], data['county'])
    #print(response)
    return jsonify(response)

@app.route('/get-new-model', methods=['POST'])
def get_new_model():
    data = request.get_json()
    data_dict = get_files(data['county'])
    print(data)
    if data['map'] == 'MLMAP':
        print("bla")
        response = {'geojson': data_dict['geojson']}
    else:
        print("here")
        response = gc.get_colors_LM(data_dict['geojson'], data_dict['model'], data_dict['segid_speeds'], data['county'])
    return jsonify(response)

    

if __name__ == '__main__':
    app.run(debug=True)