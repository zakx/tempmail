FROM python:3
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
RUN mkdir /code
WORKDIR /code
ADD requirements3.txt /code/
#RUN apt-get update && apt-get install -y postgresql-client
RUN pip install -r requirements3.txt
ADD . /code/
