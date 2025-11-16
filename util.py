import requests
import json
import os
import pandas as pd


def get_relevant_variables():

    table_groups = {
        "B01003": "Total Population",
        "B02001": "Race",
        "B03003": "Hispanic Origin",
        "B19013": "Median Household Income",
        "B17001": "Poverty",
        "B15003": "Educational Attainment",
        "B01001": "Age Structure"
    }

    url = "https://api.census.gov/data/2020/acs/acs5/variables.json"
    response = requests.get(url)
    relevant_variables = {}
    variables_metadata = response.json()["variables"]
    for variable_code, variable_info in variables_metadata.items():
        if variable_info.get("group", "") in table_groups.keys():
            relevant_variables[variable_code] = variable_info
    return relevant_variables