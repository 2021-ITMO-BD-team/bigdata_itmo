# Audio-Classification
# Author: Shan Ali


Pipeline for prototyping audio classification algorithms with Tensorflow
------------------------------------------------------------------------

### Environment

```
conda env create -f environment.yml
```


### Audio Preprocessing

clean.py can be used to preview the signal envelope at a threshold to remove low magnitude data

`python clean.py`

![signal envelope](docs/signal_envelope.png)

### Training

Change model_type to: conv1d, conv2d, lstm

Sample rate and delta time should be the same from clean.py

`python train.py`

### Testing

move to same folder and type

python predict.py --model models/conv1d.h5 --src_dir path/to/directory/mp3files

NOTE: Please provide aviod relative path.