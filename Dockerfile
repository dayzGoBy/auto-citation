FROM python:3.10

WORKDIR /bot

COPY ./requirements.txt /bot/
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p photos