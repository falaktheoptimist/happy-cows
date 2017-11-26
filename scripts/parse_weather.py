"""
Methods to parse weather data from csv files and return a dataframe
"""
import sys
import glob
import random
from datetime import datetime
import pandas as pd
import pandas.api.types as ptypes
import helper_functions as helper

def format_date(df):
    """Converts weather['Date'] to datetime"""
    return df['DATE'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

def get_dataframe_from_file(data_file):
    """ Parses NOAA daily weather summary CSVs. Returns DataFrame """
    weather = pd.read_csv(data_file, sep=',', header=0)[[
        'STATION', 'NAME', 'LATITUDE', 'LONGITUDE', 'ELEVATION', 'DATE', 'PRCP', 'TMIN', 'TMAX'
    ]]
    weather = format_date(weather)
    weather.set_index(['DATE', 'STATION'])
    
    assert weather[weather['TMAX'].notnull()]['TMAX'].between(-20, 120).all()
    assert weather[weather['TMIN'].notnull()]['TMIN'].between(-20, 120).all()
    assert weather[weather['PRCP'].notnull()]['PRCP'].between(0, 20).all()
    assert ptypes.is_string_dtype(weather['STATION'])
    assert ptypes.is_string_dtype(weather['NAME'])
    assert ptypes.is_datetime64_any_dtype(weather['DATE'])
    assert ptypes.is_numeric_dtype(weather['LATITUDE'])
    assert ptypes.is_numeric_dtype(weather['LONGITUDE'])
    assert ptypes.is_numeric_dtype(weather['ELEVATION'])
    assert ptypes.is_numeric_dtype(weather['PRCP'])
    assert ptypes.is_numeric_dtype(weather['TMIN'])
    assert ptypes.is_numeric_dtype(weather['TMAX'])

    return weather

def main():
    """ Selects a random weather file, parses file, prints df.info()"""
    files = glob.glob(f"{helper.get_config()['datasets']['weather']['regex']}")
    print(get_dataframe_from_file(random.choice(files)).info())

if __name__ == '__main__':
    sys.exit(main())
