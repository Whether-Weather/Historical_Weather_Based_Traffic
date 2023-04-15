import pickle

import sys
from pathlib import Path

gen_dir = str(Path(__file__).resolve().parents[2])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)


models_directory = gen_dir + "/data/created_data/models/"
models_filename = models_directory + "models_dict.pkl"

with open(models_filename, "rb") as f:
    loaded_models_dict = pickle.load(f)

# Print the contents of the loaded models dictionary
for segment_id, model in loaded_models_dict.items():
    print(f"Segment ID: {segment_id}")
    print(f"Weights: {model.coef_}")
    print(f"Intercept: {model.intercept_}")
    print()