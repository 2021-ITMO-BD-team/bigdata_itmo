FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04 AS base

RUN apt-get update
RUN apt-get install -y python3 python3-pip git wget libsm6 libxext6 libfontconfig1 libxrender1 cmake swig
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.6 1
RUN pip3 install --upgrade pip setuptools wheel

COPY requirements/tensorflow.txt /requirements/
RUN pip3 install --no-cache-dir -r /requirements/tensorflow.txt

COPY requirements/prod.txt requirements/
RUN pip3 install --no-cache-dir -r requirements/prod.txt

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ADD ./bigdata_itmo/__init__.py ./bigdata_itmo/__init__.py
COPY setup.py .
RUN pip3 install -e .

ARG VERSION
COPY models/classification/${VERSION}.pkl models/classification/${VERSION}.pkl

FROM base as prod

COPY ./bigdata_itmo/ /bigdata_itmo/
