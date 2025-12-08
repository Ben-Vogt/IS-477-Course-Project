**Exploring the Relationship Between Air Quality and Various Socioeconomic Factors in the U.S.**

**Contributors**:

* Benjamin Vogt (bavogt2)

**Date of latest update:** 12/8/2025

**Summary**

The primary object of this project was to identify if there exist geographical relationships between air quality and various socioeconomic factors, such as median household income, race & ethnicity, or educational attainment. It was motivated largely by a personal interest in both environmental and cultural issues of our time, and previous courses which suggested intersectionality between them. So, I set out to see if I could identify patterns between key pollutants and some basic demographic features within regions in the US, including total population, percentage hispanic, black or african american, poverty rate, median income, and the proportion of people who had a high school diploma or more education. In order to answer these questions, I needed to decide which pollutants to track. The *criteria pollutants* are 6 air pollutants that the Clean Air Act (1963) requires the US Environmental Protection Agency (EPA) to set and enforce standards for. This identifies these pollutants as common, and important. This project examines three of them: PM2.5 particulate matter, Ozone, and Nitrogen Dioxide. This is mainly a limitation on data and scope, to keep the project focused and accurate. As a part of its Air Quality Service (AQS) the EPA collects data from sensors all over the United States, monitoring many different pollutants. This data is available publicly via an API, and this project requests sample data from them, computing my own aggregates and integrating them with the other source of data: the American Community Survey (5-year). The US Census Bureau conducts more surveys than just the Decennial Census, and this is one of them. I use this data as a source of demographic information, and it is also provided free of charge by a government API. Once the data has been retrieved, it is cleaned, combined, and integrated before the code fits a few multilinear models using the various features I mentioned to predict concentrations of PM2.5, Ozone, and Nitrogen Dioxide. It visualizes the data using choropleth maps, displaying the predicted and actual distributions of pollutants on a map using color. The result of this project was not particularly interesting: for PM2.5 and Ozone, linear relationships with demographic characteristics that I selected accounted for less than 10 percent of the variance. However, interestingly Nitrogen Dioxide stood out: 37% of the variance in the test set was explained by the demographic features alone, which indicates that there is some relationship between demographics and Nitrogen Dioxide. Nitrogen Dioxide is a more local pollutant associated with the burning of fossil fuels: vehicle emissions, power plants, and gas powered appliances and tools are all major drivers. The model we fit also includes a large positive coefficient for the proportion of people in the region who have Hispanic origin, which may indicate that people of Hispanic origin are more likely to live in proximity to regions affected by vehicle emissions, power plants, etc. The maps show considerably more accuracy for Nitrogen Dioxide, but still fairly bad (there’s a lot of unexplained variance). Overall, this project concludes that there is not a significant correlation (at the county level) between mean PM2.5 or Ozone concentrations and median income, proportion black or african american, proportion hispanic, poverty rate, proportion high school or better, and total population. The relationship between these characteristics and Nitrogen Dioxide may be more significant on a county level, though.

**Data Profile:**  
(some of this is reiterated from my original project plan)

* **Dataset 1:** EPA AQS (Air Quality System) Dataset

