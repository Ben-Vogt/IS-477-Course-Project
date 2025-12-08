IS 477 - Interim Status Report

Benjamin Vogt (bavogt2)

11/16/2025

**Status Update:**

To begin with, my project is progressing relatively smoothly overall,
with only minor hitches. It took me longer than anticipated to figure
out how to use the two APIs that supply the data for this project. So
far, I have created and tested scripts for data retrieval, combination,
and cleaning for both datasets, as well as created a workflow with the
automation tool snakemake which we recently learned about in class that
will automatically perform all of the implemented steps to this point.
To go more in detail:

Data governance is not really something I had to think about before I
started my project. Both the EPA and Census Bureau datasets are
government datasets in the public domain, and so I can do whatever I
want with them, and access to them is provided to me free of charge by
the respective government agencies.

Data retrieval was complicated for both datasets in differing ways. The
EPA dataset is very long, or high volume. So many records. So much so,
that I decided to limit the scope of my analysis to a single year for
the time being, 2020. The 2020 sample data I retrieved for California
alone, for just 3 pollutants of interest, was around 2.5 GB in json
format. The volume of the data made API access to it tricky, as
requesting too much data at once caused my requests to the API to time
out. It took some time to figure out how to ensure that I could gather
all of the data without my script failing due to time outs. Even after
limiting the number of variables, and the temporal scope, the millions
of records I retrieved still take up a respectable 16.5GB of storage,
and so I have not included my data directory on github (git would not
like that). The script I created for this is called
**retrieve_aqs_data.py** and lives in the root directory of my project.
It outputs the data retrieved to
**data/annual_data/2020/state_data\_{state_code}.json** for each of the
FIPS state codes used by the government to identify the states. Each
file contains all of the AQS sample data for 3 criteria pollutants
(PM2.5 particulate matter, Ozone, and Nitrogen Dioxide) in the year
2020. It also generates a file called **metadata.md** that contains
information about the various fields in that dataset.

The second dataset used is the American Community Survey (ACS) 5-year
data collected by the US Census Bureau. The script responsible for
retrieving this data is called **retrieve_acs_data.py** and it lives in
the root directory of my project. The difficulty with the ACS dataset is
not the number of observations, but instead the number of fields. I
retrieved data aggregates for the county level, so the number of
observations is quite manageable, but the ACS tables have over 2000
fields in total. To make matters more challenging, the Census Bureau
does not use descriptive labels for these fields... they refer to them
instead with proprietary codes that are cryptic in their meaning. I had
to reference their written guide in order to determine the codes for the
*groups* of variables that I wanted. The script also generates its own
metadata file (using metadata retrieved via API) that is stored in
**census_metadata.md** in the root, which includes the Census Bureau's
metadata for all of the variables that I retrieved. It writes the data
in json format to
**data/5_year_data/2020/census_state_data\_{state_code}.json** for each
FIPS state code. Each file includes demographic information by county
for all variables in the groups: B01003 (Total Population), B02001
(Race), B03003 (Hispanic Origin), B19013 (Median Household Income),
B17001 (Poverty), B15003 (Educational Attainment), and B01001 (Age
Structure). I most certainly will not need all of these variables for my
analysis, but I have not yet completed an analysis of the data, and so
I'm not sure which variables I will want to highlight. The data is not
significantly large compared to the AQS data, so I'm not concerned about
storing all of it for now.

Two more scripts, **combine_aqs_data.py** and **combine_acs_data.py**
simply combine the state level data files in json format in
**data/annual_data/2020** and **data/5_year_data/2020** directories
respectively into combined csv files stored in
**data/combined_data/2020.** They do not perform data cleaning or
aggregation, simply concatenation.

Last (for now) **clean_aqs_data.py** and **clean_acs_data.py** load the
combined data and output cleaned versions to **data/cleaned_data/2020**.
I have taken basic data cleaning steps for both datasets, like removing
unreasonable outliers, nonsensical values, and records that are missing
too much information to be used. The Census Bureau data uses certain
negative values as sentinel values that I needed to identify and replace
with missing values. There is room for improvement in both of the
cleaning scripts still, but I think they are in a decent place at the
moment.

Other artifacts in the repository include:

**exploration.ipynb**, a Jupyter notebook file that I am using to
experiment with different methods, running code without needing to run
files from the command line before moving it to my python script files.

**codes.md** and **classes.md**, markdown files generated during my
aforementioned explanation while I was querying the AQS API to decide
which pollutants to track and which codes were used to refer to them.

**util.py,** a python file I have recently decided to use to house
functions that are reused by multiple scripts. Currently only contains
one function, but potentially more as I restructure my code to be
cleaner and more readable (and also add more code).

**Snakefile**, which defines the automated workflow that I will use for
managing reproducibility and provenance.

**.gitignore** tells git to ignore a few things that need to stay on my
local machine, like the files containing my API keys and email, the data
files, and Snakemake's local metadata.

Next steps include:

**Data Aggregation:**

I need to aggregate the records in the AQS data to calculate summary
statistics at the county level, as that is the most granular level that
it is convenient for me to integrate the datasets at. I *could* attempt
to integrate at the census tract level using the coordinate data that
the AQS provides, but this would be difficult, time consuming and
error-prone. The AQS and Census Bureau datasets both provide FIPS state
and county code fields, which are sufficient to uniquely identify
counties in the US. Speaking of integration...

**Timeline: 1 week (November 21st)**

**Data Integration:**

After I compute the aggregates from the AQS data, I will need to
integrate the datasets matching the data using the FIPS state and county
code fields. These fields will be extremely useful to uniquely identify
each county in the US. They are also simple, standardized,
programmatically added numerical codes that are not prone to entry
errors or semantic differences, and so should make record matching very
easy.

**Timeline: 1 week (November 21st)**

**Data Analysis & Visualization:**

I have to train models to see if certain demographic information I
collected is a good predictor of pollutant concentrations, and I'll
ideally visualize the data using choropleth maps.

**Timeline: 2 weeks (Early December)**

**Project Documentation:**

I've already taken strides in this direction, generating some initial
metadata files for each dataset, and providing a snakemake script that
should explain the workflow. I'll just have to keep up with this,
especially as we talk about metadata standards in class.

**Timeline: Continuous**

**Changes to my Plan:**

Scope limitations: start with one year, 2020, since the scale of the
data is cumbersome.

I have determined exactly how I am planning to integrate the data: using
the FIPS (Federal Information Processing Standard) codes included by
both datasets (an advantage to using two datasets of federal origin). I
think anticipating future topics was pretty hard to plan for in the
original plan, but I have decided that I will use snakemake to manage
workflow automation and reproducibility. Metadata standards I again have
no real concept of so I'll just have to adapt to that as it gets talked
about in class.

**Contribution Summary:**

I'm working solo on this project, so all of the work done thus far was
done by me.
