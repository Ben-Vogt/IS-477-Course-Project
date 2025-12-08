import os
import pandas as pd

def integrate_data(year):
    """
    Integrate ACS and AQS data for the specified year.
    
    Parameters:
    -----------
    year : int
        Year to integrate data for
    
    Returns:
    None
    """
    
    acs_path = f"data/cleaned_data/{year}/cleaned_acs_data_{year}.csv"
    aqs_path = f"data/cleaned_data/{year}/cleaned_aqs_data_{year}.csv"
    
    if not os.path.exists(acs_path):
        raise FileNotFoundError(f"ACS data file not found: {acs_path}")
    if not os.path.exists(aqs_path):
        raise FileNotFoundError(f"AQS data file not found: {aqs_path}")
    
    acs_data = pd.read_csv(acs_path)
    aqs_data = pd.read_csv(aqs_path)

    aqs_stats = aqs_data.groupby(['state_code', 'county_code', 'parameter_code'])['sample_measurement'].agg(
        mean='mean',
        median='median',
        std='std'
    ).reset_index()

    acs_unique_counties = acs_data[['state', 'county']].drop_duplicates()
    aqs_unique_counties = aqs_stats[['state_code', 'county_code']].drop_duplicates()
    initial_acs_count = len(acs_unique_counties)
    initial_aqs_count = len(aqs_unique_counties)
    
    integrated_data = pd.merge(acs_data, aqs_stats, left_on=["state", "county"], right_on=["state_code", "county_code"], how='outer',indicator=True)
    
    both_count = len(integrated_data[integrated_data['_merge'] == 'both'])
    acs_only_count = len(integrated_data[integrated_data['_merge'] == 'left_only'])
    aqs_only_count = len(integrated_data[integrated_data['_merge'] == 'right_only'])
    acs_unmatched = integrated_data[integrated_data['_merge'] == 'left_only'][['state', 'county', 'NAME']].drop_duplicates()
    aqs_unmatched = integrated_data[integrated_data['_merge'] == 'right_only'][['state_code', 'county_code']].drop_duplicates()
    
    integrated_data_final = integrated_data[integrated_data['_merge'] == 'both'].drop(columns=['_merge'])
    final_unique_counties = integrated_data_final[['state', 'county']].drop_duplicates()
    final_county_count = len(final_unique_counties)

    output_path = f"data/integrated_data/integrated_data_{year}.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    integrated_data_final.to_csv(output_path, index=False)
    
    # Generate merge report
    os.makedirs("artifacts", exist_ok=True)
    report_path = f"artifacts/integration_report_{year}.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# Data Integration Report ({year})\n\n")
        f.write("## Summary\n\n")
        f.write(f"- **ACS Data (Counties):** {initial_acs_count:,}\n")
        f.write(f"- **AQS Data (Counties):** {initial_aqs_count:,}\n")
        f.write(f"- **Successfully Merged (Counties):** {final_county_count:,}\n")
        f.write(f"- **Final Integrated Records:** {len(integrated_data_final):,}\n\n")
        
        f.write("## Merge Statistics\n\n")
        f.write(f"- **Records with both ACS and AQS data:** {both_count:,}\n")
        f.write(f"- **Records with only ACS data (no air quality match):** {acs_only_count:,}\n")
        f.write(f"- **Records with only AQS data (no census match):** {aqs_only_count:,}\n\n")
        
        acs_match_rate = (final_county_count / initial_acs_count * 100) if initial_acs_count > 0 else 0
        aqs_match_rate = (final_county_count / initial_aqs_count * 100) if initial_aqs_count > 0 else 0
        
        f.write("## Match Rates\n\n")
        f.write(f"- **ACS counties with air quality data:** {acs_match_rate:.1f}%\n")
        f.write(f"- **AQS counties with census data:** {aqs_match_rate:.1f}%\n\n")
        
        if len(acs_unmatched) > 0:
            f.write(f"## ACS Counties Without Air Quality Data ({len(acs_unmatched)})\n\n")
            f.write("These counties have census data but no air quality monitoring stations:\n\n")
            f.write("| State Code | County Code | County Name |\n")
            f.write("|------------|-------------|-------------|\n")
            for _, row in acs_unmatched.head(50).iterrows():
                f.write(f"| {row['state']} | {row['county']} | {row['NAME']} |\n")
            if len(acs_unmatched) > 50:
                f.write(f"\n*... and {len(acs_unmatched) - 50} more counties*\n")
            f.write("\n")
        
        if len(aqs_unmatched) > 0:
            f.write(f"## AQS Monitoring Locations Without Census Data ({len(aqs_unmatched)})\n\n")
            f.write("These monitoring locations exist but do not match census county data:\n\n")
            f.write("| State Code | County Code |\n")
            f.write("|------------|-------------|\n")
            for _, row in aqs_unmatched.head(50).iterrows():
                f.write(f"| {row['state_code']} | {row['county_code']} |\n")
            if len(aqs_unmatched) > 50:
                f.write(f"\n*... and {len(aqs_unmatched) - 50} more locations*\n")
            f.write("\n")
    
    print(f"Integrated data saved to {output_path}")
    print(f"Integration report saved to {report_path}")
    print(f"Match rate: {acs_match_rate:.1f}% of ACS counties have air quality data")

if __name__ == "__main__":
    integrate_data(2020)