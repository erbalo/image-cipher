import boto3


class S3:

    def __init__(self, **kwargs):
        self.__client = boto3.client('s3', **kwargs)


    def get_object(self, bucket: str, key: str) -> bytes:
        file_byte = self.__client.get_object(Bucket=bucket, Key=key)['Body'].read()
        return file_byte


    def upload_object(self, byte_array: bytes, bucket, key):
        self.__client.put_object(Body=byte_array, Bucket= bucket, Key=key)