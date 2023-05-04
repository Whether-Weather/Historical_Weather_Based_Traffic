import os
import sys
import time
import datetime
import pickle
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error, mean_squared_error
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.metrics import MeanAbsoluteError, MeanSquaredError, RootMeanSquaredError
from keras import backend as K

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
name = 'ann_model'
models_filename = models_directory + "/" + name + ".pkl"
error_file = models_directory + '/' + name + '_error.pkl'

# Dictionary to store the trained models
error_segments = []
models_dict = {}

i = 0 
chunk = 10

def r2_score(y_true, y_pred):
    SS_res = K.sum(K.square(y_true - y_pred))
    SS_tot = K.sum(K.square(y_true - K.mean(y_true)))
    return (1 - SS_res / (SS_tot + K.epsilon()))

# Create a simple ANN model for regression
def create_ann_model(input_dim):
    model = Sequential()
    model.add(Dense(32, input_dim=input_dim, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(1, activation='linear'))

    model.compile(loss='mean_squared_error', optimizer='adam', metrics=[r2_score, MeanSquaredError(), MeanAbsoluteError(), RootMeanSquaredError()])
    return model

for segment_id, segment_data in grouped_data:
    try:
        if segment_id not in models_dict:
            segment_data = segment_data.dropna(subset=['Speed(km/hour)'])
            segment_data['Hour'] = pd.to_datetime(segment_data['Date Time']).dt.hour
            segment_data['is_raining'] = segment_data['prcp'].apply(lambda x: 1 if x > 0 else 0)

            segment_data['prcp_log'] = np.log(segment_data['prcp'] + 1e-6)

            X = segment_data[['temp', 'dwpt', 'rhum', 'prcp_log', 'is_raining', 'wdir', 'wspd', 'pres', 'Hour']]
            y = segment_data['Speed(km/hour)']

            imputer = SimpleImputer(strategy='mean')
            X_imputed = imputer.fit_transform(X)

            X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42, stratify=None)
                    # Scale the features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)

            # Create and train an ANN model on the data
            ann_model = create_ann_model(X_train_scaled.shape[1])
            ann_model.fit(X_train_scaled, y_train, epochs=100, batch_size=32, verbose=0)

            # Evaluate the model on test data
            metrics = ann_model.evaluate(X_test_scaled, y_test, verbose=0)

            # Extract the metrics
            mse, mae, rmse = metrics[1], metrics[2], metrics[3]

            # Make predictions on the test set
            y_pred = ann_model.predict(X_test_scaled).flatten()

            # Calculate the R^2 score
            r2 = r2_score(y_test, y_pred)
            print("ANN R^2 score: ", r2)


            models_dict[segment_id] = {
                'model': ann_model,
                'mse': mse,
                'mae': mae,
                'rmse': rmse,
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