FROM python:3.11-slim-buster

RUN apt-get update
RUN apt-get install gcc zbar-tools libhdf5-dev libjpeg-dev zlib1g-dev -y


COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

CMD ["python","start.py"]