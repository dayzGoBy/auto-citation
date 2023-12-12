FROM python:3.10

WORKDIR /bot

COPY ./requirements.txt /bot/
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p photos