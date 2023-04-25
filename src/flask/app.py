from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="http://localhost:3000")

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

if __name__ == '__main__':
    app.run(debug=True)

