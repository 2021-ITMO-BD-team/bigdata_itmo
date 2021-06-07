# Course project on ITMO Big Data course


# Run service

## Pre-requisites

1. Install latest Docker version [official instruction](https://docs.docker.com/engine/install/ubuntu/)
2. Install latest Docker-compose version [official instruction](https://docs.docker.com/compose/install/)
3. Install `nvidia-container-runtime` [official instruction](https://github.com/NVIDIA/nvidia-container-runtime)

## Run service using docker-compose

1. Prepare .env
```
cp docker-compose/envs/example.env docker-compose/.env
```

REPLACE `GOOGLE_API_KEY` with your own Google API key

2. Run service
```
cd docker-compose
DOCKER_BUILDKIT=1 docker-compose up --build
```


# Sorta development guide

Please work in branches, then make pull-request into master, or the master will become a huge mess.

## 1. Install dependencies
```bash
pip install -r requirements/tensorflow.txt
pip install -r requirements/prod.txt
```

If you need development requirements - install them
```
pip install -r requirements/dev.txt
```

## 2. Install package from current folder in editable mode
```bash
pip install -e .
```

## 3. If you want to have autostyle - install [pre-commit](https://pre-commit.com/) and run
```bash
pre-commit install
```

Now hooks will apply to your code within folder `bigdata_itmo` each time you make `git commit`.
