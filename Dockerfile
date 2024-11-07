FROM python:3.12-slim

RUN apt-get update
RUN apt-get install -y git
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY scenario_artefacts /app/scenario_artefacts
COPY src /app/src
COPY tests /app/tests
COPY pyproject.toml /app/pyproject.toml
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
