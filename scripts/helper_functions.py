"""Helper Functions

This is a collection of helper methods for use across scripts.
"""
import os
import yaml   # yaml file interpretation
from sqlalchemy import create_engine

_DATABASE_NAME = "happycows"
_DATABASE_PATH = "data/database/"

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
    """ Returns results of sqlalchemy.create_engine() """
    ensure_directory_exists(_DATABASE_PATH)
    return create_engine(f'sqlite:///{_DATABASE_PATH}{_DATABASE_NAME}.db')
