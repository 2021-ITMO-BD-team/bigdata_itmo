import datetime
import json
import time
import argparse
import numpy as np
from kafka import KafkaConsumer
from kafka.producer.kafka import KafkaProducer
from predict import load_ml_model, make_prediction
from mp3towav import convert
from bigdata_itmo.config import classification_config, kafka_config


model = None
args = None

def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

def convert2wav(bytes):
    # How to convert bytes to .wav format???

    # with open("temp.wav", "wb") as f:
    #     f.write(bytes)
    pass

def actual_prediction(bytes_arr):
    
    # Read bytes from kafka
    # bytes = consumer.receive(kafka_config.net_input_topic)
    # convert2wav(bytes)

    # pred = model.predict(read_wav) # {time: time, crime: 1, covid: 0, sports: 0, others:0} 
    pred_dict = make_prediction(model, args, bytes_arr)
    return pred_dict

def mock_prediction(message, topics=classification_config.TOPICS):
    np.random.seed(int(message))
    logits = np.random.uniform(size=(len(topics),))

    prediction = {topic: proba for topic, proba in zip(topics, softmax(logits))}
    prediction["time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return prediction

def test(bytes_arr):
    prediction_dict = actual_prediction(bytes_arr)
    prediction_dict["time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return prediction_dict


def predict_class():
    for message in consumer:
        ### Here goes prediction part
        ### Replace mock prediction with real prediction

        # prediction = mock_prediction(message)
        prediction_dict = actual_prediction(message.value)
        prediction_dict["time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        ### Sending to clickhouse
        producer.send(kafka_config.net_output_topic, value=prediction_dict)
        time.sleep(2)


if __name__ == "__main__":
    
    with_pipeline = True
    
    parser = argparse.ArgumentParser(description='Audio Classification Model')
    parser.add_argument('--model_fn', type=str, default='models/conv1d.h5',
                        help='model file to make predictions')
    # parser.add_argument('--pred_fn', type=str, default='y_pred',
    #                     help='fn to write predictions in logs dir')
    # parser.add_argument('--src_dir', type=str, default='wavfiles',
    #                     help='directory containing wavfiles to predict')
    parser.add_argument('--dt', type=float, default=1.0,
                        help='time in seconds to sample audio')
    parser.add_argument('--sr', type=int, default=16000,
                        help='sample rate of clean audio')
    parser.add_argument('--threshold', type=str, default=20,
                        help='threshold magnitude for np.int16 dtype')
    args, _ = parser.parse_known_args()
    model = load_ml_model(args.model_fn) # load model from .h5

    if not with_pipeline:
        # print("Converting mp3 to wav... This may take a while ")
        convert('./mp3')
        path = "./mp3_wav/0.wav"
        with open(path, "rb") as f:
            bytes_arr = f.read()
        print(test(bytes_arr))

    else:
        # how to get wav files from kafka (stream_reader.py)
        consumer = KafkaConsumer(
            kafka_config.net_input_topic, bootstrap_servers=kafka_config.bootstrap_server, value_deserializer=bytes.decode
        )

        producer = KafkaProducer(
            kafka_config.net_output_topic,
            bootstrap_servers=kafka_config.bootstrap_server,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

        predict_class()
