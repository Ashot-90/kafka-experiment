from kafka import KafkaConsumer
from json import loads
import os
import sys


def start_consumer():
    try:
        topic = os.environ['TOPIC']
    except KeyError:
        print("Error: Environment variable has not found\n", file=sys.stderr)
        sys.exit(1)
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=['kafka:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8')))
    for message in consumer:
        message = dict(message.value)
        print('Received message :', message)


if __name__ == '__main__':
    start_consumer()
