FROM python:3.12-slim

RUN apt-get update
RUN apt-get install -y git
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY scenario_artefacts /app/scenario_artefacts
COPY scripts/create_init_repo.sh /app/create_init_repo.sh
COPY src /app/src
COPY tests /app/tests
COPY pytest.ini /app/pytest.ini
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
RUN bash create_init_repo.sh
