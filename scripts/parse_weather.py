"""
Methods to parse weather data from csv files and return a dataframe
"""
import sys
import glob
import random
import pandas as pd
import helper_functions as helper

def transform_tmax(data):
    """fill values for TMAX"""
    data[['TMAX']] = data.groupby('DATE')[['TMAX']].transform(lambda x: x.fillna(x.mean()))
    return data

def transform_tmin(data):
    """fill values for TMIN"""
    data[['TMIN']] = data.groupby('DATE')[['TMIN']].transform(lambda x: x.fillna(x.mean()))
    return data

def transform_precipitation(data):
    """fill values for PRCP"""
    data[['PRCP']] = data.groupby('DATE')[['PRCP']].transform(lambda x: x.fillna(x.mean()))
    return data

def transform_date(data):
    """ Ensure DATE is a datetime """
    data['DATE'] = pd.to_datetime(data['DATE'])
    data = data.groupby('DATE').mean().reset_index()
    return data.set_index(['DATE'])

def identify_heatwave(data):
    """Identify a day as hot if TMAX > 90.  Identify as heatwave if three consecutive hot days"""
    data['IS_HOT'] = data['TMAX'].apply(lambda x: x > 90)
    data['IS_HEATWAVE'] = data['IS_HOT'].rolling(3).sum() == 3
    return data

def identify_coldwave(data):
    """Identify a day as cold if TMIN < 10.  Identify as coldwave if three consecutive cold days"""
    data['IS_COLD'] = data['TMIN'].apply(lambda x: x < 10)
    data['IS_COLDWAVE'] = data['IS_COLD'].rolling(3).sum() == 3
    return data

def transform_features(data):
    data = transform_tmax(data)
    data = transform_tmin(data)
    data = transform_precipitation(data)
    data = transform_date(data)
    data = identify_heatwave(data)
    data = identify_coldwave(data)
    return data

def drop_features(data):
    """ Drop non-essential weather features. """
    data = data.reset_index()
    return data[[
        'DATE', 'PRCP', 'TMIN', 'TMAX', 'IS_HOT', 'IS_HEATWAVE', 'IS_COLD', 'IS_COLDWAVE'
    ]].set_index('DATE')

def make_columns_lower(data):
    """Make all column headers lowercase"""
    data = data.reset_index()
    data.columns = [x.lower() for x in data.columns]
    return data

def get_dataframe_from_file(data_file):
    """ Parses NOAA daily weather summary CSVs. Returns DataFrame """
    weather = pd.read_csv(data_file, sep=',', header=0)[[
        'STATION', 'NAME', 'LATITUDE', 'LONGITUDE', 'ELEVATION', 'DATE', 'PRCP', 'TMIN', 'TMAX'
    ]]

    weather = transform_features(weather)
    weather = drop_features(weather)
    return make_columns_lower(weather)

def main():
    """ Selects a random weather file, parses file, prints df.info()"""
    files = glob.glob(f"{helper.get_config()['datasets']['weather']['regex']}")
    print(get_dataframe_from_file(random.choice(files)).info())

if __name__ == '__main__':
    sys.exit(main())
