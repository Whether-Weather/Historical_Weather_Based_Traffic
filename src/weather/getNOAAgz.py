import requests
from bs4 import BeautifulSoup
import tarfile
import io
import csv
import json
import concurrent.futures

url = "https://www.ncei.noaa.gov/data/global-hourly/archive/csv/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Function to process a single CSV file and return a dictionary
def process_csv_file(file):
    data = {}
    reader = csv.DictReader(file)
    for row in reader:
        station = row["STATION"]
        if station not in data:
            data[station] = []
        data[station].append(row)
    return data

# Function to process a single tar.gz file
def process_tar_gz(file_name):
    data = {}
    print(f"Processing {file_name}")
    file_url = url + file_name
    file_response = requests.get(file_url)

    with tarfile.open(fileobj=io.BytesIO(file_response.content), mode="r:gz") as tar:
        for member in tar.getmembers():
            if member.isfile() and member.name.endswith(".csv"):
                csv_file = tar.extractfile(member)
                file_data = process_csv_file(io.TextIOWrapper(csv_file))
                
                # Merge the file data into the main dictionary
                for station, records in file_data.items():
                    if station not in data:
                        data[station] = []
                    data[station].extend(records)
    return data

# Main dictionary to store all data
all_data = {}

# Find all tar.gz files
tar_gz_files = [link['href'] for link in soup.find_all('a', href=True) if link['href'].endswith('.tar.gz')]

tar_gz_files = tar_gz_files[122:123]

# Process the tar.gz files using multiple threads
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(process_tar_gz, tar_gz_files)
    for result in results:
        for station, records in result.items():
            if station not in all_data:
                all_data[station] = []
            all_data[station].extend(records)

print("All data processed.")

# Save the compiled data to a JSON file
with open('weather_data.json', 'w') as json_file:
    json.dump(all_data, json_file)

print("Data saved to weather_data.json.")
