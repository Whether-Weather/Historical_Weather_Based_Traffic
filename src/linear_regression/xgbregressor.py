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
import xgboost as xgb
from sklearn.model_selection import GridSearchCV
from sklearn.feature_selection import RFECV
from sklearn.pipeline import Pipeline

gen_dir = str(Path(__file__).resolve().parents[2])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)

# Load the combined data
#data = pd.read_csv(gen_dir + '/data/created_data/training_data/combined_data.csv')

####
county = 'HarrisCounty'
folder_path = gen_dir + "/data/created_data/" + county + "/combined_data"

# List all the csv files in the folder
pkl_files = [f for f in os.listdir(folder_path) if f.endswith('combined.pkl')]

# Create a list of file paths
file_paths = [os.path.join(folder_path, file) for file in pkl_files]

dfs = []
for file in file_paths:
    time1 = time.perf_counter()

    df = pd.read_pickle(file)
    # print(df.head(10))
    time2 = time.perf_counter()
    print(time2 - time1)
    dfs.append(df)

data = pd.concat(dfs, ignore_index=True)
dfs = None
df = None


####

# Preprocess the data
# data['Date Time'] = pd.to_datetime(data['Date Time'])

# Group the data by segment ID
grouped_data = data.groupby('Segment ID')

# Directory to store the models
models_directory = gen_dir + "/data/created_data/" + county
name = 'random_forest_model_n15'
models_filename = models_directory + "/" + name + ".pkl"
error_file = models_directory + '/' + name + '_error.pkl'

# Dictionary to store the trained models
error_segments = []
models_dict = {}
# try:
#     with open(models_filename, "rb") as f:
#         models_dict = pickle.load(f)
# except FileNotFoundError:
#     with open(models_filename, "wb") as f:
#         pickle.dump(models_dict, f)

# try:
#     with open(error_file, "rb") as f:
#         error_segments = pickle.load(f)
# except FileNotFoundError:
#     with open(error_file, "wb") as f:
#         pickle.dump(error_segments, f)
# Train a model for each segment ID
param_grid = {
    'n_estimators': [50, 100, 200, 300],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.2],
    'subsample': [0.8, 0.9, 1.0],
    'colsample_bytree': [0.8, 0.9, 1.0],
    'gamma': [0, 0.1, 0.2]
}


i = 0 
chunk = 200
for segment_id, segment_data in grouped_data:
    try:
        if segment_id not in models_dict:
            segment_data = segment_data.dropna(subset=['Speed(km/hour)'])
            segment_data['Hour'] = pd.to_datetime(segment_data['Date Time']).dt.hour
            segment_data['is_raining'] = segment_data['prcp'].apply(lambda x: 1 if x > 0 else 0)

            segment_data['prcp_log'] = np.log(segment_data['prcp'] + 1e-6)

            X = segment_data[['temp', 'dwpt', 'rhum', 'prcp_log', 'is_raining', 'snow', 'wdir', 'wspd', 'wpgt', 'pres', 'tsun', 'coco', 'Hour']]
                #['temp', 'dwpt', 'rhum', 'prcp_log', 'is_raining', 'wdir', 'wspd', 'pres', 'Hour']]
            y = segment_data['Speed(km/hour)']

           

            imputer = SimpleImputer(strategy='mean')
            X_imputed = imputer.fit_transform(X)


            X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42, stratify=None)

            
            model = xgb.XGBRegressor(max_depth  = 5, n_estimators = 100, learning_rate = 0.1, random_state=42)
            
            # # Create the RFE object with cross-validation
            # rfe = RFECV(estimator=model, step=1, cv=3, scoring='r2', n_jobs=-1)

            # # Fit the RFE object to the training data
            # rfe.fit(X_train, y_train)

            # # Get the selected features
            # selected_features = rfe.support_
            # print("Selected features:", selected_features)

            # # Get the feature ranking
            # feature_ranking = rfe.ranking_
            # print("Feature ranking:", feature_ranking)

            # # Train the XGBRegressor model with the selected features
            # X_train_selected = X_train[:, selected_features]
            # X_test_selected = X_test[:, selected_features]

            model.fit(X_train, y_train)

            # Evaluate the model on test data
            score = model.score(X_test, y_test)
            

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
        i += 1
        if i % chunk == 0:
            with open(models_filename, "wb") as f:
                pickle.dump(models_dict, f)
            with open(error_file, "wb") as f:
                pickle.dump(error_segments, f)
    except:
        error_segments.append(segment_id)

# Save the models dictionary to a file

with open(models_filename, "wb") as f:
    pickle.dump(models_dict, f)


with open(error_file, "wb") as f:
    pickle.dump(error_segments, f)



# r2 average 0.3369184769603356
# mae average 2.901023902003224

#with imputer
#r2 average 0.33010720727733905
#mae average 2.88497609616322