import boto3
import pytest
import os

from moto import mock_s3

from internal.adapters.aws.client import S3


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture
def s3_client(aws_credentials):
    with mock_s3():
        connection = boto3.client("s3", region_name="us-east-1")
        yield connection


@pytest.fixture
def s3_test(s3_client, bucket_name='testing'):
    s3_client.create_bucket(Bucket=bucket_name)
    yield


def test_get_object(s3_client, s3_test, bucket_name='testing', key='testing', body='testing body'):
    client = S3()

    s3_client.put_object(Bucket=bucket_name, Key=key, Body=body)
    response = client.get_object(bucket=bucket_name, key=key)

    assert response.decode() == body


def test_upload_object(s3_client, s3_test, bucket_name='testing', key='testing', body='testing body'):
    client = S3()

    encoded = body.encode()
    client.upload_object(byte_array=encoded, bucket=bucket_name, key=key)
    response = s3_client.get_object(Bucket=bucket_name, Key=key)

    assert response['Body'].read().decode() == encoded.decode()
