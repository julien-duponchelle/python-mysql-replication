FROM python:3.11

RUN apt-get update && apt-get install -y mariadb-client && rm -rf /var/lib/apt/lists/*
RUN pip install pytest

ARG MYSQL_5_7
ENV MYSQL_5_7 ${MYSQL_5_7}

ARG MYSQL_5_7_PORT
ENV MYSQL_5_7_PORT ${MYSQL_5_7_PORT}

ARG MYSQL_8_0
ENV MYSQL_8_0 ${MYSQL_8_0}

ARG MYSQL_8_0_PORT
ENV MYSQL_8_0_PORT ${MYSQL_8_0_PORT}

ARG MARIADB_10_6
ENV MARIADB_10_6 ${MARIADB_10_6}

ARG MARIADB_10_6_PORT
ENV MARIADB_10_6_PORT ${MARIADB_10_6_PORT}

COPY .mariadb .mariadb
COPY README.md README.md
COPY setup.py setup.py
COPY pymysqlreplication pymysqlreplication

RUN pip install .
