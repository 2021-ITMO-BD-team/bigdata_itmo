import os
from datetime import datetime
from os import path, remove

import ffmpeg
from kafka import KafkaProducer
from streamlink import streams

from bigdata_itmo.config import kafka_config, stream_config, system_config

filedir = system_config.internal_dir
os.makedirs(filedir, exist_ok=True)


def remove_files():
    for t in range(1, 13):
        temp_path = path.join(filedir, "part{}.ts".format(t))
        remove(temp_path)


def send_file(producer, address):
    producer.send(kafka_config.net_input_topic, address)


def stream_reciever(producer, stream_link):
    stream = streams(stream_link)
    fd = stream["worst"].open()
    i = 1
    while True:
        if i > 12:
            inputs_audio = []
            for t in range(1, 13):
                temp_path = path.join(filedir, "part{}.ts".format(t))
                inputs_audio.append(ffmpeg.input(temp_path).audio)
            unique_id = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            temp_path = path.join(filedir, f"{str(unique_id)}.wav")
            ffmpeg.concat(*inputs_audio, v=0, a=1).output(temp_path).run(capture_stderr=True)
            send_file(producer, temp_path)
            remove_files()
            i = 1
        data = fd.read(2500000 * 6)
        with open(path.join(filedir, "part{}.ts".format(i)), "wb+") as f:
            f.write(data)
        i += 1


if __name__ == "__main__":
    assert stream_config.stream_link is not None
    producer = KafkaProducer(bootstrap_servers=kafka_config.bootstrap_server, value_serializer=str.encode)
    stream_reciever(producer, stream_config.stream_link)
