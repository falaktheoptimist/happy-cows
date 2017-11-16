"""
Methods to parse classification data from csv files and return a dataframe
"""
from datetime import datetime
import re as re
import pandas as pd

def get_dataframe_from_file(data_file):
    classification_date = datetime.strptime(re.search('\d{4}_\d{2}_\d{2}', data_file)[0], '%Y_%m_%d')
    classifications = pd.read_csv(
        data_file,
        sep=',',
        header=1
    )
    classifications.dropna(axis=1, how='all', inplace=True)
    classifications['date'] = classification_date
    return classifications