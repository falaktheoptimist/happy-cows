# Data Wrangling

This document is intended to outline the data gathering and cleansing processes utilized in this project.  Specific questions to answer include:

- What kind of cleaning steps were performed?
- How did you deal with missing values, if any?
- Were there outliers, and how did you decide to handle them?

## Data set: Weather

### Acquisition

The data set consists of daily summaries of weather measurements for Franklin County, Pennsylvania such as low temperature, high temperature, and total precipitation.  The CSV files were requested from the [NOAA Online Climate Data Online Search](https://www.ncdc.noaa.gov/cdo-web/search) for full calendar year 2014, 2015, and 2016, and then again for all available data in 2017.  The resulting CSV files were uploaded to AWS S3 to be programmatically retrieved by the script [get_data.py](/scripts/get_data.py).

### Cleaning

In order to clean the weather data, the full files are processed by the script [parse_weather.py](/scripts/parse_weather.py).  Initially, the resulting DataFrame was limited to a smaller set of variables including the station identifier, name of station, latitude, longitude, elevation, date, volume of precipitation, maximum temperature and minimum temperature.  The resulting DataFrame was reindexed to a unique combination of station identifer and date (parsed to a date time object from a string), as row represents daily summary from a single station.  Null values were permitted in the precipitation, minimum temperature, and maximum temperature columns and interpreted as measurements not taken by a specific station.  Assumed ranges were applied to the precipitation (assumed to between 0 and 20 inches if not null) and temperature columns (assumed to be between -20 and 120 degrees if not null).  After asserting numerical ranges, the remaining columns were checked for the expected data types.  The resulting DataFrame was stored in a local database through the [load_data.py](/scripts/load_data.py)

### Data set: Milk Production

ToDo

## Data set: Animal Classification

ToDo