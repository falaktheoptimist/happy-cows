"""
Methods to parse milk volume data from raw log files and return a dataframe
"""
from datetime import datetime
import re as re
import numpy as np
import pandas as pd

def extract_milk_weight(row):
    """ Extracts milk_weight values"""
    if row['measurement'] in ['MilkToday1', 'MilkToday2']:
        return float(row['value'])
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

def get_dataframe_from_file(data_file):
    """Parse and store milk volumes filename expected in YYYYMMDD.txt format"""
    # Extract milk date from filename
    milking_date = datetime.strptime(re.search('\d{8}', data_file)[0], '%Y%m%d')

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
    
    # Lines are expected to begin with \n character
    assert milk_data['full_line'].str.startswith("\n").all()
    milk_data['full_line'] = milk_data['full_line'].str.replace("\n","")
    
    # Split full_line into multiple columns, 
    assert len(milk_data.columns) == 1
    milk_data = pd.DataFrame(milk_data['full_line'].str.replace("\n","").str.split('\t').tolist(), index=None)
    assert len(milk_data.columns) == 6
    milk_data.columns = ['date', 'record_type', 'animal_id', 'animal_type', 'measurement', 'value']
    
    # milk_data.date is assumed to be in HH:MM:SS format.  Confirm, transform and combine with milk_date
    assert milk_data['date'].str.contains('\d{2}:\d{2}:\d{2}').all()
    milk_data['date'] = milk_data['date'].apply(lambda x: datetime.strptime(x, '%H:%M:%S'))
    milk_data['date'] = milk_data['date'].apply(lambda x: datetime.combine(milking_date, x.time()))
    assert not milk_data['date'].isnull().values.any()
    
    # milk_data.record_type is assumed to be homogenous value of 'R'
    assert milk_data['record_type'].values.all() == 'R'
    milk_data.drop(['record_type'], axis = 1, inplace = True)
    assert 'record_type' not in milk_data.columns
    
    # milk_data.animal_id is assumed to be an integer value
    assert milk_data['animal_id'].str.contains('^\d+$').all()
    milk_data['animal_id'] = milk_data['animal_id'].apply(lambda id_string: int(id_string))
    assert not milk_data['animal_id'].isnull().values.any()

    # milk_data.animal_type assumed not null, and homogenous value of 'Cow'
    assert milk_data['animal_type'].str.contains('^Cow$').all()
    milk_data.drop(['animal_type'], axis=1, inplace=True)
    assert 'animal_type' not in milk_data.columns

    milk_data['milk_weight'] = milk_data.apply(extract_milk_weight, axis=1)
    milk_data['average_flow'] = milk_data.apply(extract_average_flow, axis=1)
    milk_data['max_flow'] = milk_data.apply(extract_max_flow, axis=1)
    
    milk_data.drop(['measurement'], axis = 1, inplace = True)
    milk_data.drop(['value'], axis = 1, inplace = True)
    assert 'measurement', 'value' not in milk_data.columns

    return milk_data.pivot_table(index=['date', 'animal_id'], values=['milk_weight', 'average_flow', 'max_flow']).dropna()