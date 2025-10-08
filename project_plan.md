# **IS 477 Project Plan**

## **Exploring the Relationship Between Air Quality and Various Socioeconomic Factors in the U.S.**

## **Overview**

The goal of this project is to examine how certain socioeconomic
features, such as income and demographics, are related (geographically)
to air quality in the U.S. The project will work with data that are
situated in specific times and places, in order to analyze trends over
time and in various regions of the U.S. It aims to synthesize multiple
data sources in order to arrive at solid statistical conclusions that
support or refute claims about environmental justice and the
intersectionality of social and environmental ethics issues.

## **Research Questions**

- How does air quality vary with (median) household income across U.S.
  metropolitan areas?

- Are there patterns in pollution exposure that are associated with
  demographic composition?

- Is pollutant exposure associated geographically with educational
  attainment or employment rates?

## **Team**

I am working alone, and so I will be responsible for all of the involved
tasks, such as data collection and API use, database setup, data
cleaning, data analysis, generating visualizations, and drafting both
the final and intermediate reports.

## **Datasets**

Identify and describe the datasets you will use. You must include at
least two different datasets that will be integrated later. For each
dataset, note:

- **Name of dataset (1):** EPA AQS (Air Quality System) Dataset**\**

- **Access method:** [[API
  Access]{.underline}](https://aqs.epa.gov/aqsweb/documents/data_api.html#sample)

- **Data format:** All data is provided as JSON by the API, but it will
  be useful to use it in a database to enable queries and integration

- **Scope and variables of interest**: The dataset contains information
  about the concentrations of various airborne pollutants, on as
  granular a level as daily readings, along with information about the
  geographical location of specific sensors and timestamps for each
  reading. You can also query less granular data, but I think working
  with the lowest level records will be the most interesting and
  engaging way to approach this project.**\**

- **Licensing and ethical considerations:** There are few ethical
  concerns with using this dataset: the data are not particularly
  personal, and don't pertain to individuals, nor can they be used to
  infer any specific, personal information even about groups of people.
  Furthermore, the dataset (as government datasets usually are) is in
  the public domain, and so there are no restrictions on how I may use
  it for this project. That said, the EPA does seem to have a few
  requests about responsible use of their API to avoid overloading their
  services, including recommended limits to query size and frequency,
  which shouldn't be too much of an issue.

- **Planned integration:** Because the data are labeled with both time
  and geographical location, it should be possible to integrate this
  data with any other records that have similar fields, for example
  census data. This allows the data to reveal relationships between
  pollutants and any other features that we have temporally and
  geographically situated data for.

- **Name of dataset(2):** American Community Survey: US Census
  Bureau**\**

- **Access method:** [[API
  Access]{.underline}](https://www.census.gov/data/developers/data-sets/acs-3year.html)
  (although the census website seems to be a bit janky due to the
  current government shutdown: apparently the API is still accessible
  though, and hopefully the shutdown will end soon. There are also
  probably other hosts that have this data, if necessary, although none
  can be as reliable as straight from the source). It also looks like
  they provide [[file download]{.underline}](https://www2.census.gov/)s
  for the data.

- **Data format:** It seems that the census datasets are formatted as
  CSV, although again I will likely use a relational database for
  modeling and organizing the data.

- **Scope and variables of interest**: The dataset(s) contain
  information about various socioeconomic features with which I am
  concerned, including demographics, income, education, employment, etc.
  on as low as a county level. This gives me decent geographic
  granularity.**\**

- **Licensing and ethical considerations:** Using census data poses some
  ethical questions, since certain census data *can* pertain to
  individuals. However this microdata is not data that I plan to work
  with, and is not contained by the particular datasets I have in mind,
  so violations of individual privacy are unlikely. Furthermore, this
  data is also in the public domain, and so there are no restrictions on
  how it may be used. However, again access to the API requires a free
  account and should be used responsibly.

- **Planned integration:** Because I have approximate dates and
  geographical locations to which the data are relevant, I can combine
  them with the records from the EPA's sensors to look for patterns in
  how various socioeconomic features tracked by Census Bureau data are
  related to concentrations of air pollutants.

## **Timeline**

The exact plan may depend on any barriers I run into, but basically:

Week 1: I can jump right into data acquisition, researching how to use
the API's to query the massive amount of data the government has.

Week 2: Import relevant parts of the data into a database schema so that
I can use SQL queries to manipulate the data.

Week 3: Data cleaning, handling missing values, redundant/duplicate
records, etc. All of this work will need to be written as reusable
scripts so that I can construct a pipeline for the way that I processed
the data, for future reproducibility.

Week 4: Begin work on data integration. I anticipate this to be a
challenging part of the project, since the level of granularity for time
and location is different between the datasets, and furthermore
sometimes geographic boundaries can change over time, so there may be
many ambiguities to resolve.

Week 5: Finalize data integration. By the end of this week I would like
to be able to relate the datasets completely, aggregate air quality
records, etc.

Week 6: Begin Data Analysis. Explore various relationships and see what
patterns can be gleaned from the synthesis of the datasets.\
\
Week 7: Decide on and generate important visuals from the analysis
steps.\
\
Week 8: Clean up project documentation, put together scripts for
acquisition, cleaning, integration, analysis, and visualization to
create the final automated workflow that allows all of the steps for my
project to be reproduced. Data dictionary, etc.

Week 9: Prepare final report + flex time in case something goes wrong
and I need to switch something up.

(note that Week 1 refers to the week immediately following the
submission of this project report, beginning 10/8 and ending 10/14. That
leaves 9 weeks in total before the final deadline on 12/10).

## **Constraints** 

- The data are government data, and unfortunately right when I started
  thinking about this plan, Congress shut down the government by being
  utterly ineffective. So there *could* be issues with accessing the
  data from their original source using the official APIs provided by
  the Census Bureau and the EPA.

- The datasets, especially the very granular EPA dataset I mentioned,
  could be inconveniently large. I do have access to plenty of
  computational resources to handle this, but it should be noted that
  the scale of the data could be tricky.

- Census data is famously exclusionary, and in using it I am limited by
  the Census Bureau's choices on what categories to put people in.

## **Gaps**

- Integrating more granular location data with only higher level (county
  level) location identifiers could prove difficult - I'm not 100% sure
  yet how I'm going to do that.

- I'm not really sure what I'm going to *do* with the data after I
  complete my analysis: most data lifecycles include steps for
  archiving+maintenance or destruction of the data after analysis and
  visualizations are complete, but I'm not sure how that step can really
  be applied to my project.
