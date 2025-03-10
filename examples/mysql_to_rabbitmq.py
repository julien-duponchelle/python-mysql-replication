#!/usr/bin/env python

#
# Update a RabbitMQ when an event is triggered
# in MySQL replication log
#

import json
import pika

from pika import DeliveryMode
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
    DeleteRowsEvent,
    UpdateRowsEvent,
    WriteRowsEvent,
)

MYSQL_SETTINGS = {"host": "127.0.0.1", "port": 3306, "user": "root",
                  "passwd": "password"}

def main():
    stream = BinLogStreamReader(
        connection_settings=MYSQL_SETTINGS,
        server_id=3,
        only_events=[DeleteRowsEvent, WriteRowsEvent, UpdateRowsEvent],
    )

    credentials = pika.PlainCredentials(
        username='username',
        password='password'
    )
    params = pika.ConnectionParameters('rabbitmq_host', credentials=credentials)

    # RabbitMQ Connection Settings
    conn = pika.BlockingConnection(params)
    channel = conn.channel()
    channel.queue_declare(queue='order')
    channel.exchange_declare(durable=True, exchange_type='direct', exchange='direct')
    channel.queue_bind(queue='order', exchange='direct', routing_key='order')

    for binlogevent in stream:
        for row in binlogevent.rows:
            if isinstance(binlogevent, DeleteRowsEvent):
                routing_key = "order"
                message_body = row["values"].items()

            elif isinstance(binlogevent, UpdateRowsEvent):
                routing_key = "order"
                message_body = row["after_values"].items()

            elif isinstance(binlogevent, WriteRowsEvent):
                routing_key = "order"
                message_body = row["values"].items()

            properties = pika.BasicProperties(content_type='application/json',
                                              delivery_mode=DeliveryMode.Transient)
            channel.basic_publish(
                exchange='direct',
                routing_key=routing_key,
                body=json.dumps(message_body, default=lambda x: str(x)),
                properties=properties
            )

    stream.close()
    conn.close()


if __name__ == '__main__':
    main()
