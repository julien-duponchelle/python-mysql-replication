ARG BASE_IMAGE=${BASE_IMAGE:-python:3.11-alpine}
FROM ${BASE_IMAGE}

COPY pymysqlreplication pymysqlreplication
COPY README.md README.md
COPY setup.py setup.py
RUN apk add bind-tools
RUN apk add mysql-client
RUN pip install .
RUN pip install pytest

ARG MYSQL_5_7
ENV MYSQL_5_7 ${MYSQL_5_7}

ARG MYSQL_5_7_CTL
ENV MYSQL_5_7_CTL ${MYSQL_5_7_CTL}