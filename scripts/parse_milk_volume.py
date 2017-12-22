"""
Methods to parse milk volume data from raw log files and return a dataframe
"""
import sys
import glob
import random
from datetime import datetime
import re as re
import numpy as np
import pandas as pd
import helper_functions as helper

def extract_columns_from_fullline(data):
    """ Transform data['full_line'] into dataframe with multiple columns """
    # Lines are expected to begin with \n character
    assert data['full_line'].str.startswith("\n").all()
    data['full_line'] = data['full_line'].str.replace("\n", "")
    assert not data['full_line'].str.startswith("\n").any()

    # Split full_line into multiple columns
    assert len(data.columns) == 1
    data = pd.DataFrame(data['full_line'].str.split('\t').tolist(), index=None)
    assert len(data.columns) == 6
    data.columns = ['date', 'record_type', 'animal_id', 'animal_type', 'measurement', 'value']
    return data

def validate_and_drop_record_type(data):
    """ data.record_type is assumed to be homogeneous value of 'R' """
    assert data['record_type'].values.all() == 'R'
    data = data.drop(['record_type'], axis=1)
    assert 'record_type' not in data.columns
    return data

def validate_and_drop_animal_type(data):
    """ data.animal_type assumed not null, and homogenous value of 'Cow'"""
    assert data['animal_type'].str.contains('^Cow$').all()
    data = data.drop(['animal_type'], axis=1)
    assert 'animal_type' not in data.columns
    return data

def transform_date(data, milking_date):
    """data.date is assumed to be in HH:MM:SS format.
       Confirm, transform and combine with milk_date"""
    assert data['date'].str.contains(r'\d{2}:\d{2}:\d{2}').all()
    data['date'] = data['date'].apply(lambda x: datetime.strptime(x, '%H:%M:%S'))
    data['date'] = data['date'].apply(lambda x: datetime.combine(milking_date, x.time()))
    assert not data['date'].isnull().values.any()
    return data

def transform_animal_id(data):
    """ data.animal_id is assumed to be an integer value """
    assert data['animal_id'].str.contains(r'^\d+$').all()
    data['animal_id'] = data['animal_id'].apply(lambda id_string: int(id_string))
    assert not data['animal_id'].isnull().values.any()
    return data

def extract_milk_weight(row):
    """ Extracts milk_weight values"""
    if row['measurement'] in ['MilkToday1', 'MilkToday2']:
        # Weight Values from log files are in kg, converting to pounds
        return round(float(row['value']) * 2.2046, 1)
    return np.nan

def extract_average_flow(row):
    """ Extracts average_flow values """
    if row['measurement'] in ['AverFlow1', 'AverFlow2']:
        return float(row['value'])
    return np.nan

def extract_max_flow(row):
    """ Extracts max_flow values """
    if row['measurement'] in ['PeakFlow1', 'PeakFlow2']:
        return float(row['value'])
    return np.nan

def extract_milk_production_data(data):
    """ Extracts individual records of concern into unique columns """
    data['milk_weight'] = data.apply(extract_milk_weight, axis=1)
    data['average_flow'] = data.apply(extract_average_flow, axis=1)
    data['max_flow'] = data.apply(extract_max_flow, axis=1)
    return data

def consolidate_to_daily_summaries(data):
    """ Builds a daily summary table for storage """
    data = data.reset_index()
    ds = pd.DataFrame()
    ds['date'] = pd.to_datetime(data['date'].dt.date)
    data['date'] = pd.to_datetime(data['date'].dt.date)
    ds['animal_id'] = data['animal_id']
    ds = ds.set_index(['date', 'animal_id'])
    
    ds['milk_weight'] = data.groupby(['date', 'animal_id']).sum()['milk_weight']
    ds['average_flow'] = data.groupby(['date', 'animal_id']).mean()['average_flow']
    ds['max_flow'] = data.groupby(['date', 'animal_id']).max()['max_flow']

    ds = ds.reset_index().set_index('date')
    ds = ds.drop('index').drop_duplicates()
    return ds

def drop_features(data):
    """ Drop unused columns """
    data = validate_and_drop_record_type(data)
    data = validate_and_drop_animal_type(data)
    data.drop(['measurement'], axis=1)
    data.drop(['value'], axis=1)
    assert 'measurement', 'value' not in data.columns
    return data

def get_dataframe_from_file(data_file):
    """Parse and store milk volumes filename expected in YYYYMMDD.txt format"""
    # Extract milk date from filename
    milking_date = datetime.strptime(re.search(r'\d{8}', data_file)[0], '%Y%m%d')

    # Parse each line into dataframe
    milk_data = pd.read_csv(
        data_file,
        sep='&',
        lineterminator='\r',
        encoding='Latin',
        names=['full_line']
    )

    # Extract lines with animal specific measurements
    milk_data = milk_data[milk_data['full_line'].str.contains('\tR\t[0-9]+\tCow\t')]

    milk_data = extract_columns_from_fullline(milk_data)

    milk_data = transform_animal_id(milk_data)
    milk_data = transform_date(milk_data, milking_date)

    milk_data = extract_milk_production_data(milk_data)
    milk_data = drop_features(milk_data)
    milk_data = milk_data.pivot_table(index=['date', 'animal_id'], values=['milk_weight', 'average_flow', 'max_flow']).dropna()
    return consolidate_to_daily_summaries(milk_data)

def main():
    """ Selects a random weather file, parses file, prints df.info()"""
    files = glob.glob(f"{helper.get_config()['datasets']['milk_volumes']['regex']}")
    print(get_dataframe_from_file(random.choice(files)))

if __name__ == '__main__':
    sys.exit(main())
