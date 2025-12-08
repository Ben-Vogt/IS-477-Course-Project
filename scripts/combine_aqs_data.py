import pandas as pd
import os
import json

def combine_aqs_data(year):
    data_dir = f"data/annual_data/{year}"
    combined_file = f"combined_aqs_data_{year}.csv"
    data_frames = []

    for file_name in os.listdir(data_dir):
        if file_name.endswith(".json"):
            file_path = os.path.join(data_dir, file_name)
            json_data = json.load(open(file_path, 'r'))
            
            # Convert JSON data to DataFrame
            df = pd.json_normalize(json_data['Data'])
            data_frames.append(df)

    combined_df = pd.concat(data_frames, ignore_index=True)
    combined_df.to_csv(f"data/combined_data/{year}/{combined_file}", index=False)
    print(f"Combined data saved to {combined_file}")

if __name__ == "__main__":
    combine_aqs_data(2020)