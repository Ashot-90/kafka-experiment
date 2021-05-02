import time
import requests
import re
from kafka import KafkaProducer
import json
import os
import sys


def start_producer():
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    try:
        url = os.environ['URL']
        regexp = os.environ['PATTERN']
        topic = os.environ['TOPIC']
    except KeyError:
        print("Error: Environment variable has not found", end='', file=sys.stderr)
        sys.exit(1)
    while True:
        response = requests.get(url)
        data = {'url': url,
                'time': round(time.time() * 1000),
                'response_code': response.status_code,
                'response_time': response.elapsed.total_seconds(),
                'regexp': regexp}
        x = re.search(regexp, str(response.content))
        data['regexp_found'] = x is not None
        message = json.dumps(data)
        producer.send(topic, value=message.encode())
        time.sleep(1)


if __name__ == '__main__':
    start_producer()
