"""
Methods to parse weather data from csv files and return a dataframe
"""
import sys
import glob
import random
import pandas as pd
import helper_functions as helper
from datetime import datetime

def get_dataframe_from_file(data_file):
    weather = pd.read_csv(data_file,sep=',', header=0)[[
        'STATION', 'NAME', 'LATITUDE', 'LONGITUDE', 'ELEVATION', 'DATE', 'PRCP', 'TMIN', 'TMAX'
    ]]
    weather['DATE'] = weather['DATE'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
    weather.index = weather['DATE']
    return weather

def main():
    """ Selects a random weather file, parses file, prints df.info()"""
    files = glob.glob(f"{helper.get_config()['datasets']['weather']['regex']}")
    print(get_dataframe_from_file(random.choice(files)).info())

if __name__ == '__main__':
    sys.exit(main())
