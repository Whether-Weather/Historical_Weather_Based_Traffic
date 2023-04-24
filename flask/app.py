from flask import Flask, request

app = Flask(__name__)

import subprocess


@app.route('/get-model', methods=['POST'])
def get_model():
    data = request.get_json()
    print("data")
    print(data)
    # pass data as parameters to Python script
    param1 = data['param1']
    param2 = data['param2']
    subprocess.call(['python', 'my_script.py', param1, param2])

