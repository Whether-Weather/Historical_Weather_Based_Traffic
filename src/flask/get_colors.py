from datetime import datetime, timedelta, timezone

import numpy as np
from meteostat import Hourly, Stations
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler


def get_colors(geojson, model, segid_speeds, prcp, temp, rhum, time, dew, direction, speed, pres):
    print("In Colors")
# Get the geojson from flask 
    wrong_seg = []
    for feature in geojson['features']:
        seg_id = feature['properties']['segment_id']
        X_test = [[float(temp), float(dew), float(rhum), float(np.log(float(prcp) + 1e-6)), float(1 if float(prcp) > 0 else 0), float(direction), float(speed), float(pres), float(time)]]
        
        # Predict the speed using the linear regression model and the feature vector
        if int(seg_id) in model:
            y_pred = model[int(seg_id)]['model'].predict(X_test)[0]
        # print('predicted speed',y_pred)
        
            feature['properties']['Speed'] = float(round(y_pred,2))
            feature['properties']['color'], feature['properties']['Percent_Difference'] = get_color(y_pred, segid_speeds[seg_id]['Ref Speed(km/hour)'])
            feature['properties']['Reference_Speed'] = float(segid_speeds[seg_id]['Ref Speed(km/hour)'])
            
    return {'geojson': geojson}
        
# For feature in features, get sgement_id from properties
#   Get predicted speed based off of, passed in data values from flask
#   Add speed, and RGB color to properties 

#Return this as response to front-end, which displays data and refreshes 

def get_colors_LM(geojson, model, segid_speeds, county):
    stations = Stations()
    coordinates = ()
    if county == "San Jose, CA":
        coordinates = (37.3541, -121.9552)
    elif county == "Harris County, Texas":
        coordinates = (29.763564, -95.447633)
    nearby_station = stations.nearby(*coordinates)
    closest_station = nearby_station.fetch(1)

    
    data = Hourly(closest_station, start=datetime.now() - timedelta(hours=1) + timedelta(hours=7), end=datetime.now()+ timedelta(hours=7))
    data = data.fetch()
    prcp = float(data['prcp'][0])
    temp = float(data['temp'][0])
    rhum = float(data['rhum'][0])
    time = (datetime.now().hour+7)%24
    dew = float(data['dwpt'][0])
    direction = float(data['wdir'][0])
    speed = float(data['wspd'][0])
    pres = float(data['pres'][0])
    
    for feature in geojson['features']:
        seg_id = feature['properties']['segment_id']
        X_test = [[float(temp), float(dew), float(rhum), float(np.log(float(prcp) + 1e-6)), float(1 if float(prcp) > 0 else 0), float(direction), float(speed), float(pres), float(time)]]
        
        # Predict the speed using the linear regression model and the feature vector
        if int(seg_id) in model:
            y_pred = model[int(seg_id)]['model'].predict(X_test)[0]
        # print('predicted speed',y_pred)
        
            feature['properties']['Speed'] = float(round(y_pred,2))
            feature['properties']['color'], feature['properties']['Percent_Difference'] = get_color(y_pred, segid_speeds[seg_id]['Ref Speed(km/hour)'])
            feature['properties']['Reference_Speed'] = float(segid_speeds[seg_id]['Ref Speed(km/hour)'])

    return {'geojson': geojson, 'weather': {"Rain (in)":prcp,"Temperature (Celsius)": temp,"Humidity (%)":rhum, "Time (UTC)":time,"Dew Point (%)": dew,"Wind Direction (Degrees)":direction, "Wind Speed (km/hr)":speed,"Air Pressure (hpa)":pres}}
    
    

def get_color(current_speed, historical_speed):
    """Return an RGB array between dark red (-20% slower) and bright green (+20% faster)
    depending on the comparison between the current speed and historical speed."""

    # Calculate the percentage difference between the current speed and historical speed
    percentage_diff = (current_speed - historical_speed) / historical_speed * 100
    
    # Determine the color based on the percentage difference
    if percentage_diff <= -20:
        # Dark red for -20% or slower
        return [[139, 0, 0], percentage_diff]
    elif percentage_diff >= 20:
        # Bright green for +20% or faster
        return [[0, 255, 0], percentage_diff]
    else:
        # Calculate the color between red and green based on the percentage difference
        red = max(0, min(255, int(255 * (120 + percentage_diff) / 140)))
        green = max(0, min(255, int(255 * (120 - percentage_diff) / 140)))
        blue = 0
        return [[red, green, blue], percentage_diff]


