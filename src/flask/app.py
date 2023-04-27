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
CORS(app, origins="http://localhost:3000")

import pickle
import subprocess
import sys
from pathlib import Path

gen_dir = str(Path(__file__).resolve().parents[2])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)

county = 'SantaClara'
models_directory = gen_dir + "/data/created_data/" + county  + "/"
models_filename = models_directory + "santaclara.pkl"

with open(models_filename, "rb") as f:
    loaded_models_dict = pickle.load(f)



filename = gen_dir + '/data/created_data/' + county + '/' + county + '.json'
with open(filename, "rb") as f:
    geojson = json.load(f)

@app.route('/get-model', methods=['POST'])
def get_model():
    print(request.get_json())
    data = request.get_json()

    response = gc.get_colors(geojson, loaded_models_dict, data['rain'], data['temperature'], data['humidity'])
    return jsonify(response)
    
    

if __name__ == '__main__':
    app.run(debug=True)

