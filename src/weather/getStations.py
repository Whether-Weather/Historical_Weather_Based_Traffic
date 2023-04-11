import ftplib
import pandas as pd

# # Connect to the FTP server
# ftp = ftplib.FTP("ftp.ncdc.noaa.gov")
# ftp.login()

# # Change to the directory containing the station list file
# ftp.cwd("pub/data/ghcn/daily")

# # Download the station list file
# with open("ghcnd-stations.txt", "wb") as file:
#     ftp.retrbinary("RETR ghcnd-stations.txt", file.write)

# # Close the FTP connection
# ftp.quit()

# Read the station list file
with open("ghcnd-stations.txt", "r") as file:
    station_list = file.readlines()


data = []
for line in station_list:
    station_id = line[0:11].strip()
    latitude = float(line[12:20].strip())
    longitude = float(line[21:30].strip())
    elevation = float(line[31:37].strip())
    station_name = line[41:].strip()
    data.append([station_id, latitude, longitude, elevation, station_name])

# Create a DataFrame from the parsed data
columns = ["station_id", "latitude", "longitude", "elevation", "station_name"]
df = pd.DataFrame(data, columns=columns)

# Define the coordinates of Santa Clara County
min_latitude, max_latitude = 37.055, 37.484
min_longitude, max_longitude = -122.006, -121.164

# Filter the DataFrame to get weather stations in Santa Clara County
santa_clara_stations = df[
    (df["latitude"] >= min_latitude)
    & (df["latitude"] <= max_latitude)
    & (df["longitude"] >= min_longitude)
    & (df["longitude"] <= max_longitude)
]

# Print the list of weather stations in Santa Clara County
print(santa_clara_stations[["station_id", "station_name", "latitude", "longitude"]])


