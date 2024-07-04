FROM python:3.12-slim

WORKDIR /register

ADD ./requirements.txt /register/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt --no-cache-dir

# ARG COMMUNICATION_IP=default_value
# ENV COMMUNICATION_IP ${COMMUNICATION_IP}
ENV COMMUNICATION_IP=http://145.100.135.10

RUN echo $COMMUNICATION_IP

COPY . .

CMD ["python", "register.py"]
