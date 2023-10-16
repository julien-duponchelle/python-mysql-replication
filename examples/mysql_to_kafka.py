#!/usr/bin/env python

#
# Output Kafka events to the console from MySQL replication stream
#

from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
    DeleteRowsEvent,
    UpdateRowsEvent,
    WriteRowsEvent,
)

from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaConsumer, KafkaProducer

MYSQL_SETTINGS = {"host": "127.0.0.1", "port": 3306, "user": "root", "passwd": ""}


def create_kafka_topic(topic_name, num_partitions=1, replication_factor=1):
    admin_client = KafkaAdminClient(bootstrap_servers="127.0.0.1:9092")

    topic = NewTopic(
        name=topic_name,
        num_partitions=num_partitions,
        replication_factor=replication_factor
    )

    admin_client.create_topics(new_topics=[topic])


def main():
    global message_body
    producer = KafkaProducer(
        bootstrap_servers='127.0.0.1:9092',
        value_serializer=lambda v: str(v).encode('utf-8')
    )

    stream = BinLogStreamReader(
        connection_settings=MYSQL_SETTINGS,
        server_id=3,
        only_events=[DeleteRowsEvent,UpdateRowsEvent,WriteRowsEvent]
    )

    for binlogevent in stream:

        for row in binlogevent.rows:
            if isinstance(binlogevent, DeleteRowsEvent):
                topic = "deleted"
                message_body = row["values"].items()

            elif isinstance(binlogevent, UpdateRowsEvent):
                topic = "updated"
                message_body = row["after_values"].items()

            elif isinstance(binlogevent, WriteRowsEvent):
                topic = "created"
                message_body = row["values"].items()

            producer.send(topic, key=None, value=message_body)

    consumer = KafkaConsumer(
        'deleted',
        'updated',
        'created',
        bootstrap_servers='127.0.0.1:9092',
        value_deserializer=lambda x: x.decode('utf-8'),
        auto_offset_reset='earliest',
        group_id = '1'
    )

    for message in consumer:
        print(f"Topic: {message.topic}, Value: {message.value}")

    stream.close()
    producer.close()
    consumer.close()


if __name__ == "__main__":
    create_kafka_topic("deleted", num_partitions=3, replication_factor=1)
    create_kafka_topic("created", num_partitions=3, replication_factor=1)
    create_kafka_topic("updated", num_partitions=3, replication_factor=1)
    main()
