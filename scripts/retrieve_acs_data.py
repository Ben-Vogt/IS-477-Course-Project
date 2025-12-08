from dotenv import load_dotenv
import os
import requests
import json
import time
import pandas as pd
from scripts import util
from scripts.compute_checksums import compute_file_checksum, load_checksums

def verify_file_checksum(filepath, year, data_type="acs_data"):
    """Verify a file's checksum matches the stored value. Returns True if valid, False if invalid, None if no checksum exists."""
    checksums = load_checksums(year)
    filename = os.path.basename(filepath)
    
    if filename not in checksums[data_type]:
        return None  # No checksum recorded yet
    
    expected_checksum = checksums[data_type][filename]
    actual_checksum = compute_file_checksum(filepath)
    return actual_checksum == expected_checksum

def retrieve_acs_data(year, states="all"):
    """
    Retrieve ACS (American Community Survey) data for various demographic data fields.
    Saves the data in the data/5_year_data/[year] directory
    
    Parameters:
    -----------
    year : int
        Year to retrieve data for
    states : str or list, default="all"
        State(s) to retrieve data for. Use "all" for all states or provide state name(s).
    
    Returns:
    None

    """
    
    load_dotenv(dotenv_path=".env")
    census_api_key = os.getenv("CENSUS_API_KEY")
    email = os.getenv("EMAIL")
    api_key = os.getenv("API_KEY")

    if not api_key or not email or not census_api_key:
        raise ValueError("Both API keys and email must be provided")
    
    # Deadass forgot to save the state codes, so just request them again from EPA... census uses the same ones anyways mb
    params = {"email": email, "key": api_key}
    states_response = requests.get("https://aqs.epa.gov/data/api/list/states", params=params)
    state_codes = {}
    for state in states_response.json().get('Data', []):
        state_codes[state.get('value_represented')] = state.get('code')

    # Determine which states to query
    if states == "all":
        state_code_list = list(state_codes.values())
    else:
        if isinstance(states, str):
            states = [states]
        state_code_list = [state_codes.get(state) for state in states if state in state_codes]
        if not state_code_list:
            raise ValueError(f"Invalid state name(s): {states}")
    
    if not os.path.exists(f"data/5_year_data/{year}"):
        os.makedirs(f"data/5_year_data/{year}")

     # Get state names for logging
    state_code_to_name = {v: k for k, v in state_codes.items()}

    # Request all variables from each table group of interest
    table_groups = {
        "B01003": "Total Population",
        "B02001": "Race",
        "B03003": "Hispanic Origin",
        "B19013": "Median Household Income",
        "B17001": "Poverty",
        "B15003": "Educational Attainment",
        "B01001": "Age Structure"
    }

    print("Fetching metadata for table groups:")
    relevant_variables = util.get_relevant_variables()
    
    # Write Census variable metadata to census_metadata.md
    with open("artifacts/census_metadata.md", "w", encoding="utf-8") as f:
        f.write("# Census ACS 5-Year (2020) Variable Metadata\n\n")
        f.write(f"**Total Variables:** {len(relevant_variables)}\n\n")
        f.write("**Table Groups:**\n")
        for code, name in table_groups.items():
            f.write(f"- {code}: {name}\n")
        f.write("\n---\n\n")
        
        # Group variables by table
        for table_code, table_name in table_groups.items():
            f.write(f"## {table_code}: {table_name}\n\n")
            
            # Get all variables for this table
            table_vars = {k: v for k, v in relevant_variables.items() if v.get("group") == table_code}
            
            # Get the concept from any variable in this table (they all share the same concept)
            concept = next(iter(table_vars.values())).get("concept", "N/A") if table_vars else "N/A"
            f.write(f"**Concept:** {concept}\n\n")
            
            f.write(f"**Variables in this table:** {len(table_vars)}\n\n")
            
            # Separate by suffix type
            estimates = {k: v for k, v in table_vars.items() if k.endswith("E")}
            margins = {k: v for k, v in table_vars.items() if k.endswith("M")}
            annotations_e = {k: v for k, v in table_vars.items() if k.endswith("EA")}
            annotations_m = {k: v for k, v in table_vars.items() if k.endswith("MA")}
            
            f.write(f"- Estimates (E): {len(estimates)}\n")
            f.write(f"- Margins of Error (M): {len(margins)}\n")
            f.write(f"- Estimate Annotations (EA): {len(annotations_e)}\n")
            f.write(f"- Margin Annotations (MA): {len(annotations_m)}\n\n")
            
            # Write estimate variables with their metadata
            f.write("### Estimate Variables\n\n")
            for var_code in sorted(estimates.keys()):
                var_info = estimates[var_code]
                f.write(f"#### `{var_code}`\n\n")
                f.write(f"**Label:** {var_info.get('label', 'N/A')}\n\n")
                f.write(f"**Type:** {var_info.get('predicateType', 'N/A')}\n\n")
                
                # Show related attributes
                attrs = var_info.get('attributes', '')
                if attrs:
                    f.write(f"**Related Variables:** `{attrs}`\n\n")
                
                f.write("---\n\n")
    
    print(f"Wrote metadata for {len(relevant_variables)} variables to artifacts/census_metadata.md")
    
    for i, state_code in enumerate(state_code_list, 1):
        state_name = state_code_to_name.get(state_code, "Unknown")
        print(f"Preparing to fetch data for state {i} / {len(state_code_list)}: {state_name} (code: {state_code})")

        filepath = f"data/5_year_data/{year}/census_state_data_{state_code}.json"
        if os.path.exists(filepath):
            # Verify checksum of existing file
            checksum_result = verify_file_checksum(filepath, year, "acs_data")
            if checksum_result is True:
                print(f"Census data for state code {state_code} already exists and checksum is valid. Skipping download.")
                continue
            elif checksum_result is False:
                print(f"Census data for state code {state_code} exists but checksum is INVALID. Re-downloading...")
                os.remove(filepath)
            else:
                print(f"Census data for state code {state_code} already exists but no checksum on record. Verifying by re-download.")
                os.remove(filepath)

        # Fetch each table group separately (Census API only allows one group per request)
        all_tables_data = {}
        for table_code, table_name in table_groups.items():
            print(f"  Fetching {table_name} ({table_code})...")
            if os.path.exists(f"data/5_year_data/{year}/census_state_data_{state_code}.json"):
                print(f"  Data for {table_name} already exists. Skipping.")
                continue
            params = {
                "get": f"group({table_code})",
                "for": "county:*",
                "in": f"state:{state_code}",
                "key": census_api_key
            }
            
            table = requests.get(f"https://api.census.gov/data/{year}/acs/acs5", params=params)

            if table.status_code == 204:
                print(f"  No data available for {table_name}: Check that this isn't in error.")
                all_tables_data[table_code] = None
            elif table.status_code != 200:
                print(f"Failed to retrieve {table_name} for state code {state_code}. Status code: {table.status_code}")
                print(f"Error message: {table.text}")
                raise Exception(f"API request failed with status code {table.status_code}: {table.text}")
            else:
                all_tables_data[table_code] = table.json()
            
            time.sleep(2)  # be nice

        filepath = f"data/5_year_data/{year}/census_state_data_{state_code}.json"
        with open(filepath, "w") as f:
            json.dump(all_tables_data, f)
        print(f"Saved census data for state code {state_code}")
        time.sleep(5) # be nice

retrieve_acs_data(2020, states="all")

