import os
import logging
from time import time
from uuid import uuid4

from ai_common_utils.files import load_env_file
from ai_s3_client import S3Client


logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)
if not os.environ.get("DOCKER_ENV"):
    load_env_file(".env")


os.environ["S3_ENDPOINT_URL"] = "http://localhost:9000"
os.environ["POSTGRES_HOST"] = "localhost"


s3 = S3Client()

if not os.environ.get("DOCKER_ENV"):
    load_env_file("docker/varvara/.env")

os.environ["S3_ENDPOINT_URL"] = "http://localhost:9000"
os.environ["FASTAPI_HOST_REWRITE"] = "localhost"
os.environ["FASTAPI_PORT_REWRITE"] = "1234"
os.environ["STATS_HOST_REWRITE"] = "localhost"
os.environ["STATS_PORT_REWRITE"] = "1244"
BUCKET_NAME = "test"

s3 = S3Client()
s3.connect()

PATH_VIDEO = "docs/samples/video/nice.mp4"
idx = str(uuid4())
path_s3 = f"/speech/videos/{idx}"


st = time()
s3.upload_file(
    BUCKET_NAME,
    # "models",
    PATH_VIDEO,
    path_s3,
)
et = time()

print(et - st)
