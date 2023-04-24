import datetime
import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import os
import time

gen_dir = str(Path(__file__).resolve().parents[2])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)

folder_path = gen_dir + "/data/created_data/SantaClara/all/pickle"

pkl_files = [f for f in os.listdir(folder_path) if f.endswith('.pkl')]

file_paths = [os.path.join(folder_path, file) for file in pkl_files]

dfs = []
for file in file_paths:
    time1 = time.perf_counter()

    df = pd.read_pickle(file)
    time2 = time.perf_counter()
    print(time2 - time1)
    dfs.append(df)

data = pd.concat(dfs, ignore_index=True)
dfs = None
df = None

grouped_data = data.groupby('Segment ID')

models_directory = gen_dir + "/data/created_data/models/"

models_dict = {}

transformations = ['linear', 'sqrt', 'square', 'cube', 'cbrt', 'quad_root']

for segment_id, segment_data in grouped_data:
    segment_data = segment_data.dropna(subset=['Speed(km/hour)'])
    segment_data['Date Time'] = pd.to_datetime(segment_data['Date Time'])
    segment_data.loc[:, 'Hour'] = segment_data['Date Time'].dt.hour

    X = segment_data[['temp', 'rhum', 'prcp', 'snow', 'wspd', 'pres', 'coco', 'Hour']]
    y = segment_data['Speed(km/hour)']

    best_model = None
    best_score = float('-inf')
    best_transformation = None
    imputer = SimpleImputer(strategy='mean')
    X_imputed = imputer.fit_transform(X)
    
    for transformation in transformations:
        if transformation == 'linear':
            X_transformed = X_imputed
        elif transformation == 'sqrt':
            X_transformed = np.sqrt(np.abs(X_imputed))
        elif transformation == 'square':
            X_transformed = np.power(X_imputed, 2)
        elif transformation == 'cube':
            X_transformed = np.power(X_imputed, 3)
        elif transformation == 'cbrt':
            X_transformed = np.cbrt(np.abs(X_imputed))
        elif transformation == 'quad_root':
            X_transformed = np.power(np.abs(X_imputed), 1/4)

        X_train, X_test, y_train, y_test = train_test_split(X_transformed, y, test_size=0.2, random_state=42, stratify=None)

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        score = model.score(X_test, y_test)

        if score > best_score:
            best_score = score
            best_model = model
            best_transformation = transformation

    models_dict[segment_id] = {
        'model': model,
        'r2_score': score,
        'mae': mean_absolute_error(y_test, model.predict(X_test)),
        'mse': mean_squared_error(y_test, model.predict(X_test)),
        'rmse': np.sqrt(mean_squared_error(y_test, model.predict(X_test))),
        'training_size': len(X_train),
        'testing_size': len(X_test),
        'feature_names': list(X.columns),
        'training_timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

models_filename = models_directory + "models_all_sqrt_rf_dict.pkl"
with open(models_filename, "wb") as f:
    pickle.dump(models_dict, f)
