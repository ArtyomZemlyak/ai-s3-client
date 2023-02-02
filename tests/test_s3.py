import io
import os

from ai_s3_client import S3Client


if not os.environ.get("DOCKER_ENV"):
    from ai_common_utils.files import load_env_file
    load_env_file("tests/.env")


TEST_BUCKET_NAME = "my-test-bucket-for-tests"
s3c = S3Client()


def test_checkconn_decorator():
    try:
        s3c.create_bucket()
        assert False
    except ValueError:
        assert True


def test_create_bucket():
    if not s3c.s3:
        s3c.connect()
    s3c.create_bucket(TEST_BUCKET_NAME)
    assert True


def test_upload_obj():
    if not s3c.s3:
        s3c.connect()

    temp_file = io.BytesIO(b"Test!")

    s3c.upload_obj(TEST_BUCKET_NAME, temp_file, "test-file.txt")
    assert True


def test_try_delete_bucket():
    if not s3c.s3:
        s3c.connect()
    try:
        s3c.delete_bucket(TEST_BUCKET_NAME)
        assert False
    except Exception as e:
        assert True


def test_delete_obj():
    if not s3c.s3:
        s3c.connect()
    s3c.delete_obj(TEST_BUCKET_NAME, "test-file.txt")
    assert True


def test_delete_bucket():
    if not s3c.s3:
        s3c.connect()
    s3c.delete_bucket(TEST_BUCKET_NAME)
    assert True
