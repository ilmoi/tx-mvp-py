from json import dumps

import boto3

client = boto3.client('firehose')

def send_to_firehose(json_data):
    response = client.put_record(
        DeliveryStreamName='PUT-S3-KsnN5',
        Record={
            'Data': dumps(json_data).encode('utf-8')
        }
    )
    # ic(response)