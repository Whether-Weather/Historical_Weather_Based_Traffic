import datetime
import pandas as pd
from meteostat import Stations, Hourly

# Set the time range

def get_weather_data(station_id, start = datetime.datetime(2022, 3, 1), end = datetime.datetime(2023, 4, 9)):
    # Get hourly weather data for the station
    data = Hourly(station_id, start, end)
    data = data.fetch()
    print("Weather data retrieved")
    return data

def get_weather_dict(station_id, start = datetime.datetime(2022, 3, 1), end = datetime.datetime(2022, 4, 9)):
    data = get_weather_data(station_id, start, end)
    weather_data = {"times": {}}
    selected_columns = ['temp', 'dwpt', 'rhum', 'prcp', 'snow', 'wdir', 'wspd', 'wpgt', 'pres', 'tsun', 'coco']
    # data['snow'] = data['snow'].fillna(0)

    for index, row in data.iterrows():
        time = row.name.to_pydatetime()
        row_dict = {col: row[col] for col in selected_columns}
        weather_data["times"][str(time)] = row_dict


    return weather_data

x = get_weather_dict("KSJC0")

if __name__ == '__main__':
    a = 441531089




# start = datetime.datetime(2022, 3, 1)
# end = datetime.datetime(2023, 4, 9)

# # Find weather stations in Santa Clara County
# stations = Stations()
# stations = stations.nearby(37.3541, -121.9552)  # Santa Clara County coordinates
# stations_list = stations.fetch(1)  # Get the 10 closest stations

# # Add the station ID, latitude, and longitude as new columns
#     data['station_id'] = station_id
#     data['latitude'] = station_info['latitude']
#     data['longitude'] = station_info['longitude']