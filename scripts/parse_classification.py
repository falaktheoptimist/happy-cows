"""
Methods to parse classification data from csv files and return a dataframe
"""
from datetime import datetime
import sys
import re as re
import glob
import random
import pandas as pd
import helper_functions as helper

_INT_COLUMNS = {
    'BARN_ID':'animal_id',
    'LAC':'lactation_count',
    'ST':'stature',
    'SR':'strength',
    'BD':'body_depth',
    'DF':'dairy_form',
    'RA':'rump_angle',
    'RW':'rump_width',
    'LS':'rear_legs_side',
    'RL':'rear_legs_rear',
    'LO':'locomotion',
    'FA':'foot_angle',
    'FU':'fore_udder',
    'UH':'udder_height',
    'UW':'udder_width',
    'UC':'udder_cleft',
    'UD':'udder_depth',
    'TP':'front_teat_placement',
    'RT':'rear_teat_placement',
    'TL':'teat_length',
    'UT':'udder_tilt',
    'CS':'body_condition',
    'FC':'front_end_capacity_aggregate',
    'DS':'dairy_strength_aggregate',
    'RP':'rump_aggregate',
    'FL':'feet_and_legs_aggregate',
    'MS':'udder_score_aggregate',
    'FS':'final_score'
}

_STRING_COLUMNS = {
    'AGE':'age'
}

_FLOAT_COLUMNS = {
    '%BAA':'breed_age_average'
}

_DATE_COLUMNS = {
    'DATE_CALVED':'date_calved',
    'DATE':'date'
}

def get_columns_dictionary():
    """ Returns compiled dictionary of all column name pairs """
    columns_dictionary = {}
    for type_dictionary in [_INT_COLUMNS, _STRING_COLUMNS, _FLOAT_COLUMNS, _DATE_COLUMNS]:
        columns_dictionary.update(type_dictionary)
    return columns_dictionary

def determine_animal_category(final_score):
    """ Returns a string category based on the final score of an animal """
    category = ""
    try:
        if final_score >= 90:
            category = "Excellent"
        if final_score >= 85:
            category = "Very Good"
        if final_score >= 80:
            category = "Good Plus"
        if final_score >= 75:
            category = "Good"
        if final_score >= 65:
            category = "Fair"
        category = "Poor"
    except ValueError:
        category = None
    return category

def get_dataframe_from_file(data_file):
    """ Returns modified dataframe from a classification file """
    columns_dictionary = get_columns_dictionary()
    date_string = re.search(r'\d{4}_\d{2}_\d{2}', data_file)[0]
    print(date_string)
    classification_date = datetime.strptime(date_string, '%Y_%m_%d')
    print(classification_date)
    class_df = pd.read_csv(
        data_file,
        sep=',',
        header=1
    )
    keys = list(columns_dictionary.keys())
    class_df['DATE'] = classification_date
    class_df = class_df[keys]

    for old_key, new_key in _INT_COLUMNS.items():
        class_df[old_key] = pd.to_numeric(class_df[old_key], errors='coerce', downcast='integer')
        class_df[old_key].rename(new_key)

    for old_key, new_key in _FLOAT_COLUMNS.items():
        class_df[old_key] = pd.to_numeric(class_df[old_key], errors='coerce', downcast='float')
        class_df[old_key].rename(new_key)

    for old_key, new_key in _DATE_COLUMNS.items():
        class_df[old_key] = pd.to_datetime(class_df[old_key], errors='coerce')
        class_df[old_key].rename(new_key)

    class_df.rename(columns=columns_dictionary, inplace=True)
    assert len(class_df.columns) == len(columns_dictionary)

    class_df['category'] = class_df['final_score'].apply(determine_animal_category)
    class_df['category'] = class_df['category'].astype('category')

    return class_df.dropna(axis=0, how='all')

def main():
    """ Selects a random classification file, parses file, prints df.info()"""
    files = glob.glob(f"{helper.get_config()['datasets']['classifications']['regex']}")
    print(get_dataframe_from_file(random.choice(files)).info())

if __name__ == '__main__':
    sys.exit(main())
