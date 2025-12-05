import os

import boto3
from dotenv import load_dotenv

bucket_name = os.getenv("MODELS_BUCKET", "bucket")
app_path = os.getenv("APP_PATH", "/app/")
load_dotenv(app_path + '.env')
os.makedirs(os.getenv("WEIGHT_ROOT"), exist_ok=True)


def download_directory_from_s3(bucket_name: str, s3_folder: str, local_dir: str):
    cf_account_id = os.getenv("CF_ACCOUNT_ID")
    s3 = boto3.client('s3', endpoint_url=f'https://{cf_account_id}.r2.cloudflarestorage.com')
    paginator = s3.get_paginator('list_objects_v2')
    for result in paginator.paginate(Bucket=bucket_name, Prefix=s3_folder):
        if 'Contents' not in result:
            continue
        for obj in result['Contents']:
            if obj['Key'] == s3_folder:
                continue
            else:
                path, filename = os.path.split(obj['Key'])
                local_file_path = os.path.join(local_dir, os.path.relpath(path, s3_folder), filename)
                if not os.path.exists(os.path.join(local_dir, os.path.relpath(path, s3_folder))):
                    os.makedirs(os.path.join(local_dir, os.path.relpath(path, s3_folder)))
                s3.download_file(bucket_name, obj['Key'], local_file_path)


download_directory_from_s3(bucket_name, 'models/', os.getenv("WEIGHT_ROOT"))
