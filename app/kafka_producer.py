from json import dumps
from time import sleep

from dotenv import load_dotenv
from icecream import ic
from kafka import KafkaProducer

load_dotenv()

producer = KafkaProducer(
    # bootstrap_servers=['localhost:9092'],
    bootstrap_servers=[
        'b-3.sol-cluster-2.k4mb5d.c18.kafka.us-east-1.amazonaws.com:9092',
        'b-2.sol-cluster-2.k4mb5d.c18.kafka.us-east-1.amazonaws.com:9092',
        'b-1.sol-cluster-2.k4mb5d.c18.kafka.us-east-1.amazonaws.com:9092'
    ],
    value_serializer=lambda x: x.encode('utf-8')
)
ic(producer)

for n in range(10):
    ic(f'sending {n}')
    # sleep(2)
    producer.send('cities', f"hola6-{n}")
