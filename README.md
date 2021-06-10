# Course project. ITMO Big Data Infrastructure course '2021


# Run service

## Pre-requisites

1. Install latest Docker version [official instruction](https://docs.docker.com/engine/install/ubuntu/)
2. Install latest Docker-compose version [official instruction](https://docs.docker.com/compose/install/)
3. Install `nvidia-container-runtime` [official instruction](https://github.com/NVIDIA/nvidia-container-runtime)

## Run service using docker-compose

### 1. Prepare .env
```
cp docker-compose/envs/example.env docker-compose/.env
```

REPLACE `GOOGLE_API_KEY` with your own Google API key

### 2. (Optional) Download models

Put files from [Google Drive](https://drive.google.com/drive/u/0/folders/1evUxK42MayKFjb94ObUHxe-D62np9WhO) into folder ``./models/classification/``

### 3. (Optional) Build containers

```
cd docker-compose
DOCKER_BUILDKIT=1 docker-compose build
```

### 3*. (Optional) Pull containers
```
cd docker-compose
docker-compose pull
```

### 4. Run service
```
cd docker-compose
docker-compose up --force-recreate
```

Wait ~50 seconds for all services to run.

If you see errors, stop services, run `docker-compose rm -svf` (issue sescribed [here](https://github.com/wurstmeister/kafka-docker/issues/389)) and up containers again.

### 5. Analyze results

* Go to Grafana Web Ui [http://localhost:3000](http://localhost:3000)
* Add Clickhouse as a data source
    * Address `http://clickchouse:8123`
    * Default database `docker`
* Import dashboard from file ``./grafana_init/news_test-1623274149966.json``



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
