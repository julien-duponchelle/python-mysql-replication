#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Update a redis server cache when an evenement is trigger
# in MySQL replication log
#

import redis

from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
    DeleteRowsEvent,
    UpdateRowsEvent,
    WriteRowsEvent,
)

MYSQL_SETTINGS = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "passwd": ""
}


def main():
    r = redis.Redis()

    stream = BinLogStreamReader(
        connection_settings=MYSQL_SETTINGS,
        only_events=[DeleteRowsEvent, WriteRowsEvent, UpdateRowsEvent])

    for binlogevent in stream:
        prefix = "%s:%s:" % (binlogevent.schema, binlogevent.table)

        for row in binlogevent.rows:
            if isinstance(binlogevent, DeleteRowsEvent):
                vals = row["values"]
                r.delete(prefix + str(vals["id"]))
            elif isinstance(binlogevent, UpdateRowsEvent):
                vals = row["after_values"]
                r.hmset(prefix + str(vals["id"]), vals)
            elif isinstance(binlogevent, WriteRowsEvent):
                vals = row["values"]
                r.hmset(prefix + str(vals["id"]), vals)

    stream.close()


if __name__ == "__main__":
    main()
