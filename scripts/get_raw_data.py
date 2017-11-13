# -*- coding: utf-8 -*-
"""Raw Data Retrieval

This script populates the ./data/raw folders with an raw files currently stored on AWS S3.

Proper configuration and placement of .config.yml in the root directory is required for operation.
"""
import sys
import os
import boto3  # AWS python SDK
import yaml   # yaml file interpretation

def get_config():
    """Returns Configuration Dictionary"""
    with open(".config.yml", 'r') as ymlfile:
        config = yaml.load(ymlfile)
    return config

def ensure_directory_exists(path):
    """Validates that a directory exists.  Creates directory if it does not."""
    if not os.path.isdir(path):
        os.makedirs(path)

def download_dataset(target_directory, bucket_name, s3):
    """Downloads an S3 Dataset and places it in a targeted directory"""
    ensure_directory_exists(target_directory)
    bucket_list = s3.Bucket(bucket_name).objects.all()

    for bucket_file in bucket_list:
        target = target_directory + bucket_file.key
        print(f'|---> {bucket_file.key}')
        s3.Bucket(bucket_name).download_file(bucket_file.key, target)

def main():
    """Gets raw data from AWS"""
    cfg = get_config()
    s3_resource = boto3.resource(
        's3',
        aws_access_key_id=cfg['aws']['access_key'],
        aws_secret_access_key=cfg['aws']['secret_key']
    )

    for dataset in cfg['datasets']:
        download_dataset(
            target_directory=dataset['local-target-folder'],
            bucket_name=dataset['bucket-name'],
            s3=s3_resource
        )
    print("Download Complete.")

if __name__ == "__main__":
    sys.exit(main())