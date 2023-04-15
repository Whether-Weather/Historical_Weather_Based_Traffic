import pandas as pd
import zipfile
import os
import io

def read_and_combine_csvs_from_zips(folder_path = '/Users/joshkelleran/SeniorDesign/Whether-Weather/Historical_Weather_Based_Traffic/data/input_data/inrix/SantaClara',
                                    name='data.csv', 
                                    columns_to_keep = ['Date Time', 'Segment ID', 'Speed(km/hour)', 'Hist Av Speed(km/hour)', 'Ref Speed(km/hour)', "Road Closure"]
                                    ):
    
    dfs = []
   
    walked = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('santa_clara_2022-03-01_to_2022-04-01_60_min_part_1.zip'):
                zip_file_path = os.path.join(root, file)
                with zipfile.ZipFile(zip_file_path, 'r') as z:
                    for zipped_file in z.namelist():
                        if zipped_file.endswith("/" + name):
                            with z.open(zipped_file) as f:
                                df = pd.read_csv(io.TextIOWrapper(f), usecols=columns_to_keep)
                                dfs.append(df)
                                walked.append(zipped_file)
    
    print(walked)
    combined_df = pd.concat(dfs, ignore_index=True)
    
    return combined_df


# Example usage
if __name__ == '__main__':
    folder_path = '/Users/joshkelleran/SeniorDesign/Whether-Weather/Historical_Weather_Based_Traffic/data/input_data/inrix/SantaClara'
    combined_dataframe = read_and_combine_csvs_from_zips(folder_path)
    print(combined_dataframe)
