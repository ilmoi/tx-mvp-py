from json import dumps
from time import sleep

import boto3
import botocore.exceptions
from icecream import ic
from kinesis.producer import KinesisProducer

client = boto3.client('kinesis')


# runs into this problem - https://github.com/NerdWalletOSS/kinesis-python/issues/24
# so just gonna use boto3 for now, no multiprocessing
# this probs wont fly with mainnet – too much data
def send_to_kinesis(json_data):
    try:
        producer = KinesisProducer(stream_name='sol-stream')
        producer.put(dumps(json_data).encode('utf-8'))
        ic('sent!')
    except Exception as e:
        ic(f'(!) failed to send data to kinesis: {e}')
        ic('retrying in 1 sec')
        sleep(1)
        send_to_kinesis(json_data)


def send_to_kinesis_boto3(json_data, partition_key):
    # try:
    response = client.put_record(
        StreamName='sol-stream',
        Data=dumps(json_data).encode('utf-8'),
        PartitionKey=partition_key,
    )
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise botocore.exceptions.ConnectionError
    ic('sent!')
    # except Exception as e:
    #     ic(f'(!) failed to send data to kinesis: {e}')
    #     ic('retrying in 1 sec')
    #     sleep(1)
    #     send_to_kinesis(json_data)
