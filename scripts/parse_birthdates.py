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
    year = row['birthdate_year']
    month = row['birthdate_month']
    day = row['birthdate_day']
    out_date = date(int(year), int(month), int(day))
    return out_date

def build_birth_dates(data):
    """ Build birth Date from components """
    data['birthdate'] = data.apply(build_date_from_row, axis=1)
    return data

def drop_features(data):
    """ Drop non-essential features. """
    data = data.reset_index()
    return data[[
        'animal_id', 'birthdate'
    ]]

def make_columns_lower(data):
    """Make all column headers lowercase"""
    data = data.reset_index()
    data.columns = [x.lower() for x in data.columns]
    return drop_features(data)

def get_dataframe_from_file(data_file):
    """ Parses birth date file and returns dataframe """
    births = pd.read_csv(data_file, sep=',', header=0)[
            ['birthdate_year',	'birthdate_month',	'birthdate_day', 'animal_id']
        ]
    births = build_birth_dates(births)
    return make_columns_lower(births)

def main():
    """ Selects a random birth file, parses file, prints df.info()"""
    files = glob.glob(f"{helper.get_config()['datasets']['birthdates']['regex']}")
    print(get_dataframe_from_file(random.choice(files)).info())

if __name__ == '__main__':
    sys.exit(main())
