import datetime
import pickle
import sys
from pathlib import Path
import io

import pandas as pd
import os

gen_dir = str(Path(__file__).resolve().parents[2])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)

folder_path = gen_dir + "/data/created_data/SantaClara/all"
output_path = folder_path + "/pickle"

# Create the output directory if it doesn't exist
if not os.path.exists(output_path):
    os.makedirs(output_path)

# List all the CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Create a list of file paths
file_paths = [os.path.join(folder_path, file) for file in csv_files]

for file in file_paths:
    df = pd.read_csv(file)

    # Write the DataFrame to a pickle file
    pickle_file = os.path.join(output_path, f"{os.path.splitext(os.path.basename(file))[0]}.pkl")
    df.to_pickle(pickle_file)

    # Read the DataFrame from the pickle file
    #df_from_pickle = pd.read_pickle(pickle_file)

    