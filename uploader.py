"""Func for uploading the file to the s3"""

from pathlib import Path
import boto3
from botocore.config import Config
from config import CLOUD_S3_ID_KEY, CLOUD_S3_SECRET_KEY, BUCKET_NAME


s3 = boto3.client(
        aws_access_key_id=CLOUD_S3_ID_KEY,
        aws_secret_access_key=CLOUD_S3_SECRET_KEY,
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        region_name='ru-central1',
        config=Config(signature_version='s3v4')
)


def upload_file_s3(file_path: Path, key: str) -> None:
    """Upload file to the s3"""
    file_path_str = str(file_path)
    s3.upload_file(file_path_str, BUCKET_NAME, key)
