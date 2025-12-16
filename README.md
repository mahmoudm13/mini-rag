# mini-rag

This is a minimial implementation of the RAG model for question answering.

## Requirements

- Python 3.8 or later

### Install Dependencies
```bash
sudo apt update
sudo apt install libpq-dev gcc python3-dev
```


### Install Python using MiniConda

1) Download and install MiniConda from [here](https://docs.anaconda.com/free/miniconda/#quick-command-line-install).
2) Create a new environment using the following command:
```bash
$ conda create -n mini-rag python=3.8
```
3) Activate the environment:

```bash
$ conda activate mini-rag
```

### (Optional) Setup your command line for better readability
```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

## Installation

### Install the required packages

```bash
$ cd src/
$ pip install -r requirements.txt
```

### Setup the environment variables and Run Docker Compose Services

```bash
$ cd ../docker/env
$ cp .env.example.app .env.app
$ cp .env.example.postgres .env.postgres
$ cp .env.example.grafana .env.grafana
$ cp .env.example.postgres-exporter .env.postgres-exporter
```

update `.env` files with your credientials

```bash
$ cd ..
$ sudo docker compose up --build -d
```

## Access Services

- FastAPI: http://localhost:8000
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090

## Run the FastAPI server (Development Mode)
```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
``` 

## POSTMAN Collection
Download the POSTMAN collection from [/src/assets/mini-rag-app.postman_collection.json](/src/assets/mini-rag-app.postman_collection.json)
