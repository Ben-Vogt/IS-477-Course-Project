import pandas as pd
import os

def clean_aqs_data(year):
    
    # Load the raw AQS data
    df = pd.read_csv(f"data/combined_data/{year}/combined_aqs_data_{year}.csv")
    
    # Data cleaning steps
    
    # 1. Drop rows with missing sample_measurement - I can't use these
    df.dropna(subset=["sample_measurement"], inplace=True)
    print(f"After dropping NaN measurements: {len(df)} records")
    
    # 2. Replace measurements below detection limit with 1/2 of detection limit. Anything less than detection_limit is unreliable.
    mask = df["sample_measurement"] < df["detection_limit"]
    df.loc[mask, "sample_measurement"] = df.loc[mask, "detection_limit"] / 2
    print(f"Replaced {mask.sum()} measurements below detection limit")
    
    # 3. Remove the highest 0.01% outliers for each parameter. Catches potential faulty readings from busted sensors.
    outliers = df.groupby("parameter", group_keys=False).apply(
        lambda x: x[x["sample_measurement"] >= x["sample_measurement"].quantile(0.9999)], 
        include_groups=False
    )
    df = df[~df.index.isin(outliers.index)]
    print(f"Removed {len(outliers)} outlier points. Remaining: {len(df)} records")
    
    # 4. Deduplication based on key columns. 
    duplicate_cols = ['state_code', 'site_number', 'parameter', 'date_gmt', 'time_gmt', 'poc']
    before_count = len(df)
    df = df.drop_duplicates(subset=duplicate_cols, keep='first')
    print(f"Removed {before_count - len(df)} duplicate records")
    
    print(f"\nFinal cleaned dataset: {len(df)} records")

    # Save cleaned data
    if not os.path.exists(f"data/cleaned_data/{year}"):
        os.makedirs(f"data/cleaned_data/{year}")

    df.to_csv(f"data/cleaned_data/{year}/cleaned_aqs_data_{year}.csv", index=False)
    print(f"Cleaned data saved to data/cleaned_data/{year}/cleaned_aqs_data_{year}.csv")

if __name__ == "__main__":
    clean_aqs_data(2020)