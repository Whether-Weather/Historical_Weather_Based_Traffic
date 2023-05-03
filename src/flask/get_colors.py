import datetime

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler


def get_colors(geojson, model, prcp, temp, rhum):
# Get the geojson from flask 
    s = 0

    for feature in geojson['features']:
        seg_id = feature['properties']['segment_id']
        X_test = [[float(temp), 0, float(rhum), float(prcp), 0, 0, 0, 0, datetime.datetime.now().hour]]
        
        # Predict the speed using the linear regression model and the feature vector
        y_pred = model[int(seg_id)]['model'].predict(X_test)[0]
        # print('predicted speed',y_pred)
        
        feature['properties']['speed'] = round(y_pred,2)
        feature['properties']['color'] = get_color(y_pred, 30)

        s+=y_pred
        
    print(float(temp), float(rhum), float(prcp), s/len(geojson['features']))
    return {'geojson': geojson}
        
# For feature in features, get sgement_id from properties
#   Get predicted speed based off of, passed in data values from flask
#   Add speed, and RGB color to properties 

#Return this as response to front-end, which displays data and refreshes 



def get_color(current_speed, historical_speed):
    """Return an RGB array between dark red (-20% slower) and bright green (+20% faster)
    depending on the comparison between the current speed and historical speed."""

    # Calculate the percentage difference between the current speed and historical speed
    percentage_diff = (current_speed - historical_speed) / historical_speed * 100
    
    # Determine the color based on the percentage difference
    if percentage_diff <= -20:
        # Dark red for -20% or slower
        return [139, 0, 0]
    elif percentage_diff >= 20:
        # Bright green for +20% or faster
        return [0, 255, 0]
    else:
        # Calculate the color between red and green based on the percentage difference
        red = max(0, min(255, int(255 * (120 + percentage_diff) / 140)))
        green = max(0, min(255, int(255 * (120 - percentage_diff) / 140)))
        blue = 0
        return [red, green, blue]


