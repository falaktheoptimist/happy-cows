import boto3  # AWS python SDK
import yaml   # yaml file interpretation
import sys, os

# Load config
with open(".config.yml", 'r') as ymlfile:
    config = yaml.load(ymlfile)

datasets = config['datasets']
s3 = boto3.resource(
    's3',
    aws_access_key_id=config['aws']['access_key'],
    aws_secret_access_key=config['aws']['secret_key']
)

def CheckDirectory(relative_path):
    if not os.path.isdir(relative_path):
        os.makedirs(relative_path)

def DownloadDataset(dataset, s3):
    current_bucket = s3.Bucket(dataset['bucket-name']) 
    bucket_list = current_bucket.objects.all()
    
    CheckDirectory(dataset['local-target-folder'])

    for bucket_file in bucket_list:
        origin = bucket_file.key
        target = dataset['local-target-folder'] + bucket_file.key
        print(f'|---> {origin}')
        s3.Bucket(dataset['bucket-name']).download_file(origin, target)

for dataset in datasets:
    print(f'Download of {dataset["name"]} data starting...')
    DownloadDataset(dataset, s3)
    print(f'Download of {dataset["name"]} data complete...')

print("Raw data has been successfully downloaded and can be found in the /data/raw/ directory.")