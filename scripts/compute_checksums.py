import hashlib
import json
import os
from pathlib import Path

def compute_file_checksum(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def compute_all_checksums(year):
    checksums = {
        "aqs_data": {},
        "acs_data": {}
    }
    
    aqs_dir = Path(f"data/annual_data/{year}")
    if aqs_dir.exists():
        print(f"Computing checksums for AQS data in {aqs_dir}...")
        for file in sorted(aqs_dir.glob("state_data_*.json")):
            checksum = compute_file_checksum(file)
            checksums["aqs_data"][file.name] = checksum
            print(f"  {file.name}: {checksum}")
    
    acs_dir = Path(f"data/5_year_data/{year}")
    if acs_dir.exists():
        print(f"Computing checksums for ACS data in {acs_dir}...")
        for file in sorted(acs_dir.glob("census_state_data_*.json")):
            checksum = compute_file_checksum(file)
            checksums["acs_data"][file.name] = checksum
            print(f"  {file.name}: {checksum}")
    
    return checksums

def save_checksums(checksums, year):
    os.makedirs("artifacts", exist_ok=True)
    checksum_file = f"artifacts/checksums_{year}.json"
    with open(checksum_file, "w") as f:
        json.dump(checksums, f, indent=2, sort_keys=True)
    
    print(f"\nChecksums saved to {checksum_file}")
    print(f"Total AQS files: {len(checksums['aqs_data'])}")
    print(f"Total ACS files: {len(checksums['acs_data'])}")

def load_checksums(year):
    checksum_file = f"artifacts/checksums_{year}.json"
    if os.path.exists(checksum_file):
        with open(checksum_file, "r") as f:
            return json.load(f)
    return {"aqs_data": {}, "acs_data": {}}

def verify_file_checksum(filepath, expected_checksum):
    if not os.path.exists(filepath):
        return False
    actual_checksum = compute_file_checksum(filepath)
    return actual_checksum == expected_checksum

if __name__ == "__main__":
    year = 2020
    checksums = compute_all_checksums(year)
    save_checksums(checksums, year)
