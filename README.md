<p align="center">Mini-RAG: Production-Ready Retrieval-Augmented Generation</p>
<p align="center"> <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" /> <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI" /> <img src="https://img.shields.io/badge/Cohere-39594D?style=for-the-badge&logo=cohere&logoColor=white" alt="Cohere" /> <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" /> <img src="https://img.shields.io/badge/PgVector-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PgVector" /> <img src="https://img.shields.io/badge/Qdrant-FF4B4B?style=for-the-badge&logo=qdrant&logoColor=white" alt="Qdrant" /> <img src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white" alt="Nginx" /> <img src="https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white" alt="Prometheus" /> <img src="https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white" alt="Grafana" /> </p>

<p align="center"> <img src="https://img.shields.io/github/license/mahmoudm13/mini-rag?style=flat-square" alt="License" /> </p>

Mini-RAG is a streamlined, scalable implementation of a Retrieval-Augmented Generation pipeline. It bridges the gap between static LLMs and dynamic private data by integrating high-performance vector databases (Qdrant & PgVector) with a robust FastAPI backend. Designed with observability in mind, it includes a full monitoring stack to track performance and system health in real-time.
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
