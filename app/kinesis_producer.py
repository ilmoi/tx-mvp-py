from json import dumps

from kinesis.producer import KinesisProducer


def send_to_kinesis(json_data):
    producer = KinesisProducer(stream_name='sol-stream')
    # for i in range(100):
    #     producer.put(f"{i}".encode('utf-8'))
    producer.put(dumps(json_data).encode('utf-8'))
    # ic('sent!')


