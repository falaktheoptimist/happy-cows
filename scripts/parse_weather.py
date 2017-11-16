"""
Methods to parse weather data from csv files and return a dataframe
"""
import pandas as pd

def get_dataframe_from_file(data_file):
    return pd.read_csv(data_file,sep=',',header=0)