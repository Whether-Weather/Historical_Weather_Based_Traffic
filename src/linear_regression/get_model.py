import pickle
import sys
from pathlib import Path

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

gen_dir = str(Path(__file__).resolve().parents[2])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)

county = 'HarrisCounty'
models_directory = gen_dir + "/data/created_data/" + county
models_filename = models_directory + "/random_forest_model_n15.pkl"

with open(models_filename, "rb") as f:
    loaded_models_dict = pickle.load(f)

# Print the contents of the loaded models dictionary
i = 0
r2_total = 0
m = 0
for segment_id, model_info in loaded_models_dict.items():
    # if model_info['r2_score'] > 0:
    r2_total += model_info['r2_score']
    m += model_info['mae']
    i += 1
    # print(f"Segment ID: {segment_id}")
    # model = model_info['model']
    # print(f"r2Score: {model_info['r2_score']}")
    # print(f"Weights: {model.coef_}")
    # print(f"Intercept: {model.intercept_}")
    # print()
print(f"r2 average {r2_total / i}")
print(f"mae average {m / i}")

# r2 average 0.33010720727733905
# mae average 2.88497609616322

# r2 average 0.335499189615741
# mae average 2.903078186903178

# r2 average 0.3106663717212711
# mae average 2.9248631513345322