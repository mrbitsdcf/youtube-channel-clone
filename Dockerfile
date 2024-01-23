FROM python:3.10-buster

LABEL description="Container para Python"
LABEL version="1.0"

RUN apt-get -y update && \
    apt-get -y upgrade

RUN apt-get install ffmpeg -y

RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH "/"

WORKDIR .
