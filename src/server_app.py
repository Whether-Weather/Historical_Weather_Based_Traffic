




import json
import sys
from pathlib import Path

import get_colors as gc
from flask_cors import CORS

from flask import Flask, jsonify, request

gen_dir = str(Path(__file__).resolve().parents[2])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://whether-weather.github.io"}})


import pickle


gen_dir = str(Path(__file__).resolve().parents[2])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)

county = 'SantaClara'
models_directory = gen_dir + "/data/created_data/" + county  + "/"
models_filename = models_directory + "random_forest_model.pkl"

with open(models_filename, "rb") as f:
    loaded_models_dict = pickle.load(f)


filename = gen_dir + '/data/created_data/' + county + '/' + county + '.json'
with open(filename, "rb") as f:
    geojson = json.load(f)

fn = gen_dir + '/data/created_data/' + county + '/segid_to_refspeed.pkl'
with open(fn, "rb") as f:
    segid_speeds = pickle.load(f)    

new_county = 'HarrisCounty'
houston_filename = gen_dir + '/data/created_data/' + new_county + '/' + new_county + '.json'
with open(houston_filename, "rb") as f:
    houston_geojson = json.load(f)

houston_models_directory = gen_dir + "/data/created_data/" + new_county  + "/"
houston_models_filename = houston_models_directory + "may7logistic.pkl"

with open(houston_models_filename, "rb") as f:
    houston_loaded_models_dict = pickle.load(f)

houston_fn = gen_dir + '/data/created_data/' + new_county + '/segid_to_refspeed.pkl'
with open(houston_fn, "rb") as f:
    houston_segid_speeds = pickle.load(f)    

county_data = {
    "San Jose, CA" : {
        "model": loaded_models_dict,
        "segid_speeds": segid_speeds,
        "geojson": geojson
    },
    "Harris County, Texas": {
        "model": houston_loaded_models_dict,
        "segid_speeds": houston_segid_speeds,
        "geojson": houston_geojson

    }
}

@app.route('/get-model', methods=['POST'])
def get_model():
    # print(request.get_json())
    data = request.get_json()
    if set(data.keys()) != {'county'}:
        print(data['county'])
        response = gc.get_colors(county_data[data['county']]['geojson'], county_data[data['county']]['model'], county_data[data['county']]['segid_speeds'], data['rain'], data['temperature'], data['humidity'], data['time'], data['dew'], data['direction'], data['speed'], data['pressure'])
    else: 
        response = gc.get_colors_LM(county_data[data['county']]['geojson'], county_data[data['county']]['model'], county_data[data['county']]['segid_speeds'])
    #print(response)
    return jsonify(response)

@app.route('/get-new-model', methods=['POST'])
def get_new_model():
    data = request.get_json()
    if data:
        response = county_data[data['county']]['geojson']
    else:
        response = None
    return jsonify(response)

    

if __name__ == '__main__':
    app.run(debug=True)

