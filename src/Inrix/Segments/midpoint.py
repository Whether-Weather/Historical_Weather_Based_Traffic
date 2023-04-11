import csv
import json

# Open the CSV file and read the data
with open('metadata.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Create a dictionary with the midpoint of each segment as the value
midpoints = {}
for row in data:
    start_lat, end_lat = float(row['Start Latitude']), float(row['End Latitude'])
    start_lon, end_lon = float(row['Start Longitude']), float(row['End Longitude'])
    mid_lat = (start_lat + end_lat) / 2
    mid_lon = (start_lon + end_lon) / 2
    midpoint = (mid_lat, mid_lon)
    midpoints[row['Segment ID']] = midpoint

with open('midpoints.json', 'w') as fp:
        json.dump(midpoints, fp)

