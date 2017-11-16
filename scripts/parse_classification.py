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

_COLUMN_DICT = {
    'BARN_ID':'animal_id',
    'AGE':'age',
    'LAC':'lactation_count',
    'DATE_CALVED':'date_calved',
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
    'FS':'final_score',
    '%BAA':'breed_age_average'
}

def determine_breakdown_category_from_final_score(final_score):
    """ Returns a string category based on the final score of an animal """
    final_score = int(final_score)
    if final_score >= 90:
        return "Excellent"
    if final_score >= 85:
        return "Very Good"
    if final_score >= 80:
        return "Good Plus"
    if final_score >= 75:
        return "Good"
    if final_score >= 65:
        return "Fair"
    return "Poor"

def get_dataframe_from_file(data_file):
    """ Returns modified dataframe from a classification file """
    classification_date = datetime.strptime(re.search('\d{4}_\d{2}_\d{2}', data_file)[0], '%Y_%m_%d')
    class_df = pd.read_csv(
        data_file,
        sep=',',
        header=1
    )
    class_df = class_df[list(_COLUMN_DICT.keys())]
    class_df.rename(columns=_COLUMN_DICT, inplace=True) 
    assert len(class_df.columns) == len(_COLUMN_DICT)
    class_df.dropna(axis=0, how='any', inplace=True)
    class_df['date'] = classification_date
    class_df['category'] = class_df['final_score'].apply(lambda x: determine_breakdown_category_from_final_score(x))
    return class_df

def main():
    """ Selects a random classification file and attempts to parse it. Prints df.head(10) """
    files = glob.glob(f"{helper.get_config()['datasets']['classifications']['regex']}")
    print(get_dataframe_from_file(random.choice(files)).head(10))

if __name__ == '__main__':
    sys.exit(main())
