# API Metadata Fields

**Service:** sampleData

**Total Fields:** 27

---

## 1. state_code

The FIPS code of the state in which the monitor resides.  AQS uses 2-digit or character codes that identifies one of the 50 states, U. S. territories, or Washington, DC.  For border sites, the code '80' is used for Mexico and 'CC' is used for Canada.

When submitting transactions, a user may opt to use the code 'TT' to indicate that this data is for a Native American Tribe, and that the next field on the transaction identifies a tribal area using the Bureau of Indian Affairs tribal code.

Data in the application may be viewed in Tribal format by selecting Tribal Mode in the Admin > Security menu.
## 2. county_code

A Federal Information Processing Standards (FIPS) code that identifies a county, parish, or independent city within a state.  In certain cases other geo-political entities, such as tribe via the BIA tribal code, may be used.  For border sites, it identifies the geo-political equivalent to U. S. states, such as Mexican states or Canadian provinces.

When submitting transactions, a user may opt to use a Bureau of Indian Affairs tribal code in this fied (if the State Code was entered as 'TT' to indicate that this data is for a Native American Tribe).

Data in the application may be viewed in Tribal format by selecting Tribal Mode in the Admin > Security menu.

## 3. site_number

The 4-digit number used to uniquely identify the air monitoring site within a county or tribal land.  The values are always numeric, but are treated as a string and padded with leading zeroes so they must always have 4 digits.

There is no requirement that Site Numbers be assigned continuously or in any particular order. Regional or local organizations are thus free to allocate Site Numbers in any way they choose, as long as there is no duplication within a county or tribal area.  Be aware that a tribal land using a Site Number will also reserve that Site Number for the overlapping county.  Likewise, if a county has already reserved a Site Number, it cannot be used for an overlapping Tribal land.

If a new Site Number is needed for a site that may lay in multiple jurisdictions, all agencies should cooperate to assign a Site Number to ensure that the Number is unique within the county and, for example, an ovelapping Tribal land. In other words, when a new Site Number is assigned, it must be different from any other Site Number already existing for that combination of State Code and County Code and Tribal land.

A specific Site Number is associated with a specific physical location (latitide and longitude). Any change in location requires a new Site Number to be assigned (unless a waiver is obtained from the apporpriate regional office). Although a location change would routinely mean a new Site Number, some changes that do not change the site's location in respect to surrounding sources and its measurement scale may require no change. An EPA regional office should be consulted for assistance in determining whether a new site Number is required.  AQS also has the ability to "link" sites.  This allows the time series of data (used for NAAQS and other purposes) for a parameter to be considered continuous even if the site moved and the Site Number changed.



## 4. parameter_code

The AQS code corresponding to the parameter measured by the monitor.
## 5. poc

This is the "Parameter Occurrence Code" used to distinguish different instruments that measure the same parameter at the same site.  There is no meaning to the POC (e.g. POC 1 does not indicate the primary monitor).  For example, the first monitor established to measure carbon monoxide (CO) at a site could have a POC of 1. If an additional monitor were established at the same site to measure CO, that monitor could have a POC of 2. However, if a new instrument were installed to replace the original instrument used as the first monitor, that would be the same monitor and it would still have a POC of 1.

For criteria pollutants, data from different sampling methods should only be stored under the same POC if the sampling intervals are the same and the methods are reference or equivalent. For sites where duplicate sampling is being conducted by multiple agencies or by one agency with multiple samplers, multiple POCs must be utilized to store all samples.

For non-criteria pollutants, data from multiple sampling methods can be stored under the same POC if the sampling intervals are the same and there is only one sample for the time reported. If multiple open path monitors are reporting data for the same parameter, each open path would be assigned a different POC.

While there are no national EPA practices assigning POC values, there may be regional or agency conventions where a POC value may have specific significance.  Since these do not apply universally, you will likely get the wrong set of monitors assuming the POC represents something.  There is enough metadata avaialable in AQS to correctly classify all monitors (e.g., primary, speciation, etc.)

Numbers do not need to be assigned sequentially.
## 6. latitude

The angular distance north or south of the equator measured in decimal degrees.  North is positive.

AQS converts reported coordinates (latitude and longitude) to the same datum so that sites can be more easily used for mapping and geospatial analysis.  The standard datum is WGS84 and this is the latitude in the WGS84 datum.
## 7. longitude

The angular distance east or west of the prime meridian measured in decimal degrees.  East is positive, West is negative.

