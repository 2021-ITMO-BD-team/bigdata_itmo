from kafka import KafkaConsumer

consumer = KafkaConsumer(bootstrap_servers="localhost:9092", group_id="test", value_deserializer=bytes.decode)

consumer.subscribe(["test"])

for message in consumer:
    print(f"topic={message.topic} partition={message.partition} offset={message.offset} value={message.value}")
