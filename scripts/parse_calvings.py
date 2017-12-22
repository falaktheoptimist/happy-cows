"""
Methods to parse herd genetics report from csv file and return a dataframe
"""
import sys
import glob
import random
from datetime import date
import pandas as pd
import helper_functions as helper

def build_date_from_row(row):
    """Build date from components"""
    year = row['calving_date_year']
    month = row['calving_date_month']
    day = row ['calving_date_day']
    out_date = date(int(year), int(month), int(day))
    return out_date

def build_calving_dates(data):
    """ Build Calving Date from components """
    data['calving_date'] = data.apply(build_date_from_row, axis=1)
    return data

def drop_features(data):
    """ Drop non-essential features. """
    data = data.reset_index()
    return data[[
        'animal_id', 'calving_date'
    ]]

def make_columns_lower(data):
    """Make all column headers lowercase"""
    data = data.reset_index()
    data.columns = [x.lower() for x in data.columns]
    return drop_features(data)

def get_dataframe_from_file(data_file):
    """ Parses calving date file and returns dataframe """
    calvings = pd.read_csv(data_file, sep=',', header=0)[
            ['calving_date_month',	'calving_date_day',	'calving_date_year', 'animal_id']
        ]
    calvings = build_calving_dates(calvings)
    calvings = drop_features(calvings)
    return make_columns_lower(calvings)

def main():
    """ Selects a random calving file, parses file, prints df.info()"""
    files = glob.glob(f"{helper.get_config()['datasets']['calvings']['regex']}")
    print(get_dataframe_from_file(random.choice(files)).info())

if __name__ == '__main__':
    sys.exit(main())
