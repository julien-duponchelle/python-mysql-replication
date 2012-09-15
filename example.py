#!/usr/bin/env python

import pymysql
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.constants.BINLOG import *

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='mysql')


stream = BinLogStreamReader(conn, blocking = False, resume_stream = False)

for binlogevent in stream:
    print binlogevent.timestamp
    print binlogevent.event_type
    if binlogevent.event is not None:
        print binlogevent.event.dump()

conn.close()


