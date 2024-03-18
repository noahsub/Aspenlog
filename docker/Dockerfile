FROM ubuntu:latest

WORKDIR /app

ADD . /app

RUN apt-get update -y

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update -y
RUN apt-get install -y python3.11 python3-pip

RUN python3.11 -m pip install --upgrade pip

RUN python3.11 -m pip install --no-cache-dir -r requirements_linux.txt

EXPOSE 42613

CMD ["python3.11", "main.py"]