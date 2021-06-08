import time

from kafka import KafkaProducer

from bigdata_itmo.config import kafka_config


def read_stream():

    for i in range(100000):
        producer.send(kafka_config.net_input_topic, str(i))
        time.sleep(3)


if __name__ == "__main__":

    producer = KafkaProducer(bootstrap_servers=kafka_config.bootstrap_server, value_serializer=str.encode)

    read_stream()
