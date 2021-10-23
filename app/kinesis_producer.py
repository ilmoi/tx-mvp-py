from dotenv import load_dotenv
from icecream import ic
from kinesis.producer import KinesisProducer

load_dotenv()


def send_to_kinesis():
    producer = KinesisProducer(stream_name='sol-stream')
    for i in range(100):
        producer.put(f"{i}".encode('utf-8'))
    ic('sent!')


send_to_kinesis()