* **Access method:** [API Access](https://aqs.epa.gov/aqsweb/documents/data_api.html#sample)

* **Data format:** All data is provided as JSON by the API. My code later converts it to csv in the process of working on it because I like csv better.

* **Scope and variables of interest**: The dataset contains information about the concentrations of various airborne pollutants, on as granular a level as daily or even hourly readings, along with information about the geographical location of specific sensors and timestamps for each reading. We are most interested in the three key pollutants I identified: PM25, Ozone, and Nitrogen Dioxide. The scope of this dataset is quite large: millions of samples, gigabytes of data, even on a restricted timescale with just a few pollutants. The bonus of this is that the flexibility to manipulate samples in whatever ways necessary makes the full data more useful. Though, the scale of it did convince me to restrict the scope of the data to just the year 2020\. The dataset also includes import variables state\_code and county\_code. Together, these form a FIPS (Federal Information Processing Standard) code that can be used to uniquely identify a specific county in the United States. These variables are critical, and are used for integrating the AQS data with the ACS data. The particular pollutants each record measures is stored in parameter\_code and the measurement is stored in sample\_measurement. There are two more variables related to data quality: qualifier is used to mark unusual samples, and detection\_limit records the lower limit of the concentration that the sensor can accurately detect. Values that are below the detection limit are not reliable measurements.

* **Licensing and ethical considerations:** There are few ethical concerns with using this dataset: the data are not particularly personal, and don’t pertain to individuals, nor can they be used to infer any specific, personal information even about groups of people. Furthermore, the dataset (as government datasets usually are) is in the public domain, and so there are no restrictions on how I may use it for this project. That said, the EPA does have a few requests about responsible use of their API to avoid overloading their services, including recommended limits to query size and frequency, which I have adhered to in my usage of the API.

* **Dataset 2:** American Community Survey: US Census Bureau

* **Access method:** [API Access](https://www.census.gov/data/developers/data-sets/acs-3year.html)

* **Data format:** Like the other API, it returns data as JSON. But way more complicated and annoying JSON. This data is also converted to CSV once my pipeline starts to work with it.

* **Scope and variables of interest**: The dataset(s) contain information about various socioeconomic features with which I am concerned, including population, demographics, income, and education etc. on as low as a county level. This is the best geographic granularity I could achieve without a considerably more difficult task. In particular, we are interested in the groups: B01003 (Total Population), B02001 (Race), B03003 (Hispanic Origin), B19013 (Median Household Income), B17001 (Poverty), and B15003 (Educational Attainment). There are labels within each category which make the actual variable names look quite ugly: B01003 \- Estimate\!\!:Total for example is an estimate for the total population. Importantly, this dataset also includes variables state and county that have FIPS codes for each included county. These variables enable integration with AQS data. This dataset is considerably less data than the AQS data, probably because it starts off with aggregates rather than individual observations. It has many more features, though, and because of the confusing proprietary codes it can be difficult to figure out which feature has the information that is needed.

* **Licensing and ethical considerations:** Using census data poses some ethical questions, since certain census data *can* pertain to individuals. However this microdata is not data that I plan to work with, and is not contained by the particular datasets I have in mind, so violations of individual privacy are unlikely. Furthermore, this data is also in the public domain, and so there are no restrictions on how it may be used. Again, ethical API use is encouraged by the Census Bureau, and my code complies. 

The exact process for the acquisition of these datasets is contained by two appropriately named scripts in the scripts folder of my project. You will need to sign up for an API key for both the US Census Bureau and the EPA, as they use separate APIs. My key is not included, so the workflow will not function until you acquire a key, and store it in a .env file in the root.

**Data Quality:**

My analysis encountered several data quality issues that I needed to address, some of which were not able to be resolved. 

First, is a problem that I already touched on a little, but should also be included in this section: detection limits. The EPA data is collected automatically by physical sensors in the US. Which is awesome, because it means that the data was not full of typos that I needed to try and use fuzzy matching or some other text analysis technique to fix. But because they are physical sensors, they have a limit to how precisely they can measure the concentration of pollutants. If a measurement is below this limit, its exact measurement is unreliable. We just know that it’s below the limit. There are quite a few records like this, and so my code needed to handle them. I went with a simple approach that just replaces the sample\_measurement for these records with ½ the detection limit. 

Some records were missing pollutant measurements entirely. I think these records might serve some kind of administrative purpose, but for my analysis they were useless, so I discarded them entirely. There were also a small number of extreme outlier points that didn’t make physical sense, so I tried to discard those as well by removing the top 0.01% of measurements. 

The ACS data is much cleaner, which makes sense considering it isn’t raw observations. One of the most important data quality issues with BOTH datasets is completeness, though. They don’t cover all the counties in the U.S., and actually a fairly limited number of counties had both AQS and ACS data. The unincorporated territories of course have absolutely nothing as well. So completeness is a pretty big problem, but unfortunately this wasn’t an issue that I was able to resolve. So the area where the conclusions of my project apply isn’t necessarily the US as a whole, since I’m sure that the counties that are included are not distributed at random. They seem to frequently be ones with major cities. 

Because both of these datasets are far removed from manual human inputted data, they do avoid many of the quality issues associated with that.

**Findings:**

The full numeric results of the models I fit are contained in /artifacts/[results.md](http://results.md). I used 5-fold cross validated LASSO regularized multilinear regression. The models themselves are saved in the /models directory. The visualizations generated are found in /maps/2020/. They are html, so you will need to open them in a tool that can interact with that, like a browser, to view them.

A summary of the most important findings: The multilinear model to predict a county’s mean PM2.5 concentration from their total population, hispanic\_percentage, poverty\_rate, diploma\_rate, black\_or\_african\_american\_percentage, and median\_income was quite poor. It achieved an R squared of 0.0594 on the test set, explaining not even 6% of the variance. Also, the test RMSE was considerably lower than the train RMSE. This is a classic sign of underfitting, meaning that linear combinations of these features fail to capture much of the true signal.

The results for Ozone were similarly bad. The R squared value on the test data was 0.0808, indicating that just 8.08% of the variance in a county’s mean Ozone could be predicted using the demographic information that I used. This model eliminated nearly all of the coefficients, focusing on just poverty rate and black\_or\_african\_american\_percentage. But because of how poor the model is, this doesn’t really tell us that much. 

The model for Nitrogen Dioxide is strange. The RMSE is higher, relative to the typical observation, but it explains a considerable amount more of the variance: it achieves R squared of 0.3708 on the test set, indicating 37.08% of the variance in the mean Nitrogen Dioxide measurement is explained by the linear combination of the 4 variables that weren’t eliminated: total\_population, hispanic\_percentage, diploma\_rate, and black\_or\_african\_american\_percentage.

This section is short, but hopefully the full results in [results.md](http://results.md) can satisfy any further inquiry about the results. It’s just that they are mostly inconclusive, so this section is not particularly interesting.

**Future Work**

There are a lot of directions for future work. For one, I had to limit the analysis to just 3 pollutants to prevent my retrieval and storage methods from being a problem. More pollutants could be analyzed. The first ones to look should likely be the other three criteria pollutants: carbon monoxide, sulfur dioxide, and lead. Also, my analysis was limited to just the full year 2020\. I know that some pollutants do exhibit seasonal patterns, so it’s possible that using a more granular time scale or a larger time interval could improve the ability to find patterns in the data. Those are the simplest, easiest ways that I think the project could be expanded on. There are other directions, though, too. If you could find a way to make the geographical data more granular than the county level, for example by finding other sources of demographic information for the areas around particular sensors, you could do a lot less aggregation than I did. It’s totally possible, and I think even likely that the types of patterns that I was searching for are much more visible at a more granular level of geography, down to local cities and towns. Such data would probably need to come from multiple more local sources though, and it was not feasible for this project. Other directions could bring in other types of data, like climate data, since I think that also could have relationships with certain pollutants. 

Other directions still could focus on improving the accuracy of the model by using other statistical techniques. In fact, I have no doubt that a more accurate model could be constructed by using different types of models, like boosted models or neural networks. For the purposes of this project, though, I wanted a model that was particularly interpretable, and so the multilinear model was my first choice. Feature selection is another area where one could definitely improve. The Census data has hundreds of features: I just chose a few mostly arbitrarily for this project. If you really did a deep search for patterns, you could work on searching the feature space for the most relevant characteristics, which could both improve the accuracy of predictions and also help us to infer something about social and environmental justice.

The last direction for future work may not just be in improving analysis of the data, but actually finding ways to acquire more data. One of the biggest issues this project ran into was the incompleteness of the data, in the sense that many counties in the U.S. did not have enough data. Clearly, work to make more data available about air quality and demographics remains critical to answering questions like these on a broad scale like I attempted to in this project. Is it a policy issue? Are people unwilling to respond to surveys? How can we improve the completeness of datasets like these? I think those questions are just as important as the ones I tried to answer in this project, if not more.

**Reproducing**

My project is automated from end-to-end using snakemake. However, there are a few things you will need first:

(Probably Optional) Operating System:   
Edition    Windows 11 Home  
Version    24H2  
OS build    26100.7171  
Experience    Windows Feature Experience Pack 1000.26100.265.0

Anaconda: Version 24.11.3. Used for managing the virtual environment

My conda environment: I have exported the environment to a yaml file that specifies all the packages needed. Use conda env create \-f requirements.yaml to create an environment from it once you have anaconda. You will then need to activate it using conda activate 477-env. If creating the environment doesn’t work, you may be on MacOS. I think it uses Windows specific build strings in that file, so you can get it to work by removing the build strings (the stuff that comes after the version numbers). Use Windows for best results.

A US Census API key: [https://api.census.gov/data/key\_signup.html](https://api.census.gov/data/key_signup.html)

A US EPA API key: You have to sign up for this via API. Open exploration.ipynb, then replace the variable “email” in the first non-import cell with your email, and run the imports and the first cell to request a key.

Save both keys in a file .env in the root. The structure should look like this:

EMAIL \= your email here  
API\_KEY \= your epa api key here  
CENSUS\_API\_KEY \= your census api key here

Then, you should be prepared to reproduce the analysis. Ensure that you have sufficient space for all the data on your drive free: having 30 gigabytes free should be enough to be safe. It is large, which I regret, but there’s not much I could do to make it smaller when retrieving the raw data from the EPA. 

run the command snakemake \--cores all to run the automated workflow

Note: This takes a long time. Hours, on my computer. Part of why this submission is late. Verifying the automated workflow took multiple runs.

The retrieval process takes the longest. The EPA API is *painfully* slow, and I often need to retry because it rejects requests for too much data. They also want me to limit requests considerably, which I have. Please be patient with it. If it breaks off connection in the middle of requesting the data (I have done a lot of work to make sure that this doesn’t happen, but it still might), you can resume the retrieval by running the command again. It should pick up where it left off. 

Some additional miscellaneous notes about the file structure and contents:

*  All data is contained by the data folder.   
* data/5\_year\_data holds the raw ACS data  
* data/annual\_data contains the raw AQS data. data/integrated   
* data/combined\_data contains the files that combine the data from all states into one  
* data/cleaned\_data contains the results of the next step where the combined data are each cleaned  
* data/integrated\_data holds the final data file, which merges the two datasets on the state code and county code  
* All scripts are contained in the scripts folder  
* Scripts are descriptively named. If you have questions about the data flow between them, the Snakefile that defines the snakemake workflow should provide a good reference.  
* The root contains a notebook exploration.ipynb. This file serves to make the one manual request for an API key, but I also used it for generally exploring the APIs and the data before creating the scripts.  
* All additional artifacts (mainly markdown) are contained by the artifacts folder.  
* census\_metadata.md is a data dictionary for the ACS data, retrieved via the API  
* metadata.md is a data dictionary for the AQS data, also retrieved via the API  
* codes.md and classes.md are artifacts generated during exploration that provide a dictionary of EPA parameter codes. They are not updated by my scripts, but serve as a static reference if desired.  
* integration\_report\_2020.md reports information about the dataset integration, to evaluate how well the data matched, how many records had no matches, and to identify any potential issues with the integration step.  
* checksums\_2020.json is a file containing checksums for all the files I downloaded. Neither the AQS data nor the Census data provides checksums for downloads, so I computed my own on the version of the data that I downloaded, and my scripts use these to verify the integrity of the files that they download. They are not dynamically saved, although the code I used to compute them is available in scripts/compute\_checksums.py.   
* project\_plan.md and StatusReport.md are two previous readme’s written at earlier stages in the project. They are included for completeness.  
* The maps directory contains choropleth visualizations generated by the analysis. Each is descriptively named.  
* The models directory saves the trained models in .pkl format  
* Snakefile describes the automated end-to-end workflow for the project. 

**Citations**:

U.S. Environmental Protection Agency. (2020). Air Quality System (AQS) data \[Dataset\]. Retrieved from [https://aqs.epa.gov/aqsweb/documents/data\_api.html](https://aqs.epa.gov/aqsweb/documents/data_api.html)  
U.S. Census Bureau. (2020). American Community Survey 5-year estimates \[Dataset\]. Retrieved from [https://www.census.gov/data/developers/data-sets/acs-5year.html](https://www.census.gov/data/developers/data-sets/acs-5year.html)

*Anaconda Software Distribution*. (2020). *Anaconda Documentation*. Anaconda Inc. Retrieved from [https://docs.anaconda.com/](https://docs.anaconda.com/)

Pedregosa, F., Varoquaux, Ga"el, Gramfort, A., Michel, V., Thirion, B., Grisel, O., … others. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, *12*(Oct), 2825–2830. (scikit-learn)

McKinney, W., & others. (2010). Data structures for statistical computing in python. In *Proceedings of the 9th Python in Science Conference* (Vol. 445, pp. 51–56). (pandas)

Inc., P. T. (2015). Collaborative data science. Montreal, QC: Plotly Technologies Inc. Retrieved from [https://plot.ly](https://plot.ly) (plotly)

(Many contributors) Joblib. https://github.com/joblib/joblib.git  
(the developers do not have a recommended citation)

Chandra, R. V., & Varanasi, B. S. (2015). *Python requests essentials*. Packt Publishing Ltd. (requests)

Van Rossum, G., & Drake Jr, F. L. (1995). *Python reference manual*. Centrum voor Wiskunde en Informatica Amsterdam. (Python programming language)

Mölder F, Jablonski KP, Letcher B *et al.* Sustainable data analysis with Snakemake \[version 3; peer review: 2 approved\]. *F1000Research* 2025, **10**:33 ([https://doi.org/10.12688/f1000research.29032.3](https://doi.org/10.12688/f1000research.29032.3))  (snakemake)

This project relies on various other packages available under open source licenses. The citations above include the major packages and software whose functionality I needed, and the rest are dependencies of those packages. environment.yaml contains a full list of the packages used, including versions.

