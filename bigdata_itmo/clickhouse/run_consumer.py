import json
import os
import os.path as osp

from clickhouse_driver import Client
from kafka import KafkaConsumer

from bigdata_itmo.config import classification_config, clickhouse_config, kafka_config

LOG_FILE = osp.join("/bd_itmo", "clickhouse", "data.txt")


def create_ch_client():

    client = Client(clickhouse_config.address)

    columns_init = " ".join([f"{topic} Float32," for topic in classification_config.TOPICS])

    client.execute("use docker")
    client.execute(
        f"create table IF NOT EXISTS {clickhouse_config.table_name}"
        + f"( {columns_init}"
        + "time DateTime('Europe/Moscow')"
        + ")"
        + "ENGINE = MergeTree() ORDER BY time"
    )
    with open(LOG_FILE, "r") as fin:
        for line in fin:
            client.execute(f"INSERT INTO {clickhouse_config.table_name} format JSONEachRow {line}")
    return client


def read_messages():

    for message in consumer:
        message = message.value
        answer = json.dumps(message)
        client.execute(f"INSERT INTO {clickhouse_config.table_name} format JSONEachRow {answer}")
        with open(LOG_FILE, "a") as fout:
            fout.write(str(answer) + "\n")


if __name__ == "__main__":

    consumer = KafkaConsumer(
        kafka_config.net_output_topic,
        bootstrap_servers=[kafka_config.bootstrap_server],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )

    os.makedirs(osp.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "w"):
        pass
    client = create_ch_client()

    read_messages()
