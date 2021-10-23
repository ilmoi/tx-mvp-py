from icecream import ic
from kinesis.consumer import KinesisConsumer


def receive_from_kinesis():
    consumer = KinesisConsumer('sol-stream')
    ic('ready to receive!')
    for m in consumer:
        m = m['Data'].decode('utf-8')
        ic(f"Received message: {m}")


receive_from_kinesis()
