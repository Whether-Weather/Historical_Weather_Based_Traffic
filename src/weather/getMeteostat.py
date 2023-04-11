import datetime
import pandas as pd
from meteostat import Stations, Hourly

# Set the time range
start = datetime.datetime(2022, 3, 1)
end = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=1)

# Find weather stations in Santa Clara County
stations = Stations()
stations = stations.nearby(37.3541, -121.9552)  # Santa Clara County coordinates
stations_list = stations.fetch(10)  # Get the 10 closest stations

all_data = pd.DataFrame()

for station_id, station_info in stations_list.iterrows():
    # Get hourly weather data for the station
    data = Hourly(station_id, start, end)
    data = data.fetch()

    # Add the station ID, latitude, and longitude as new columns
    data['station_id'] = station_id
    data['latitude'] = station_info['latitude']
    data['longitude'] = station_info['longitude']

    # Concatenate the data from each station
    all_data = pd.concat([data, all_data])

# Save the data to a CSV file, including the date and time
all_data.to_csv('weather_data_santa_clara_county.csv')

print("Weather data saved to weather_data_santa_clara_county.csv.")

