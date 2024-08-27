FROM python:3.11.4-slim-buster

# set work directory
RUN mkdir packd
COPY . /packd/
WORKDIR /packd

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc && \
    apt-get clean

# install dependencies
RUN pip install --upgrade pip
RUN pip install psycopg2-binary
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["gunicorn","--bind", ":5000", "packd.wsgi:application"]