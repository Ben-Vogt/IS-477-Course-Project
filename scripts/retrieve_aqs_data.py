import pandas as pd
import requests
import json
import time
from dotenv import load_dotenv
import os
from scripts.compute_checksums import compute_file_checksum, load_checksums

def verify_file_checksum(filepath, year):
    """Verify a file's checksum matches the stored value. Returns True if valid, False if invalid, None if no checksum exists."""
    checksums = load_checksums(year)
    filename = os.path.basename(filepath)
    
    if filename not in checksums["aqs_data"]:
        return None  # No checksum recorded yet
    
    expected_checksum = checksums["aqs_data"][filename]
    actual_checksum = compute_file_checksum(filepath)
    return actual_checksum == expected_checksum

def retrieve_AQS_data(year, states="all"):
    """
    Retrieve AQS (Air Quality System) data for 3 key criteria pollutants.
    Saves the data in the data/annual_data/[year] directory
    
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
    email = os.getenv("EMAIL")
    api_key = os.getenv("API_KEY")
    
    if not api_key or not email:
        raise ValueError("API key and email must be provided")
    
    # Get metadata for the sampleData service
    params = {
        "email": email,
        "key": api_key,
        "service": "sampleData"
    }


    metadata = requests.get("https://aqs.epa.gov/data/api/metaData/fieldsByService", params=params)

    response_json = metadata.json()
    metadata_dict = response_json.get("Data", [])

    # Write metadata to a nicely formatted markdown file
    with open("artifacts/metadata.md", "w", encoding="utf-8") as f:
        f.write("# API Metadata Fields\n\n")
        f.write(f"**Service:** sampleData\n\n")
        f.write(f"**Total Fields:** {len(metadata_dict)}\n\n")
        f.write("---\n\n")
        
        for i, field in enumerate(metadata_dict, 1):
            f.write(f"## {i}. {field.get('field_name', 'N/A')}\n\n")
            f.write(f"{field.get('field_description', 'N/A')}")
            f.write("\n")

    print("Metadata written to artifacts/metadata.md")

    # Get state codes mapping
    params = {"email": email, "key": api_key}
    states_response = requests.get("https://aqs.epa.gov/data/api/list/states", params=params)
    state_codes = {}
    for state in states_response.json().get('Data', []):
        state_codes[state.get('value_represented')] = state.get('code')
    
    # Define criteria pollutants: limited to save memory, as 
    criteria_params = {
        "PM2.5": "88101",
        "Ozone": "44201",
        "Nitrogen dioxide (NO2)": "42602",
    }
    
    # Determine which states to query
    if states == "all":
        state_code_list = list(state_codes.values())
    else:
        if isinstance(states, str):
            states = [states]
        state_code_list = [state_codes.get(state) for state in states if state in state_codes]
        if not state_code_list:
            raise ValueError(f"Invalid state name(s): {states}")
    
    if not os.path.exists(f"data/annual_data/{year}"):
        os.makedirs(f"data/annual_data/{year}")

    # Get state names for logging
    state_code_to_name = {v: k for k, v in state_codes.items()}
    
    for i, state_code in enumerate(state_code_list, 1):
        state_name = state_code_to_name.get(state_code, "Unknown")
        print(f"Preparing to fetch data for state {i} / {len(state_code_list)}: {state_name} (code: {state_code})")

        filepath = f"data/annual_data/{year}/state_data_{state_code}.json"
        if os.path.exists(filepath):
            # Verify checksum of existing file
            checksum_result = verify_file_checksum(filepath, year)
            if checksum_result is True:
                print(f"Annual data for state code {state_code} already exists and checksum is valid. Skipping download.")
                continue
            elif checksum_result is False:
                print(f"Annual data for state code {state_code} exists but checksum is INVALID. Re-downloading...")
                os.remove(filepath)
            else:
                print(f"Annual data for state code {state_code} already exists but no checksum on record. Verifying by re-download.")
                os.remove(filepath)
    
        # Fetch data month by month
        all_data = []
        skip_state = False  # Flag to skip states that return persistent 400 errors
        months = [
            (f"{year}0101", f"{year}0131"), (f"{year}0201", f"{year}0228" if year % 4 != 0 else f"{year}0229"),
            (f"{year}0301", f"{year}0331"), (f"{year}0401", f"{year}0430"),
            (f"{year}0501", f"{year}0531"), (f"{year}0601", f"{year}0630"),
            (f"{year}0701", f"{year}0731"), (f"{year}0801", f"{year}0831"),
            (f"{year}0901", f"{year}0930"), (f"{year}1001", f"{year}1031"),
            (f"{year}1101", f"{year}1130"), (f"{year}1201", f"{year}1231")
        ]
        
        for month_num, (bdate, edate) in enumerate(months, 1):
            print(f"  Fetching month {month_num}/12 for state {state_code}...")
            
            params = {
                "email": email,
                "key": api_key,
                "param": ",".join(criteria_params.values()),
                "bdate": bdate,
                "edate": edate,
                "state": state_code
            }
            
            # Fetch data from API with retry logic
            max_retries = 1
            retry_delay = 15
            month_failed = False
            samples_data = None
            for attempt in range(max_retries):
                try:
                    samples = requests.get("https://aqs.epa.gov/data/api/sampleData/byState", params=params, timeout=60)
                    if samples.status_code == 200:
                        samples_data = samples.json()
                        break
                    elif samples.status_code == 400:
                        print(f"    API returned status code 400 (Bad Request) - state may be invalid")
                        month_failed = True
                        skip_state = True
                        break
                    else:
                        print(f"    API returned status code {samples.status_code}")
                        month_failed = True
                        break
                except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, json.JSONDecodeError) as e:
                    if attempt < max_retries - 1:
                        print(f"    Connection error on attempt {attempt + 1}. Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                    else:
                        print(f"    Month {month_num} failed after {max_retries} attempts. Trying half-month intervals...")
                        month_failed = True
            
            # If month request failed, try splitting into two half-month requests
            if month_failed:
                # Calculate midpoint of month
                start_date = bdate
                start_day = int(bdate[-2:])
                end_day = int(edate[-2:])
                mid_day = (start_day + end_day) // 2
                mid_date = f"{bdate[:-2]}{mid_day:02d}"
                next_day = mid_day + 1
                second_half_start = f"{bdate[:-2]}{next_day:02d}"
                
                half_months = [(start_date, mid_date), (second_half_start, edate)]
                half_failed = False
                
                for half_num, (half_bdate, half_edate) in enumerate(half_months, 1):
                    print(f"    Fetching half {half_num}/2 of month {month_num}...")
                    
                    params = {
                        "email": email,
                        "key": api_key,
                        "param": ",".join(criteria_params.values()),
                        "bdate": half_bdate,
                        "edate": half_edate,
                        "state": state_code
                    }
                    
                    max_retries = 5
                    retry_delay = 15
                    half_success = False
                    samples_data = None
                    for attempt in range(max_retries):
                        try:
                            samples = requests.get("https://aqs.epa.gov/data/api/sampleData/byState", params=params, timeout=120)
                            if samples.status_code == 200:
                                samples_data = samples.json()
                                half_success = True
                                break
                            elif samples.status_code == 400:
                                print(f"      API returned status code 400 (Bad Request) - state may be invalid")
                                half_failed = True
                                skip_state = True
                                break
                            else:
                                print(f"      API returned status code {samples.status_code}")
                                half_failed = True
                                break
                        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, json.JSONDecodeError) as e:
                            if attempt < max_retries - 1:
                                print(f"      Connection error on attempt {attempt + 1}. Retrying in {retry_delay} seconds...")
                                time.sleep(retry_delay)
                            else:
                                print(f"      Half-month failed after {max_retries} attempts. Trying weekly intervals...")
                                half_failed = True
                    
                    if half_success and samples_data and samples_data.get('Data'):
                        all_data.extend(samples_data['Data'])
                    elif half_failed:
                        # Split half-month into weekly intervals
                        from datetime import datetime, timedelta
                        start = datetime.strptime(half_bdate, "%Y%m%d")
                        end = datetime.strptime(half_edate, "%Y%m%d")
                        current = start
                        
                        while current <= end:
                            week_end = min(current + timedelta(days=6), end)
                            week_bdate = current.strftime("%Y%m%d")
                            week_edate = week_end.strftime("%Y%m%d")
                            
                            print(f"      Fetching week {week_bdate} to {week_edate}...")
                            
                            params = {
                                "email": email,
                                "key": api_key,
                                "param": ",".join(criteria_params.values()),
                                "bdate": week_bdate,
                                "edate": week_edate,
                                "state": state_code
                            }
                            
                            max_retries = 15
                            retry_delay = 15
                            samples_data = None
                            for attempt in range(max_retries):
                                try:
                                    samples = requests.get("https://aqs.epa.gov/data/api/sampleData/byState", params=params, timeout=180)
                                    if samples.status_code == 200:
                                        samples_data = samples.json()
                                        break
                                    elif samples.status_code == 400:
                                        print(f"        API returned status code 400 (Bad Request) - state {state_code} appears invalid")
                                        skip_state = True
                                        samples_data = None
                                        break
                                    else:
                                        print(f"        API returned status code {samples.status_code}")
                                        raise Exception(f"API error: {samples.status_code}")
                                except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, json.JSONDecodeError) as e:
                                    if attempt < max_retries - 1:
                                        print(f"        Connection error on attempt {attempt + 1}/{max_retries}. Retrying in {retry_delay} seconds...")
                                        time.sleep(retry_delay)
                                    else:
                                        print(f"        Failed to fetch week after {max_retries} attempts")
                                        raise
                            
                            if samples_data and samples_data.get('Data'):
                                all_data.extend(samples_data['Data'])
                            
                            current = week_end + timedelta(days=1)
                            time.sleep(5)
                    
                    time.sleep(1)
            else:
                if samples_data and samples_data.get('Data'):
                    all_data.extend(samples_data['Data'])
            
            # If state should be skipped due to persistent 400 errors, break out of month loop
            if skip_state:
                print(f"  Skipping remaining months for state {state_code} due to persistent API errors")
                break
            
            time.sleep(10)  # Be courteous between month requests
        
        # Combine all monthly data into single file with same structure
        if all_data:
            combined_data = {
                "Header": [{"status": "Success", "request_time": time.strftime("%Y-%m-%dT%H:%M:%S")}],
                "Data": all_data
            }
            filepath = f"data/annual_data/{year}/state_data_{state_code}.json"
            with open(filepath, "w") as f:
                json.dump(combined_data, f)
            print(f"Fetched and saved {len(all_data)} records for state code {state_code}")
        else:
            print(f"No data retrieved for state {state_code} ({state_name}). Skipping file creation.")
    
retrieve_AQS_data(2020, states="all")