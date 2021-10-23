from json import loads

from dotenv import load_dotenv
from icecream import ic
from kafka import KafkaConsumer

load_dotenv()

consumer = KafkaConsumer(
    'cities',
    # bootstrap_servers=['localhost:9092'],
    bootstrap_servers=[
        'b-3.sol-cluster-2.k4mb5d.c18.kafka.us-east-1.amazonaws.com:9092',
        'b-2.sol-cluster-2.k4mb5d.c18.kafka.us-east-1.amazonaws.com:9092',
        'b-1.sol-cluster-2.k4mb5d.c18.kafka.us-east-1.amazonaws.com:9092'
    ],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: x.decode('utf-8')
)

ic('Ready to receive messages!')
for m in consumer:
    m = m.value
    ic(m)
