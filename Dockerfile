FROM python:3.10-alpine

WORKDIR /bot

COPY ./requirements.txt /bot/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["python3", "./src/main.py"]