"""
Calculates the number of days since calving and stores in milk database
"""
import sys
import numpy as np
import pandas as pd
import helper_functions as helper

def retrieve_data(connection):
    milk = pd.read_sql_table('milk_volume', connection)
    calvings = pd.read_sql_table('calvings', connection)
    return milk, calvings

def get_calving_dates(classification):
    return classification[['animal_id', 'calving_date']].dropna(how='any').sort_values('date_calved')

def add_days_since_calving(milk, calvings):
    calving_dates = []
    for index, row in milk.iterrows():
        milk_date = row['date']
        animal_id = row['animal_id']
        c = calvings[(calvings['calving_date'] <= milk_date) & (calvings['animal_id'] == animal_id)]
        c = c['calving_date']
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
        milk, calvings = retrieve_data(con)
        milk = add_days_since_calving(milk, calvings)
        milk.to_sql(con=con, name='milk_volume', if_exists='replace')

if __name__ == '__main__':
    sys.exit(main())