AQS converts reported coordinates (latitude and longitude) to the same datum so that sites can be more easily used for mapping and geospatial analysis.  The standard datum is WGS84 and this is the longitude in the WGS84 datum.
## 8. datum

The Datum associated with the Latitude and Longitude measures.  The Datum represents the physical model of the earth used when determining latitude and longitude.

AQS computes a "standard" location representation for all site location/coordinates so that data from AQS can be more easily used for mapping and geospatial analysis. This is accomplished using a geodatabase lookup to convert the user-provided coordinates into Latitude and Longitude with the standard horizontal datum of WGS84. (i.e. This field will always be WGS84.)

If this field is blank, it means that either the user input coordinates or datum are unkown and unrecoverable.
## 9. parameter

The name or description assigned in AQS to the parameter measured by the monitor. Parameters may be pollutants or non-pollutants (e.g., wind speed).
## 10. date_local

The date the sample was taken in Local Standard Time.  This represents only the date, the time is in a separate field.  This time reflects the beginning of the sample duration.  That is, if the time is 2:00 and the duration is 1-hour, then sampling happened from 2:00 - 3:00.
## 11. time_local

The time of day that sampling began on a 24-hour clock in Local Standard Time.
## 12. date_gmt

The date the sample was taken in Greenwhich Mean Time.
## 13. time_gmt

The time of day that sampling began on a 24-hour clock in Greenwich Mean Time.
## 14. sample_measurement

The measured value in the standard units of measure for the parameter.

This value is calculated from the value reported to AQS using the following steps:

* The units are converted from the reported units or measure to the AQS standard units of measure
* The rounding and truncation rules for the parameter-method combination are applied.

For example:

## 15. units_of_measure

The unit of measure for all statistics on the same row.  Every parameter has a standard unit of measure.  Submitters are allowed to report data in any unit and EPA converts to a standard unit so that we may use the data in calculations.
## 16. sample_duration

The length of time that air passes through the monitoring device before it is analyzed (measured). So, it represents an averaging period in the atmosphere (for example, a 24-hour sample duration draws ambient air over a collection filter for 24 straight hours). For continuous monitors, it can represent an averaging time of many samples (for example, a 1-hour value may be the average of four one-minute samples collected during each quarter of the hour).

There are two types of sample durations.  First are "observed"; that is, this is the data reported to EPA as a sample measurement. 24-Hour is an observed duration and represents the average inherent in the monitoring method.

The others are "calculated" by AQS to match the form of the standard.  24-Hr-Block-Avg is a calculated duration.  This duration is needed to convert reported hourly data to the 24-hour averages needed to match the standard.
## 17. sample_frequency

The frequency at which sample observations are made.  Specified as the amount of time that elapses between the beginning of subsequent observations. Usually, this indicates how often 24-hour samples are taken, e.g., daily, every third day, stratified random, etc.  If this value is null, it implies continuous samples reported hourly.
## 18. detection_limit

The minimum sample concentration detectable for the monitor and method.  Each method has a federal MDL assigned to it by the EPA.  If the analyzing agency has determined and reported their own MDL, this will be listed rather than the federal MDL.
## 19. uncertainty

The total measurement uncertainty associated with a reported measurement as indicated by the reporting agency.  This includes method uncertainty, both the analytical and the volume uncertainty. No blank corrections are assumed (other than laboratory baseline corrections which are an integral part of each analysis).  Uncertainty should be reported in the same units of measure as the Sample Value.
## 20. qualifiers

Sample values may have qualifiers that indicate why they are missing or that they are out of the ordinary. Types of qualifiers are: null data, exceptional event, natural events, and quality assurance. All Qualifiers are described in this field.
## 21. method_type

An indication of whether the method used to collect the data is a federal reference method (FRM), equivalent to a federal reference method, an approved regional method, or none of the above (non-federal reference method).
## 22. method_code

A three-digit code representing the measurement method. A method code is only unique within a parameter (that is, method 132 for ozone is not the same as method 123 for benzene).  The encoding contains both the sample collection and sample analysis descriptions.
## 23. method

A short description of the processes, equipment, and protocols used in gathering and measuring the sample.  This field is a concatenation of the method of collection and the method of analysis.
## 24. state

The name of the state where the monitoring site is located.
## 25. county

The name of the county where the monitoring site is located.
## 26. date_of_last_change

This represents the date the most relevant underlying data in AQS was last changed.  That is, for annual summary data, it is the date these values were last affected by a change in raw data.  If the AQCR code on the annual summary view changed, the date of last change would not be updated.
## 27. cbsa_code

The code of the core based statistical area (metropolitan area) where the monitoring site is located.
