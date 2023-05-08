import pickle
import sys
from pathlib import Path

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

gen_dir = str(Path(__file__).resolve().parents[2])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)

county = 'HarrisCounty'
models_directory = gen_dir + "/data/created_data/" + county
models_filename = models_directory + "/may7logistic.pkl"

with open(models_filename, "rb") as f:
    loaded_models_dict = pickle.load(f)

# Print the contents of the loaded models dictionary
i = 0
r2_total = 0
m = 0
r2_dist = []
i_val = []
for segment_id, model_info in loaded_models_dict.items():
    r2_dist.append(model_info['r2_score'])
    i_val.append([i])
    i += 1

r2_dist.sort()


plt.figure(figsize=(10, 6))
plt.scatter(i_val, r2_dist)
plt.title(f'r2 score vs index')
plt.xlabel('index')
plt.ylabel('r2 score')
plt.show()

    # if model_info['r2_score'] > 0:
    # if model_info['r2_score'] > .4:
    #     r2_total += model_info['r2_score']
    #     m += model_info['mae']
    #     i += 1
    # print(f"Segment ID: {segment_id}")
    # model = model_info['model']
    # print(f"r2Score: {model_info['r2_score']}")
    # print(f"Weights: {model.coef_}")
    # print(f"Intercept: {model.intercept_}")
    # print()
# print(f"r2 average {r2_total / i}")
# print(f"mae average {m / i}")
# print(i)

# r2 average 0.33010720727733905
# mae average 2.88497609616322

# r2 average 0.335499189615741
# mae average 2.903078186903178

# r2 average 0.3106663717212711
# mae average 2.9248631513345322