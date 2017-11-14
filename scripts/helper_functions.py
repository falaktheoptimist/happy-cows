"""Helper Functions

This is a collection of helper methods for use across scripts.
"""
import os
import yaml   # yaml file interpretation

def ensure_directory_exists(path):
    """Validates that a directory exists.  Creates directory if it does not."""
    if not os.path.isdir(path):
        os.makedirs(path)

def get_config():
    """Returns Configuration Dictionary"""
    with open(".config.yml", 'r') as ymlfile:
        config = yaml.load(ymlfile)
    return config

