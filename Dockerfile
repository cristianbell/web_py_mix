FROM python:3.8-buster
#FROM ubuntu
#RUN apt-get update
#RUN apt-get -y install python3 python3-pip

WORKDIR /code
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
# RUN apk add --no-cache gcc musl-dev linux-headers
RUN apt-get -y install gcc
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run"]
