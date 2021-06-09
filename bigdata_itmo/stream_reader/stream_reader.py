import time
from os import path, remove
from sys import exit

import ffmpeg
import fire
from kafka import KafkaProducer
from streamlink import streams

from bigdata_itmo.config import kafka_config, system_config

filedir = path.join(system_config.data_dir, "internal")


def remove_files():
    try:
        for t in range(1, 13):
            temp_path = path.join(filedir, "part{}.ts".format(t))
            remove(temp_path)
        temp_path = path.join(filedir, "temp.wav")
        remove(temp_path)
    except:  # noqa E722
        print("Error while removing temporary files\n")
        exit(1)


def send_file(producer, stream_link):
    timestamp = time.time()
    try:
        with open("temp.wav", "rb") as f:
            bytes = f.read()
    except:  # noqa E722
        print("Error while reading audiofile\n")
        exit(1)
    try:
        producer.send(kafka_config.net_input_topic, bytes)
    except:  # noqa E722
        print("Error while sending file\n")
        exit(1)


def stream_reciever(producer, stream_link):
    stream = streams(stream_link)
    fd = stream["worst"].open()
    i = 1
    try:
        while True:
            if i > 12:
                inputs_audio = []
                for t in range(1, 13):
                    temp_path = path.join(filedir, "part{}.ts".format(t))
                    inputs_audio.append(ffmpeg.input(temp_path).audio)
                temp_path = path.join(filedir, "temp.wav")
                ffmpeg.concat(*inputs_audio, v=0, a=1).output(temp_path).run(capture_stderr=True)
                send_file(producer, stream_link)
                remove_files()
                i = 1
            data = fd.read(2500000 * 6)
            with open("part{}.ts".format(i), "wb+") as f:
                f.write(data)
            i += 1
    except ffmpeg.Error as err:
        print(err.stderr)
        fd.close()
        exit(1)


def start_reading(stream_link=None):
    if stream_link is not None:
        try:
            producer = KafkaProducer(bootstrap_servers=kafka_config.bootstrap_server)
        except:  # noqa E722
            print("Error while running producer\n")
            exit(1)
        stream_reciever(producer, stream_link)
    else:
        print("Enter a stream link with -stream_link\n")
        exit(1)


if __name__ == "main":
    fire.Fire(start_reading)
