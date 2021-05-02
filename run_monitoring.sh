#!/bin/bash
# Start zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties &
# Start kafka
bin/kafka-server-start.sh config/server.properties &
# Create topic
bin/kafka-topics.sh --create --topic mytopic --bootstrap-server localhost:9092
# wait until server coming up
while ! nc -z localhost 9092
do
  echo Waiting for 9092 port to be accessible
  sleep 5
done
python3 producer.py &
python3 consumer.py &
wait
