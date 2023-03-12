import json
import logging

from internal.application.images.service import Service as ImageService
from internal.adapters.storage.s3.handler import S3Storage
from internal.adapters.aws.client import S3


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def handler(event, context):

    print("Received event: " + json.dumps(event))
    print(context.aws_request_id)

    records = [x for x in event.get(
        'Records', []) if x.get('EventSource') == 'aws:sns']
    latest_event = records[-1] if records else {}

    info = latest_event.get('Sns', {})
    subject = info.get('Subject', '')
    message = info.get('Message', '')

    print(subject, '-', message)

    s3_client = S3(
        aws_access_key_id='AKIAQKN6BMPH2IFI5I4D',
        aws_secret_access_key='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',
        region_name='us-west-2'
    )
    storage = S3Storage('test/caja', 'jpeg', s3_client)
    service = ImageService(storage)
    service.encrypt('draco-test-trigger')
