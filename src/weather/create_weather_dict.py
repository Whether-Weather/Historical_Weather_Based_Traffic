#creates all_weather json file which can be loaded as a dict
#takes in weather csv file and creates dictionary with long,lat,date as key for the dictionary and val is rainfall
#maybe can change value to rainfall, snowfall array or whatever we like


import pandas as pd
import math

from utils import file_helper_functions as fhf




def create_weather_dict(filename='data/input_data/weather/new_weather_data.csv'):
    df_weather = pd.read_csv(filename)
    lat_column = df_weather['LATITUDE'].tolist()
    long_column = df_weather['LONGITUDE'].tolist()
    precipitation = df_weather['PRCP'].tolist()
    weather_date = df_weather['DATE'].tolist()

    weather_dict = {}
    j = 0
    for i in range(0, len(lat_column)):
        format_str = str(long_column[i]) + "," + str(lat_column[i]) + "," + str(weather_date[i])
        
        if math.isnan(precipitation[i]):
            weather_dict[format_str] = 0
        else:
            weather_dict[format_str] = precipitation[i]
    
    fhf.write_dict_to_json(weather_dict, 'data/created_data/weather/all_weather.json')
    

if __name__ == "__main__":
    print()
