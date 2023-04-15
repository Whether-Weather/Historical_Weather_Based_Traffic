import datetime
import json

from meteostat import Hourly, Stations

midpoint_dict_file_path = 'midpoints.json'
segment_data_file_path = 'segment_data.json'

# Set the time range
start = datetime.datetime(2022, 3, 1)
end = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=1)

# Initialize meteostat Stations 
stations = Stations()


# Caching Station Data 
whetherStations = {}

# Get midpoint Dict 
with open(midpoint_dict_file_path) as json_file:
    midpoints = json.load(json_file)
    
# Get segment data Dict
with open(segment_data_file_path) as json_file:
    segments = json.load(json_file)
    
    
# Loop Through Segments 
for seg,info in segments:
    #TODO: If weather data exists pass
    
    # Get midpoint Lat and Long
    Lat,Long = midpoints[seg]
    
    # Find closest station
    stations = stations.nearby(Lat,Long)
    station_id,station_info = stations.fetch(1)
    data = None
    
    # If data isn't cached, then call api and cache, otherwise take from cache
    if station_id not in whetherStations:
        data = Hourly(station_id, start, end)
        data = data.fetch()
        whetherStations[station_id] = data
    else:
        data = whetherStations[station_id]
    
    
    # Append weather data to each time in road data
    for time in info['Times'].keys():
        info['Times'][time].append(data['time'])
        
    
    
    
    
    
    
    