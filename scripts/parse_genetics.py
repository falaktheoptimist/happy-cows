"""
Methods to parse herd genetics report from csv file and return a dataframe
"""
import sys
import glob
import random
import pandas as pd
import helper_functions as helper

def drop_features(data):
    """ Drop non-essential features. """
    data = data.reset_index()
    return data[[
        'ANIMAL_ID','NAME','PRO','%P','Fat','%F','Rel','Milk','SCS','PL','DPR','TYPE','REL','UDC','FLC','CTPI'
    ]]

def make_columns_lower(data):
    """Make all column headers lowercase"""
    data = data.reset_index()
    data.columns = [x.lower() for x in data.columns]
    return data

def get_dataframe_from_file(data_file):
    """ Parses Herd Genetics Report and returns dataframe """
    genetics = pd.read_csv(data_file, sep=',', header=0)[[
        'ANIMAL_ID','NAME','FS','PRO','%P','Fat','%F','Rel','Milk','SCS','PL','DPR','TYPE','REL','UDC','FLC','CTPI'
    ]]

    genetics = drop_features(genetics)
    return make_columns_lower(genetics)

def main():
    """ Selects a random herd genetics reprot file, parses file, prints df.info()"""
    files = glob.glob(f"{helper.get_config()['datasets']['genetics']['regex']}")
    print(get_dataframe_from_file(random.choice(files)).sample(5))

if __name__ == '__main__':
    sys.exit(main())
