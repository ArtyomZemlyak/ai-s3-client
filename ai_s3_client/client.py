"""
File contains description of class S3Client.
"""

import io
import os
import logging
from functools import wraps

import boto3
from botocore.client import Config


def checkconn(func):
    @wraps(func)
    def wrapper(self, *Paramters, **kwParamters):
        if self.s3:
            return func(self, *Paramters, **kwParamters)
        else:
            raise ValueError("No connection to s3! Use .connect() before!")

    return wrapper


class S3Client:
    """
    A class for working with AWS S3 API and compatible API.
    """

    def __init__(self) -> None:
        self.s3 = None
        self.s3client = None

    def connect(self):
        """
        Connecting to s3 server or compatible s3 api server.
        """
        logging.info("S3Client connection to s3...")
        self.s3 = boto3.resource(
            "s3",
            endpoint_url=os.environ.get("S3_ENDPOINT_URL"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            config=Config(signature_version="s3v4"),
            region_name="eu-east-1",
        )
        self.s3client = boto3.client(
            "s3",
            endpoint_url=os.environ.get("S3_ENDPOINT_URL"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            config=Config(signature_version="s3v4"),
            region_name="eu-east-1",
        )

        logging.info("Connected to s3 done!")

    @checkconn
    def create_bucket(self, name: str):
        """
        Create backet on S3 connected server.

        Paramters
        ----------
        `name`: str
            S3 compatible name of backet to create.
        """
        creation_date = self.s3.Bucket(name).creation_date
        if not creation_date:
            self.s3.create_bucket(Bucket=name)
        else:
            logging.error(f"Bucket {name} already exists!")

    @checkconn
    def delete_bucket(self, name: str):
        """
        Delete backet on S3 connected server.

        Paramters
        ----------
        `name`: str
            S3 compatible name of existing backet to delete.
        """
        creation_date = self.s3.Bucket(name).creation_date
        if creation_date:
            self.s3.Bucket(name).delete()
        else:
            logging.error(f"Bucket {name} not exists!")

    @checkconn
    def upload_obj(self, bucket_name: str, obj: io.BytesIO, key: str):
        """
        Upload object to s3 connected server.

        Paramters
        ----------
        `bucket_name`: str
            S3 compatible name of existing backet.

        `obj`: io.BytesIO
            Temp file object bytes.

        `key`: str
            Key str name for file on s3 server.
        """
        self.s3.Bucket(bucket_name).upload_fileobj(obj, key)

    @checkconn
    def upload_file(self, bucket_name: str, path_file: str, key: str):
        """
        Upload file to s3 connected server.

        Paramters
        ----------
        `bucket_name`: str
            S3 compatible name of existing backet.

        `path_file`: str
            path to file.

        `key`: str
            Key str name for file on s3 server.
        """
        self.s3.Bucket(bucket_name).upload_file(path_file, key)

    @checkconn
    def download_obj(self, bucket_name: str, key: str):
        """
        Download object or file from s3 connected server.

        Paramters
        ----------
        `bucket_name`: str
            S3 compatible name of existing backet.

        `key`: str
            Key str name of file on s3 server.

        Returns
        -------
        `obj`: io.BytesIO
            Bytes of file object in temp file.
        """
        temp_file = io.BytesIO()
        self.s3.Bucket(bucket_name).download_fileobj(key, temp_file)
        return temp_file

    @checkconn
    def delete_obj(self, bucket_name: str, key: str):
        """
        Delete object or file from s3 connected server.

        Paramters
        ----------
        `bucket_name`: str
            S3 compatible name of existing backet.

        `key`: str
            Key str name of file on s3 server.
        """
        self.s3.Bucket(bucket_name).delete_objects(
            Delete={
                "Objects": [
                    {
                        "Key": key,
                        # 'VersionId': 'string'
                    },
                ],
                # 'Quiet': True|False
            },
            # MFA='string',
            # RequestPayer='requester',
            # BypassGovernanceRetention=True|False,
            # ExpectedBucketOwner='string'
        )

    @checkconn
    def get_all_objects(self, bucket_name: str, prefix: str):
        """
        Get list of objects in specific path on bucket.

        Paramters
        ----------
        `bucket_name`: str
            S3 compatible name of existing backet.

        `prefix`: str
            Prefix str for searching objects.

        Returns
        -------
        `objects`: Lisrt[str]
            List of finded str object keys.
        """
        bucket = self.s3.Bucket(bucket_name)
        objs = []
        for obj in bucket.objects.filter(Delimiter="/", Prefix=prefix):
            objs.append(obj.key)
        return objs

    @checkconn
    def get_file_url(self, bucket_name: str, key: str):
        """
        Get url of file.

        Paramters
        ----------
        `bucket_name`: str
            S3 compatible name of existing backet.

        `key`: str
            Key str name of file on s3 server.

        Returns
        -------
        `url`: str
            Generated url for file.
        """
        return self.s3client.generate_presigned_url(
            "get_object",
            ExpiresIn=3600,  # datetime.utcnow() + timedelta(seconds=100)
            Params={
                "Bucket": bucket_name,
                "Key": key,
            },
        )

    @checkconn
    def remove_obj(self, bucket_name: str, key: str, return_response: bool = False):
        """
        Remove obj from S3 server.

        Paramters
        ----------
        `bucket_name`: str
            S3 compatible name of existing backet.

        `key`: str
            Key str name of file on s3 server.

        `return_response`: bool
            True - return response after removing obj.

        Returns
        -------
        `response`: DeleteObjectsOutputTypeDef
            Response after removing obj.
        """
        response = self.s3.Bucket(bucket_name).delete_objects(
            Delete={
                "Objects": [
                    {
                        "Key": key,
                    },
                ],
            }
        )
        if return_response:
            return response
