# Data in Dairy: An Exploration Of Milk Production

## Background

Dairy producers of all sizes are under an ever-present economic pressure to produce more with less to meet the global demand for dairy products.  As a result, farmers need to carefully monitor the environments of their cattle to prevent injury, encourage production, and stop the spread of disease.  As a result, careful examination of input factors such as genetics, nutrition, climate, facilities, and negative health-events may provide actionable insights into ways to modify operations and improve the health, well-being, and production of a given herd.

### The Problem

To make thoughtful, long-term business decisions farmers need to be confident in the future milk production of their herd.  The total weight of milk produced is a primary component of how farmers receive compensation.  If a farmer fails to produce sufficient milk weights, it can lead to financial loss even a ceasing of operations. The ultimate objective of this analysis is to provide an estimate of future milk production for each animal in a given herd.

### Client(s)

The primary client(s) for this project are individual Dairy Producers.  Farms of all sizes would benefit from a detailed analysis and estimation of future milk production.  Often large farms rely heavily upon herd management software that provides a comprehensive, data-driven perspective on operations.  To make the most out of the power of these tools, it often requires capital investment in devices and sensors, additional man-hours for data entry, or other expense for outside expertise.  These barriers usually leave small and mid-size farms making decisions without the power of software, relying upon intuition and analog data sources.

This analysis seeks to generate a tool capable of deriving insights from these paper data sources and bring value to small and medium-sized operations.  Armed with a data-driven analysis, small and medium-sized farms would be better able to weigh the projected value of operational changes to their facilities over time.  Some areas of modification may include:

- Nutrition
- Milking Frequency
- Milking Facilities
- Breeding/Pedigree Strategies
- Facility and Climate Considerations
- Herd Density
- Bedding Practices
- Other Technology Investment

### Selected Terms

#### Milk Weight

The amount of milk produced by an animal. Measured in pounds of milk. For reference, a gallon of milk weighs approximately 8.6 pounds.

#### Dry Period

The period when a cow is not producing milk. Often serves as a time of rest following a lactation period.

#### Lactation Period

The period when a cow is producing milk.

#### Days in Milk

The number of consecutive days a given cow has been actively producing milk.

#### Linear Classification Score

An integer score between 50-99 given to a milk cow, providing a numerical representation of how well a the physical attributes of an animal fits the profile of an 'ideal' milking cow. A weighted summarization of 18+ assessments of a given animal.

## Current Dataset(s)

### Milk Volume Measurements | Milk Weight

#### Description

The milk weight dataset provides unique records of individual milking events from a given cow.  On this farm, cows may be milked up to twice daily.  The results of these milking sessions are captured daily system logs in a series of text files from the local storage of the dairy farm's DeLaval - ALPRO™ herd management system [[Example File]](/references/example_files/milk_volume_example.txt). The following lines provide an example of relevant data elements:

``` txt
04:27:56    R    200    Cow    Duration1    3:47
04:27:56    R    200    Cow    AverFlow1    3.8
04:27:56    R    200    Cow    PeakFlow1    5.0
04:27:56    R    200    Cow    MilkToday1    14.8
```

The lines above suggest that Cow #200 produced 14.8 pounds of milk, in three minutes and forty-seven seconds with an average flow rate of 3.8 lb/min and a peak flow of 5.0 lb/min.  Also, this milking occurred at 4:27:56 am.

#### Raw Data Acquisition

The system logs were manually retrieved from the herd management system and uploaded to a private AWS S3 bucket for on-demand, repeatable retrieval via [script](/scripts/get_data.py)

#### Data Wrangling

The contents of each log file were parsed into pandas.DataFrame.  Regex expressions were used to select only the records matching the pattern of desired data elements. For additional detail on the parsing of these log files please see the script [parse_milk_volume.py](/scripts/parse_milk_volume.py).  The processed data was are stored in a local database via the script [load_database.py](/scripts/load_database.py).

### Physical Attributes of Cows | Linear Classification Score

#### Description

