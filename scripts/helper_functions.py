"""Helper Functions

This is a collection of helper methods for use across scripts.
"""
import os
import yaml   # yaml file interpretation
from sqlalchemy import create_engine
from table_definitions import DATABASE_NAME
from table_definitions import DATABASE_PATH

def ensure_directory_exists(path):
    """Validates that a directory exists.  Creates directory if it does not."""
    if not os.path.isdir(path):
        os.makedirs(path)

def get_config():
    """Returns Configuration Dictionary"""
    with open(".config.yml", 'r') as ymlfile:
        config = yaml.load(ymlfile)
    return config

def get_db_engine():
    """ Returns results of sqlalchemy.create_engine('sqlite:///data/intermediate/happy-cows.db') """
    ensure_directory_exists(DATABASE_PATH)
    return create_engine(f'sqlite:///{DATABASE_PATH}{DATABASE_NAME}.db')
