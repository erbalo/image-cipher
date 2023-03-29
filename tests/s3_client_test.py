import os
import boto3
import pytest

from moto import mock_s3

from internal.adapters.aws.client import S3


@pytest.fixture
def _aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture
def _s3_client(_aws_credentials):
    with mock_s3():
        connection = boto3.client("s3", region_name="us-east-1")
        yield connection


@pytest.fixture
def _s3_test(_s3_client, bucket_name='testing'):
    _s3_client.create_bucket(Bucket=bucket_name)
    yield


def test_get_object(_s3_client, _s3_test, bucket_name='testing', key='testing', body='testing body'):
    client = S3()

    _s3_client.put_object(Bucket=bucket_name, Key=key, Body=body)
    response = client.get_object(bucket=bucket_name, key=key)

    assert response.decode() == body


def test_upload_object(_s3_client, _s3_test, bucket_name='testing', key='testing', body='testing body'):
    client = S3()

    encoded = body.encode()
    client.upload_object(byte_array=encoded, bucket=bucket_name, key=key)
    response = _s3_client.get_object(Bucket=bucket_name, Key=key)

    assert response['Body'].read().decode() == encoded.decode()