Linear Classification Scores provide a periodic assessment of the physical attributes of a given animal.  Animals are classified on a scale from 50-99 based on some measured characteristics for comparison against the 'ideal' milking cow.  These [Linear Classification Reports](http://www.holsteinusa.com/programs_services/classification.html)  were conducted by a representative of [Holstein Association USA](http://www.holsteinusa.com/) between August 8, 2014, and July 10, 2017.

``` txt
8/5/14,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
BARN_ID,AGE,LAC,DATE_CALVED,ST,SR,BD,DF,RA,RW,LS,RL,LO,FA,FU,UH,UW,UC,UD,TP,RT,TL,UT,CS,FC,DS,RP,FL,MS,FS,E,%BAA
1485,7-Jul,6,7/10/14,50,45,44,42,25,35,29,25,25,25,14,26,35,50,5,35,35,35,35,25,92,92,92,82,80,85,,106
1542,9-Jun,4,8/6/13,50,35,35,42,15,35,50,25,,25,35,36,35,35,40,25,25,25,26,17,93,93,90,84,93,91,2,113.5
```

The example above shows the scoring for cows number 1485 and 1542.  The animals received a final linear score of 85 and 91 respectively.  The assessment occurred on August 5, 2014.

#### Raw Data Acquisition

They were retrieved in the form of paper reports. The contents of the reports were scanned to PDF and parsed into [csv files](/references/example_files/classification_example.csv) using the program [PDF Element by Wondershare](https://pdf.wondershare.com/).  The resulting CSVs were uploaded to a private AWS S3 bucket for on-demand, repeatable retrieval via [script](/scripts/get_data.py)

#### Data Wrangling

The raw data files were processed by the following script, [parse_classification.py](/scripts/parse_classification.py).  This script ensured the numerical nature of the scores, which are eventually stored in a local database by [load_database.py](/scripts/load_database.py).

### Regional Climate | NOAA Daily Weather Summaries

#### Description

The weather data set consists of daily summaries of weather measurements for Franklin County, Pennsylvania such as low temperature, high temperature, and total precipitation [[Example File]](/references/example_files/weather_example.csv).

#### Raw Data Acquisition

The CSV files were requested from the [NOAA Online Climate Data Online Search](https://www.ncdc.noaa.gov/cdo-web/search) for full calendar year 2014, 2015, and 2016, and then again for all available data in 2017.  The resulting CSV files were uploaded to AWS S3 to be programmatically retrieved by the script [get_data.py](/scripts/get_data.py).

#### Data Wrangling

The raw files are processed by in the script [parse_weather.py](/scripts/parse_weather.py).  Initially, the resulting DataFrame was limited to a smaller set of variables including the station identifier, name of station, latitude, longitude, elevation, date, the volume of precipitation, maximum temperature and minimum temperature.  Null values were permitted in the precipitation, minimum temperature, and maximum temperature columns and interpreted as measurements not taken by a specific station.  Assumed ranges were applied to the precipitation (assumed to between 0 and 20 inches if not null) and temperature columns (assumed to be between -20 and 120 degrees if not null).  After asserting numerical ranges, the remaining columns were checked for the expected data types.  The resulting DataFrame was stored in a local database through the following [script.](/scripts/load_database.py)

## Other Potential Dataset(s)

### Milk Quality Measurements | Somatic Cell Count, Butterfat Percentage

On a recurring monthly basis, detailed milk tests are taken by a certified representative of [National Dairy Herd Information Association (DHIA)](http://www.dhia.org/).  These tests provide a monthly snapshot of additional attributes that help determine the compensation to a farmer (butterfat content), and the health of an animal (Somatic Cell Count).  These reports are available in paper copy between December 2014 and November 2017.

### Reproductive Health | Insemination Date, Lactation Count, Calving Date, Days in Milk

Additional information regarding the reproductive health and gestation cycle of a given animal are available in paper records.  These factors may prove useful in further estimating the health and production volume of a given animal.

## Initial Findings

A [preliminary analysis](/notebooks/statistics_of_milk_production.ipynb) of the currently available data revealed a number of insights:

- The herd experienced a measurable per-capita head increase in milk weights during the spring months.
- A statistically-significant, positive linear correlation exists between an Animal's linear classification score and the amount of milk produced.  Specifically, animals with higher scores tended to produce more milk.
- A statistically-significant, linear relationship between maximum temperature and milk production was not found.

## Notes for further exploration

- Though a linear relationship was not found, a higher order polynomial relationships between weather and milk production may yield a better fit.
- Additional data such as days in milk may provide further perspective into the seemingly cyclical nature of milk volumes.
- Upon the completion of the calendar year 2017, gather milk production and weather data
- Utilizing the component scores such as udder and teat health that build up to a Linear Classification Score may prove more powerful predictors of overall milk production.
