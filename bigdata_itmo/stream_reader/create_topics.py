from confluent_kafka.admin import AdminClient, NewTopic

from bigdata_itmo.config import kafka_config

if __name__ == "__main__":

    admin_client = AdminClient({"bootstrap.servers": kafka_config.bootstrap_server})

    topic_list = []
    for topic_name in [kafka_config.net_input_topic, kafka_config.net_output_topic]:
        assert topic_name is not None, f"Got topic name {topic_name}"
        topic_list.append(NewTopic(topic_name, num_partitions=1, replication_factor=1))

    admin_client.create_topics(new_topics=topic_list, validate_only=False)
