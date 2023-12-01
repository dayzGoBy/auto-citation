FROM python:3.10

WORKDIR /bot

COPY ./requirements.txt /bot/
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . /app

CMD ["python3", "./src/main.py"]