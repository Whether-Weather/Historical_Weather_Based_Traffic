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
CORS(app, origins="*")

import pickle
import subprocess
import sys
from pathlib import Path

gen_dir = str(Path(__file__).resolve().parents[2])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)

county = 'SantaClara'
models_directory = gen_dir + "/data/created_data/" + county  + "/"
models_filename = models_directory + "random_forest_model_n15.pkl"

with open(models_filename, "rb") as f:
    loaded_models_dict = pickle.load(f)


filename = gen_dir + '/data/created_data/' + county + '/' + county + '.json'
with open(filename, "rb") as f:
    geojson = json.load(f)
 
 
fn = gen_dir + '/data/created_data/' + county + '/segid_to_refspeed.pkl'
with open(fn, "rb") as f:
    segid_speeds = pickle.load(f)

@app.route('/get-model', methods=['POST'])
def get_model():
    print(request.get_json())
    data = request.get_json()
    if data:
        response = gc.get_colors(geojson, loaded_models_dict, segid_speeds, data['rain'], data['temperature'], data['humidity'], data['time'], data['dew'], data['direction'], data['speed'], data['pressure'])
    else: 
        response = gc.get_colors_LM(geojson, loaded_models_dict, segid_speeds)
    return jsonify(response)
    

if __name__ == '__main__':
    app.run(debug=True)

