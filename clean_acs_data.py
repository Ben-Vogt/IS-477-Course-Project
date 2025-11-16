import pandas as pd
import json
import os
import util

def clean_census_data(year):
    # Load data
    df = pd.read_csv(f"data/combined_data/{year}/combined_acs_data_{year}.csv")
    relevant_variables = util.get_relevant_variables()
    print(f"Initial dataset contains {len(df)} records and {len(df.columns)} columns")

    # Convert cryptic variable codes to their more descritive labels
    rename_dict = {}
    for col in df.columns:
        if col in relevant_variables:
            var_info = relevant_variables[col]
            descriptive_name = f"{var_info['group']} - {var_info['label']}"
            rename_dict[col] = descriptive_name
            
    df.rename(columns=rename_dict, inplace=True)
    
    # Handle rows with the Census Bureau's special codes for missing data
    census_sentinel_values = {
    -666666666: "Insufficient sample observations (or ratio of medians issue)",
    -999999999: "Insufficient sample cases in geographic area",
    -888888888: "Not applicable or not available",
    -222222222: "Margin of error could not be computed (insufficient samples)",
    -333333333: "Margin of error could not be computed (median in open-ended interval)",
    -555555555: "Margin of error not appropriate (estimate controlled to independent population)",
    "null": "Data not available"
    }
    sentinel_list = list(census_sentinel_values.keys())
    df.replace(sentinel_list, pd.NA, inplace=True)




    # Write cleaned data at the end
    if not os.path.exists(f"data/cleaned_data/{year}"):
        os.makedirs(f"data/cleaned_data/{year}")
    
    df.to_csv(f"data/cleaned_data/{year}/cleaned_acs_data_{year}.csv", index=False)

if __name__ == "__main__":
    clean_census_data(2020)
    