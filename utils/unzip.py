import pandas as pd
import zipfile
import os
import io

def get_zip_files(folder_path = '/Users/joshkelleran/SeniorDesign/Whether-Weather/Historical_Weather_Based_Traffic/data/input_data/inrix/SantaClara'):
    walked = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.zip'):
                zip_file_path = os.path.join(root, file)
                walked.append(zip_file_path)
                    
    return walked

def get_combined_files(folder_path):
    walked = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('combined.pkl'):
                zip_file_path = os.path.join(root, file)
                walked.append(zip_file_path)
                    
    return walked


def read_csvs_from_zips(folder_path = '/Users/joshkelleran/SeniorDesign/Whether-Weather/Historical_Weather_Based_Traffic/data/input_data/inrix/SantaClara',
                                    name='data.csv', 
                                    columns_to_keep = ['Date Time', 'Segment ID', 'Speed(km/hour)', 'Hist Av Speed(km/hour)', 'Ref Speed(km/hour)', "Road Closure"],
                                    files = []):
    dfs = []
    if not files:
        files = get_zip_files(folder_path)
    for file in files:
        with zipfile.ZipFile(file, 'r') as z:
            for zipped_file in z.namelist():
                if zipped_file.endswith("/" + name):
                    with z.open(zipped_file) as f:
                        df = pd.read_csv(io.TextIOWrapper(f), usecols=columns_to_keep)
                        dfs.append(df)
                        
    # combined_df = pd.concat(dfs, ignore_index=True)
    return dfs


# Example usage
if __name__ == '__main__':
    folder_path = '/Users/joshkelleran/SeniorDesign/Whether-Weather/Historical_Weather_Based_Traffic/data/input_data/inrix/SantaClara'
    #combined_dataframe = read_and_combine_csvs_from_zips(folder_path)
    read_csvs_from_zips()

    
