import requests
import datetime

station_id = "KSJC"
https://api.weather.gov/stations/{station_id}/observations?start=2022-03-01T00:00:00Z
headers = {
    "Accept": "application/geo+json",
    "User-Agent": "my-weather-app"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")
