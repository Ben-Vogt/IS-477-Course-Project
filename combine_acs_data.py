import pandas as pd
import json
import os

def combine_acs_data(year):
    
    data_dir = f"data/5_year_data/{year}"
    acs_dfs = []
    for file_name in os.listdir(data_dir):
        if file_name.endswith(".json"):
            file_path = os.path.join(data_dir, file_name)
            acs_json = json.load(open(file_path, 'r'))
            table_groups = {
                    "B01003": "Total Population",
                    "B02001": "Race",
                    "B03003": "Hispanic Origin",
                    "B19013": "Median Household Income",
                    "B17001": "Poverty",
                    "B15003": "Educational Attainment",
                    "B01001": "Age Structure"
                }
            # Parse data for each table group
            groups = [acs_json[group] for group in table_groups.keys()]
            dfs = []
            for group in groups:
                headers = group[0]  # First row is column names
                data = group[1:]     # Rest is actual data
                df = pd.DataFrame(data, columns=headers)
                dfs.append(df)
            assert len(dfs[0]) == len(dfs[1]) == len(dfs[2]) == len(dfs[3]) == len(dfs[4]) == len(dfs[5]) == len(dfs[6])

            df_acs = pd.DataFrame()
            for i in range(len(dfs)):
                df_acs = pd.merge(df_acs, dfs[i], on=["county", "GEO_ID", "NAME", "state"], how="outer") if not df_acs.empty else dfs[i]
            acs_dfs.append(df_acs)
    
    df_acs = pd.concat(acs_dfs, ignore_index=True)
    df_acs.to_csv(f"data/combined_data/{year}/combined_acs_data_{year}.csv", index=False)
    print(f"Combined ACS data saved to data/combined_data/{year}/combined_acs_data_{year}.csv")

if __name__ == "__main__":
    combine_acs_data(2020)