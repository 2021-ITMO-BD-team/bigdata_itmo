import os
import os.path as osp

CURRENT_PATH = osp.dirname(osp.realpath(__file__))


class DownloadConfig:

    api_key = os.getenv("GOOGLE_API_KEY")


class SystemConfig:

    root_dir = osp.realpath(osp.join(CURRENT_PATH, ".."))
    data_dir = osp.join(root_dir, "data")
    model_dir = osp.join(root_dir, "models")


class ClassificationConfig:

    ### Change topics according to your model categories
    TOPICS = ["coronavirus", "disaster", "elections", "sports", "other"]
    ###


class KafkaConfig:

    server_address = os.getenv("KAFKA_SERVER_ADDRESS", "broker")
    server_port = os.getenv("KAFKA_SERVER_PORT", "9092")
    bootstrap_server = f"{server_address}:{server_port}"

    net_input_topic = os.getenv("NET_INPUT_TOPIC", "net_input_topic")
    net_output_topic = os.getenv("NET_OUTPUT_TOPIC", "net_output_topic")


class ClickhouseConfig:
    address = os.getenv("CLICKHOUSE_ADDRESS")
    table_name = "docker"


download_config = DownloadConfig()
system_config = SystemConfig()
classification_config = ClassificationConfig()
kafka_config = KafkaConfig()
clickhouse_config = ClickhouseConfig()
