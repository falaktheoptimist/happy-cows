# Data in Dairy: An Exploration Of Milk Production

## Background

Dairy producers of all sizes are under an ever-present economic pressure to produce more with less to meet the global demand for dairy products.  As a result, farmers need to carefully monitor the environments of their cattle to prevent injury, encourage production, and stop the spread of disease.  As a result, careful examination of input factors such as genetics, nutrition, climate, facilities, and negative health-events may provide actionable insights into ways to modify operations and improve the health, well-being, and production of a given herd.  This repository is an exploration of data from a single herd of dairy cows located in Franklin County, Pennsylvania.

## Client(s)

Dairy producers would receive direct benefit from a detailed analysis of their current operations.  The benefits could include increased milk production or reduced frequencies of costly adverse health events such as infection or injury.  Farmers, armed with a data-driven analysis, would be better able to weigh the projected value of operational changes to their facilities over time.  Some areas of modification may include:

- Nutrition
- Milking Frequency
- Milking Facilities
- Breeding/Pedigree Strategies
- Facility and Climate Considerations
- Herd Density
- Bedding
- Other Technology Investment

The specific objective of this analysis is to evaluate the impact of externally observable, measured factors to impact three primary data points: Milk Pounds, Butterfat, and Somatic Cell Count (SCC).

## Data

Current sources of data include:

### Milk Production Measurements

- **Description:** Measurements of milk production by animal.
- **Source:** Daily system logs from local installation of DeLaval - ALPRO™ herd management system
- **Acquisition:** Offline retrieval and parsing of records from June, 3 2015 to November 7, 2017

### Milk Quality Measurements

- **Description:** Monthly, Supervised milk tests conducted by a certified representative of [National Dairy Herd Information Association (DHIA)](http://www.dhia.org/).
- **Source:** Monthly, Hard copy DHI-300 Report conducted by DHIA captured by with the 02-DHI-APCS protocol
- **Acquisition:** Scanning and extraction of data from PDF of DHI-300 reports between December 2014 and October 2017

### Physical Attributes of Cows - Animal Classification

- **Description:** Periodic assessment of the physical attributes of a given animal.  Animals are classified on a scale from 1-100 based on a number of measured characteristics.  Used as a numeric model to compare an animal against the 'ideal' milking cow.
- **Source:** Periodic, hard-copy [Linear Classification Reports](http://www.holsteinusa.com/programs_services/classification.html) conducted by representative of [Holstein Association USA](http://www.holsteinusa.com/) between August 8, 2014 and July 10, 2017.
- **Acquisition:** Scanning and programmatic extraction of data from paper reports.

### Biographic Information

- **Description:** Basic biographic information including animal ID, animal age, days in milk, and days since calving.
- **Source:** CSV Report from DeLaval - ALPRO™ herd management system
- **Acquisition:** One-time retrieval of report from system.

### Regional Climate

- **Description:** Daily weather summaries for Franklin County, Pennsylvania. Data extends from January 1, 2014 to November 3, 2017.
- **Source:** [NOAA Online Climate Data Online Search](https://www.ncdc.noaa.gov/cdo-web/search)
- **Acquisition:** CSV Export of Daily Summary reports from all locations in Franklin County, PA.

### Approach

Analysis of these data sets will require a number of steps.  The current approach is as follows.

- Analysis of categorical information including genetic and biographical data to identify logical animal groups.
- Time series analysis of production and weather data against identified animal groups to evaluate the impact of weather-related factors.

### Deliverables

A short report outlining process methods, data retrieval, supporting code and identified models.  The primary output is the identification of actionable insights to increase Milk pounds, increase Butterfat, or to reduce Somatic Cell Count.