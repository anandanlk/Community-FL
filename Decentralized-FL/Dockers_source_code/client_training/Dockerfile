# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /client
ADD ./requirements.txt /client/requirements.txt

RUN pip3 install -r requirements.txt --no-cache-dir

# ARG COMMUNICATION_IP=default_value
# ENV COMMUNICATION_IP ${COMMUNICATION_IP}
ENV COMMUNICATION_IP=145.100.135.10

RUN echo communication_ip is $COMMUNICATION_IP
COPY . .

EXPOSE 3000
CMD python local_training.py --communication_ip $COMMUNICATION_IP


