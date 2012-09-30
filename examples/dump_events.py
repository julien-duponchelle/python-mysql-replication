#!/usr/bin/env python
#
# Dump all replication events from a remote mysql server
#


import pymysql
from pymysqlreplication import BinLogStreamReader

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='mysql')


stream = BinLogStreamReader(conn)

for binlogevent in stream:
    binlogevent.dump()

conn.close()


