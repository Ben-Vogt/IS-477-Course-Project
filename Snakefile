# Snakemake workflow for IS-477 Course Project
# Retrieves and cleans AQS and ACS data for 2020

YEAR = "2020"

rule all:
    input:
        f"artifacts/results_{YEAR}.md",
        directory(f"maps/{YEAR}/")

rule retrieve_aqs:
    input:
        script="scripts/retrieve_aqs_data.py",
    output:
        touch(f"data/annual_data/{YEAR}/.retrieve_aqs_complete"),
        "artifacts/metadata.md"
    script:
        "scripts/retrieve_aqs_data.py"

rule retrieve_acs:
    input:
        script="scripts/retrieve_acs_data.py",
        util="scripts/util.py",
        env=".env"
    output:
        touch(f"data/5_year_data/{YEAR}/.retrieve_acs_complete"),
        "artifacts/census_metadata.md"
    script:
        "scripts/retrieve_acs_data.py"

rule combine_aqs:
    input:
        flag=f"data/annual_data/{YEAR}/.retrieve_aqs_complete",
        script="scripts/combine_aqs_data.py"
    output:
        f"data/combined_data/{YEAR}/combined_aqs_data_{YEAR}.csv"
    script:
        "scripts/combine_aqs_data.py"

rule combine_acs:
    input:
        flag=f"data/5_year_data/{YEAR}/.retrieve_acs_complete",
        script="scripts/combine_acs_data.py"
    output:
        f"data/combined_data/{YEAR}/combined_acs_data_{YEAR}.csv"
    script:
        "scripts/combine_acs_data.py"

rule clean_aqs:
    input:
        data=f"data/combined_data/{YEAR}/combined_aqs_data_{YEAR}.csv",
        script="scripts/clean_aqs_data.py"
    output:
        f"data/cleaned_data/{YEAR}/cleaned_aqs_data_{YEAR}.csv"
    script:
        "scripts/clean_aqs_data.py"

rule clean_acs:
    input:
        data=f"data/combined_data/{YEAR}/combined_acs_data_{YEAR}.csv",
        script="scripts/clean_acs_data.py",
        util="scripts/util.py"
    output:
        f"data/cleaned_data/{YEAR}/cleaned_acs_data_{YEAR}.csv"
    script:
        "scripts/clean_acs_data.py"

rule integrate_data:
    input:
        acs=f"data/cleaned_data/{YEAR}/cleaned_acs_data_{YEAR}.csv",
        aqs=f"data/cleaned_data/{YEAR}/cleaned_aqs_data_{YEAR}.csv",
        script="scripts/integration.py"
    output:
        f"data/integrated_data/integrated_data_{YEAR}.csv",
        f"artifacts/integration_report_{YEAR}.md"
    script:
        "scripts/integration.py"

rule analyze_data:
    input:
        data=f"data/integrated_data/integrated_data_{YEAR}.csv",
        script="scripts/analysis.py"
    output:
        directory(f"maps/{YEAR}/"),
        f"artifacts/results_{YEAR}.md",
        directory(f"models/{YEAR}/")
    script:
        "scripts/analysis.py"