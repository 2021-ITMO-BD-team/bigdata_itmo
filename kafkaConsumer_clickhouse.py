from kafka import KafkaConsumer
from clickhouse_driver import Client, connect
import json


consumer = KafkaConsumer(
    'testPK',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: json.loads(x.decode('utf-8')))

client = Client('localhost')
client.execute('use trail')
client.execute('truncate table test')
client.execute("create table IF NOT EXISTS test(Business Float32,Political Float32, covid Float32,crime Float32, time DateTime('Europe/Moscow'), \
    sports Float32 ) ENGINE = MergeTree() ORDER BY time")

for message in consumer:
    message = message.value
    some_other_dict = json.dumps(message)
    # tupVal = tuple(message.values())
    print(some_other_dict)
    client.execute("INSERT INTO test format JSONEachRow {}".format(some_other_dict))
