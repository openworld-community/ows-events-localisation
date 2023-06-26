FROM python:3.11-slim-buster

RUN apt-get update
RUN apt-get install gcc zbar-tools libhdf5-dev libjpeg-dev zlib1g-dev -y

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY root/ /app

CMD ["python","start.py"]