import datetime

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler


def get_colors(geojson, model, prcp, temp, rhum):
# Get the geojson from flask 

    for feature in geojson['features']:
        seg_id = feature['properties']['segment_id']
        X_test = [[temp, 0, rhum, prcp, 0, 0, 0, 0, datetime.datetime.now().hour]]
        
        # Scale the feature vector using the same scaler used during training
        scaler = StandardScaler()
        X_test = scaler.fit_transform(X_test)
        
        # Predict the speed using the linear regression model and the feature vector
        y_pred = model[int(seg_id)]['model'].predict(X_test)[0]
        # print('predicted speed',y_pred)
        
        feature['properties']['speed'] = y_pred
        feature['properties']['color'] = get_color(y_pred, 50)

        
    return {'geojson': geojson}
        
# For feature in features, get sgement_id from properties
#   Get predicted speed based off of, passed in data values from flask
#   Add speed, and RGB color to properties 

#Return this as response to front-end, which displays data and refreshes 



def get_color(current_speed, historical_speed):
    """Return an RGB array between dark red (-50% slower) and bright green (+50% faster)
    depending on the comparison between the current speed and historical speed."""
    
    # Calculate the percentage difference between the current speed and historical speed
    percentage_diff = (current_speed - historical_speed) / historical_speed * 100
    
    # Determine the color based on the percentage difference
    if percentage_diff <= -50:
        # Dark red for -50% or slower
        return [139, 0, 0]
    elif percentage_diff >= 50:
        # Bright green for +50% or faster
        return [0, 255, 0]
    else:
        # Calculate the color between red and green based on the percentage difference
        red = max(0, min(255, int(255 * (100 + percentage_diff) / 100)))
        green = max(0, min(255, int(255 * (100 - percentage_diff) / 100)))
        blue = 0
        return [red, green, blue]

