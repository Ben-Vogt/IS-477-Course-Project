# Snakemake workflow for IS-477 Course Project
# Retrieves and cleans AQS and ACS data for 2020

YEAR = "2020"

rule all:
    input:
        f"data/cleaned_data/{YEAR}/cleaned_acs_data_{YEAR}.csv",
        f"data/cleaned_data/{YEAR}/cleaned_aqs_data_{YEAR}.csv"

rule retrieve_aqs:
    input:
        script="retrieve_aqs_data.py",
        env=".env"
    output:
        directory(f"data/annual_data/{YEAR}/")
    script:
        "retrieve_AQS_data.py"

rule retrieve_acs:
    input:
        script="retrieve_acs_data.py",
        util="util.py",
        env=".env"
    output:
        directory(f"data/5_year_data/{YEAR}/")
    script:
        "retrieve_acs_data.py"

rule combine_aqs:
    input:
        data=f"data/annual_data/{YEAR}/",
        script="combine_aqs_data.py"
    output:
        f"data/combined_data/{YEAR}/combined_aqs_data_{YEAR}.csv"
    script:
        "combine_aqs_data.py"

rule combine_acs:
    input:
        data=f"data/5_year_data/{YEAR}/",
        script="combine_acs_data.py"
    output:
        f"data/combined_data/{YEAR}/combined_acs_data_{YEAR}.csv"
    script:
        "combine_acs_data.py"

rule clean_aqs:
    input:
        data=f"data/combined_data/{YEAR}/combined_aqs_data_{YEAR}.csv",
        script="clean_aqs_data.py"
    output:
        f"data/cleaned_data/{YEAR}/cleaned_aqs_data_{YEAR}.csv"
    script:
        "clean_aqs_data.py"

rule clean_acs:
    input:
        data=f"data/combined_data/{YEAR}/combined_acs_data_{YEAR}.csv",
        script="clean_acs_data.py",
        util="util.py"
    output:
        f"data/cleaned_data/{YEAR}/cleaned_acs_data_{YEAR}.csv"
    script:
        "clean_acs_data.py"
