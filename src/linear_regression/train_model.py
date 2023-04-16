import datetime
import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

gen_dir = str(Path(__file__).resolve().parents[2])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)


# Load the combined data
data = pd.read_csv(gen_dir + '/data/created_data/combined_data.csv')

# Preprocess the data
data['Date Time'] = pd.to_datetime(data['Date Time'])

# Group the data by segment ID
grouped_data = data.groupby('Segment ID')

# Directory to store the models
models_directory = gen_dir + "/data/created_data/models/"

# Dictionary to store the trained models
models_dict = {}

# Train a model for each segment ID
for segment_id, segment_data in grouped_data:
    # Prepare the input and output data for the model
    segment_data = segment_data.fillna(0)

    X = segment_data[['prcp', 'snow', 'temp']]
    y = segment_data['Speed(km/hour)']

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify= None)

    # Create and train a linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate the model on test data
    score = model.score(X_test, y_test)
    #print(f"Segment ID: {segment_id}, Model Score: {score}")

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
models_filename = models_directory + "models_dict.pkl"
with open(models_filename, "wb") as f:
    pickle.dump(models_dict, f)
