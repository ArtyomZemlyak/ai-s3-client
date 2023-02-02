import os
import logging

import boto3
from botocore.client import Config

from ai_common_utils.files import load_env_file


logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)
if not os.environ.get("DOCKER_ENV"):
    load_env_file(".env")


S3_ENDPOINT_URL = ""
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
REGION_NAME = ""


s3 = boto3.resource(
    "s3",
    endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    config=Config(signature_version="s3v4"),
    region_name=REGION_NAME,
)
s3client = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    config=Config(signature_version="s3v4"),
    region_name=REGION_NAME,
)


print(list(s3.buckets.all()))
