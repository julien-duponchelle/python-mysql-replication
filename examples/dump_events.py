#!/usr/bin/env python
#
# Dump all replication events from a remote mysql server
#


from pymysqlreplication import BinLogStreamReader

mysql_settings = {'host': '127.0.0.1', 'port': 3306, 'user': 'root', 'passwd': ''}


stream = BinLogStreamReader(connection_settings = mysql_settings)

for binlogevent in stream:
    binlogevent.dump()

stream.close()


