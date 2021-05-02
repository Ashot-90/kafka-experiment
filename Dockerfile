FROM ubuntu
RUN apt-get update && apt-get upgrade -y
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y wget default-jre python3 python3-pip netcat
RUN pip3 install kafka-python requests
RUN wget https://downloads.apache.org/kafka/2.8.0/kafka_2.13-2.8.0.tgz
RUN tar xzf kafka_2.13-2.8.0.tgz
WORKDIR kafka_2.13-2.8.0
COPY producer.py .
COPY consumer.py .
COPY run_monitoring.sh .
ENV TOPIC=mytopic
CMD ./run_monitoring.sh
