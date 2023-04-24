import datetime
import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import dask.dataframe as dd
import os
import time

gen_dir = str(Path(__file__).resolve().parents[2])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)

# Load the combined data
#data = pd.read_csv(gen_dir + '/data/created_data/training_data/combined_data.csv')

####
folder_path = gen_dir + "/data/created_data/SantaClara/all/pickle"

# List all the CSV files in the folder
pkl_files = [f for f in os.listdir(folder_path) if f.endswith('.pkl')]

# Create a list of file paths
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


####

# Preprocess the data
# data['Date Time'] = pd.to_datetime(data['Date Time'])

# Group the data by segment ID
grouped_data = data.groupby('Segment ID')

# Directory to store the models
models_directory = gen_dir + "/data/created_data/models/"

# Dictionary to store the trained models
models_dict = {}
transformations = ['linear', 'sqrt', 'square', 'cube'] #, 'cbrt', 'quad_root']

# Train a model for each segment ID
for segment_id, segment_data in grouped_data:
    segment_data = segment_data.dropna(subset=['Speed(km/hour)'])
    segment_data['Date Time'] = pd.to_datetime(segment_data['Date Time'])
    segment_data.loc[:, 'Hour'] = segment_data['Date Time'].dt.hour
   
    # plt.scatter(segment_data['Hour'], segment_data['Speed(km/hour)'])
    # plt.xlabel('Hour')
    # plt.ylabel('Speed (km/hour)')
    # plt.title('Scatter plot of Speed(km/hour) vs Hour')
    # plt.xticks(range(0, 24))  # Rotate x-axis labels for better readability
    # plt.show()

    # plt.scatter(segment_data['prcp'], segment_data['Speed(km/hour)'])
    # plt.xlabel('prcp')
    # plt.ylabel('Speed (km/hour)')
    # plt.title('Scatter plot of Speed(km/hour) vs Hour')
    #  # Rotate x-axis labels for better readability
    # plt.show()
    # Prepare the input and output data for the model
    X = segment_data[['temp', 'dwpt', 'rhum', 'prcp', 'snow', 'wdir', 'wspd', 'wpgt', 'pres', 'tsun', 'coco', 'Hour']]#segment_data[['temp','prcp', 'snow', 'wspd', 'Hour']]
    #segment_data[['temp', 'dwpt', 'rhum', 'prcp', 'snow', 'wdir', 'wspd', 'wpgt', 'pres', 'tsun', 'coco']]
    y = segment_data['Speed(km/hour)']

    # Impute missing values using the mean of each feature
    best_model = None
    best_score = float('-inf')
    best_transformation = None
    imputer = SimpleImputer(strategy='mean')
    X_imputed = imputer.fit_transform(X)

    # Apply square root transformation to the imputed data
   
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

        # Split the data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X_transformed, y, test_size=0.2, random_state=42, stratify=None)

        # Create and train a linear regression model on the transformed data
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Evaluate the model on test data
        score = model.score(X_test, y_test)
        if score > best_score:
            best_score = score
            best_model = model
            best_transformation = transformation

    # Save the model to the dictionary
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

# Save the models dictionary to a file
models_filename = models_directory + "models_all_1_dict.pkl"
with open(models_filename, "wb") as f:
    pickle.dump(models_dict, f)
