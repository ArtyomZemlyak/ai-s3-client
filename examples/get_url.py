import os
import logging

from ai_common_utils.files import load_env_file
from ai_s3_client import S3Client


logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)
if not os.environ.get("DOCKER_ENV"):
    load_env_file(".env")


os.environ["S3_ENDPOINT_URL"] = "http://localhost:9000"
os.environ["POSTGRES_HOST"] = "localhost"
BUCKET_NAME = "test"


s3 = S3Client()
s3.connect()
url = s3.get_file_url(
    BUCKET_NAME,
    "/speech/videos/1be47440-1494-4939-9a06-aa90395fb92c.mp4",
)

print(url)
