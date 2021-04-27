import time

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers="localhost:9092", value_serializer=str.encode)

for i in range(100000):
    producer.send("test", str(i))
    time.sleep(1)
