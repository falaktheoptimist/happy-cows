# Data Wrangling

This document is intended to outline the data gathering and cleansing processes utilized in this project.

## Dataset: Weather

The weather data set consists of daily summaries of weather measurements for Franklin County, Pennsylvania such as low temperature, high temperature, and total precipitation [[Example File]](/references/example_files/weather_example.csv).  The CSV files were requested from the [NOAA Online Climate Data Online Search](https://www.ncdc.noaa.gov/cdo-web/search) for full calendar year 2014, 2015, and 2016, and then again for all available data in 2017.  The resulting CSV files were uploaded to AWS S3 to be programmatically retrieved by the script [get_data.py](/scripts/get_data.py).

The raw files are processed by in the script [parse_weather.py](/scripts/parse_weather.py).  Initially, the resulting DataFrame was limited to a smaller set of variables including the station identifier, name of station, latitude, longitude, elevation, date, the volume of precipitation, maximum temperature and minimum temperature.  The resulting DataFrame was reindexed to a unique combination of station identifier and date (parsed to a date time object from a string), a row represents daily summary from a single station.  Null values were permitted in the precipitation, minimum temperature, and maximum temperature columns and interpreted as measurements not taken by a specific station.  Assumed ranges were applied to the precipitation (assumed to between 0 and 20 inches if not null) and temperature columns (assumed to be between -20 and 120 degrees if not null).  After asserting numerical ranges, the remaining columns were checked for the expected data types.  The resulting DataFrame was stored in a local database through the following [script.](/scripts/load_database.py)

## Dataset: Milk Production

The milk volume data set consists of daily system logs in a series of text files from the local storage of the dairy farm's DeLaval - ALPRO™ herd management system [[Example File]](/references/example_files/milk_volume_example.txt).  These system logs consist of individual lines, each with a time stamp, and associated records.  Raw files were retrieved via [script](/scripts/get_data.py) and individually parsed order to extract relevant data.  The contents of each log file were parsed into a single column DataFrame where each row consisted of the contents of each line.  The resulting DataFrame rows further screened to include lines such as the following:

``` txt
04:27:56    R    200    Cow    Duration1    3:47
04:27:56    R    200    Cow    AverFlow1    3.8
04:27:56    R    200    Cow    PeakFlow1    5.0
04:27:56    R    200    Cow    MilkToday1    14.8
```

The lines above suggest that Cow #200 produced 14.8 pounds of milk, in three minutes and forty-seven seconds with an average flow rate of 3.8 lb/min and a peak flow of 5.0 lb/min.  Also, this record was captured at 4:27:56 am.  Additional manipulations and assertions were applied in the [parse_milk_volume.py](/scripts/parse_milk_volume.py) to produce a DataFrame with a row for each milk volume record.  Null values, indicating that the animal did not produce milk on that occasion were dropped. The resulting DataFrame was stored in a local database in the following [script.](/scripts/load_database.py)

## Dataset: Animal Classification

The animal classification dataset consists of records providing a numeric representation of the physical attributes of a given animal.  The [[Example File]](/references/example_files/classification_example.csv) consists of an expected array of integer, float, string and date values.  These data types were checked in the script [parse_classification.py][/scripts/parse_classification.py]. After enforcing the expected data types on the DataFrame, a new value categorical value was created to align with the categories used by [Holstein Association USA](http://www.holsteinusa.com/programs_services/classification.html).  The categorical values for final score brackets are 'Excellent' (90-100), 'Very Good' (85-89), 'Good Plus' (80-84), 'Good' (75-79), 'Fair' (65-74), and 'Poor' (1-64). After adding the categorical values, the incomplete rows containing null values were dropped representing space in the file.  The resulting DataFrames were stored in a local database using the following [script](/scripts/load_database.py).
