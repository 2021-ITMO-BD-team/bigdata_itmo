import os

import numpy as np
from clean import downsample_mono, envelope
from kapre.time_frequency import STFT, ApplyFilterbank, Magnitude, MagnitudeToDecibel
from tensorflow.keras.models import load_model
from tqdm import tqdm

from bigdata_itmo.config import classification_config

# import argparse
# from glob import glob
# import pandas as pd
# from mp3towav import convert
# from sklearn.preprocessing import LabelEncoder


CLASSES = {cat_id: topic for cat_id, topic in enumerate(classification_config.TOPICS)}


def load_ml_model(model_fn):
    print("Loading prediction model...")
    model = load_model(
        model_fn,
        custom_objects={
            "STFT": STFT,
            "Magnitude": Magnitude,
            "ApplyFilterbank": ApplyFilterbank,
            "MagnitudeToDecibel": MagnitudeToDecibel,
        },
    )
    return model


def make_prediction(model, args, address):
    # print("Converting mp3 to wav... This may take a while ")
    # convert(args.src_dir)

    # wav_paths = glob('{}/**'.format(args.src_dir), recursive=True)
    # wav_paths = sorted([x.replace(os.sep, '/') for x in wav_paths if '.wav' in x])
    # classes = sorted(os.listdir(args.src_dir))
    # labels = [os.path.split(x)[0].split('/')[-1] for x in wav_paths]
    # le = LabelEncoder()
    # y_true = le.fit_transform(labels)

    # Convert bytes into wav file
    results = []
    wav_paths = [address]  # only one file
    ret_dict = {k: 0 for k in CLASSES.values()}
    for z, wav_fn in tqdm(enumerate(wav_paths), total=len(wav_paths)):
        rate, wav = downsample_mono(wav_fn, args.sr)
        mask, env = envelope(wav, rate, threshold=args.threshold)
        clean_wav = wav[mask]
        step = int(args.sr * args.dt)
        batch = []

        for i in range(0, clean_wav.shape[0], step):
            sample = clean_wav[i : i + step]
            sample = sample.reshape(-1, 1)
            if sample.shape[0] < step:
                tmp = np.zeros(shape=(step, 1), dtype=np.float32)
                tmp[: sample.shape[0], :] = sample.flatten().reshape(-1, 1)
                sample = tmp
            batch.append(sample)
        X_batch = np.array(batch, dtype=np.float32)
        y_pred = model.predict(X_batch)
        y_mean = np.mean(y_pred, axis=0)
        y_pred_ind = np.argmax(y_mean)
        real_class = os.path.dirname(wav_fn).split("/")[-1]
        # print('Actual class: {}, Predicted class: {}'.format(real_class, classes[y_pred]))
        for i in range(y_mean.shape[0]):
            ret_dict[CLASSES[i]] = f"{y_mean[i]:.4f}"
        # ret_dict[CLASSES[y_pred_ind]] = 1

        # results.append(y_mean) #{crime: 1, covid: 0, sports: 0, others:0}
    return ret_dict
    # np.save(os.path.join('logs', args.pred_fn), np.array(results))


# if __name__ == '__main__':

# parser = argparse.ArgumentParser(description='Audio Classification Training')
# parser.add_argument('--model_fn', type=str, default='models/lstm.h5',
#                     help='model file to make predictions')
# parser.add_argument('--pred_fn', type=str, default='y_pred',
#                     help='fn to write predictions in logs dir')
# parser.add_argument('--src_dir', type=str, default='wavfiles',
#                     help='directory containing wavfiles to predict')
# parser.add_argument('--dt', type=float, default=1.0,
#                     help='time in seconds to sample audio')
# parser.add_argument('--sr', type=int, default=16000,
#                     help='sample rate of clean audio')
# parser.add_argument('--threshold', type=str, default=20,
#                     help='threshold magnitude for np.int16 dtype')
# args, _ = parser.parse_known_args()

# make_prediction(args)
