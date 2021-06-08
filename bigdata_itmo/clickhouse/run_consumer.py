import json

from clickhouse_driver import Client
from kafka import KafkaConsumer

from bigdata_itmo.config import classification_config, clickhouse_config, kafka_config


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
    return client


def read_messages():

    for message in consumer:
        message = message.value
        answer = json.dumps(message)
        client.execute(f"INSERT INTO {clickhouse_config.table_name} format JSONEachRow {answer}")


if __name__ == "__main__":

    consumer = KafkaConsumer(
        kafka_config.net_output_topic,
        bootstrap_servers=[kafka_config.bootstrap_server],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )

    client = create_ch_client()

    read_messages()