#!/usr/bin/env python
#
# Dump all replication events from a remote mysql server
#


from pymysqlreplication import BinLogStreamReader

mysql_settings = {'host': '127.0.0.1', 'port': 3306, 'user': 'root', 'passwd': ''}


#server_id is your slave identifier. It should be unique
#blocking: True if you want to block and wait for the next event at the end of the stream
stream = BinLogStreamReader(connection_settings = mysql_settings, server_id = 3, blocking = True)

for binlogevent in stream:
    binlogevent.dump()

stream.close()


