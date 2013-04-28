#!/usr/bin/env python
#
# Update a redis server cache when an evenement is trigger
# in MySQL replication log
#

import redis
r = redis.Redis()

from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import *

mysql_settings = {'host': '127.0.0.1', 'port': 3306, 'user': 'root', 'passwd': ''}


__stream = BinLogStreamReader(connection_settings = mysql_settings,
                           only_events = [DeleteRowsEvent, WriteRowsEvent, UpdateRowsEvent])

for binlogevent in __stream:
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

__stream.close()



