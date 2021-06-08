import datetime
import json
import time

import numpy as np
from kafka import KafkaConsumer
from kafka.producer.kafka import KafkaProducer

from bigdata_itmo.config import classification_config, kafka_config


def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


def mock_prediction(message, topics=classification_config.TOPICS):
    np.random.seed(int(message.value))
    logits = np.random.uniform(size=(len(topics),))

    prediction = {topic: proba for topic, proba in zip(topics, softmax(logits))}
    prediction["time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return prediction


def predict_class():
    for message in consumer:
        ### Here goes prediction part
        ### Replace mock prediction with real prediction
        prediction = mock_prediction(message)
        ###

        producer.send(kafka_config.net_output_topic, value=prediction)
        time.sleep(2)


if __name__ == "__main__":
    consumer = KafkaConsumer(
        kafka_config.net_input_topic, bootstrap_servers=kafka_config.bootstrap_server, value_deserializer=bytes.decode
    )

    producer = KafkaProducer(
        bootstrap_servers=kafka_config.bootstrap_server,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    predict_class()
