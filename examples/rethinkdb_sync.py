#!/usr/bin/env python
#
# Insert a new element in  a RethinkDB database
# when an evenement is trigger in MySQL replication log
#
# Please test with MySQL employees DB available here: https://launchpad.net/test-db/ 
#

import datetime
import rethinkdb as r
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import *


#RethinkDB
r.connect('localhost', 28015, 'mysql')
try:
    r.db_drop('mysql').run()
except:
    pass
r.db_create('mysql').run()

tables = ['dept_emp', 'dept_manager', 'titles', 'salaries', 'employees', 'departments']
for table in tables:
    r.db('mysql').table_create(table).run()


#MySQL
mysql_settings = {'host': '127.0.0.1', 'port': 3306, 'user': 'root', 'passwd': ''}
stream = BinLogStreamReader(connection_settings = mysql_settings,
                           only_events = [DeleteRowsEvent, WriteRowsEvent, UpdateRowsEvent], blocking = True)

#Process Feed
for binlogevent in stream:
    prefix = "%s:%s:" % (binlogevent.schema, binlogevent.table)

    for row in binlogevent.rows:
        if binlogevent.schema == 'employees':
            if isinstance(binlogevent, WriteRowsEvent):
                vals = {}
                for (k, v) in row["values"].items():
                    if isinstance(v, datetime.date):
                        vals[str(k)] = str(v)
                    else:
                        vals[str(k)] = v
                r.table(binlogevent.table).insert(vals).run()

stream.close()



