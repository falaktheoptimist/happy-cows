"""
Loads raw files and places in database
"""
import sys
import glob as glob
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import helper_functions as helper
import parse_milk_volume as milk_volume
import parse_weather as weather
import parse_classification as classification

def retrieve_data(connection):
    milk = pd.read_sql_table('milk_volume', connection)
    score = pd.read_sql_table('classification', connection)
    return milk, score

def get_calving_dates(classification):
    return classification[['animal_id', 'date_calved']].dropna(how='any').sort_values('date_calved')

def add_days_since_calving(milk, calvings):
    calving_dates = []
    for index, row in milk.iterrows():
        milk_date = row['date']
        animal_id = row['animal_id']
        c = calvings[(calvings['date_calved'] <= milk_date) & (calvings['animal_id'] == animal_id)]
        c = c['date_calved']
        if len(c) == 0:
            calving_dates.append(np.NaN)
        else:
            c = c.sort_values(ascending=False)
            calving_dates.append(c.iloc[0])
    
    milk['date_calved'] = calving_dates
    milk['days_since_calving'] = np.subtract(milk['date'], milk['date_calved'])
    milk['days_since_calving'] = milk['days_since_calving'].apply(lambda x: x.days)
    return milk

def main():
    """ Loads add days-since-calving to milk data """
    with helper.get_db_engine().connect() as con:
        milk, score = retrieve_data(con)
        calvings = get_calving_dates(score)
        milk = add_days_since_calving(milk, calvings)
        milk.to_sql(con=con, name='milk_volume', if_exists='replace')

if __name__ == '__main__':
    sys.exit(main())
