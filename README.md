python-mysql-replication
========================

Pure Python Implementation of MySQL replication protocol build on top of PyMYSQL. This allow you to receive event like insert, update, delete with their datas and raw SQL queries.

Use cases
===========

* MySQL to NoSQL database replication
* Audit

Project status
================

The current project is a proof of concept of what you can do with the MySQL
replication log.

The project is test with MySQL 5.5.


MySQL server settings
=========================

In your MySQL server configuration file you need to enable replication:

    [mysqld]
    server-id		 = 1
    log_bin			 = /var/log/mysql/mysql-bin.log
    expire_logs_days = 10
    max_binlog_size  = 100M
    binlog-format    = row #Very important if you want to receive write, update and delete row events

Examples
=========

All examples are available in the [examples directory](https://github.com/noplay/python-mysql-replication/tree/master/examples)


This example will dump all replication events to the console:

    from pymysqlreplication import BinLogStreamReader

    mysql_settings = {'host': '127.0.0.1', 'port': 3306, 'user': 'root', 'passwd': ''}


    stream = BinLogStreamReader(connection_settings = mysql_settings)

    for binlogevent in stream:
        binlogevent.dump()

    stream.close()


For this SQL sessions:

    CREATE DATABASE test;
    use test;
    CREATE TABLE test4 (id int NOT NULL AUTO_INCREMENT, data VARCHAR(255), data2 VARCHAR(255), PRIMARY KEY(id));
    INSERT INTO test4 (data,data2) VALUES ("Hello", "World");
    UPDATE test4 SET data = "World", data2="Hello" WHERE id = 1;
    DELETE FROM test4 WHERE id = 1;

Output will be:

    === RotateEvent ===
    Date: 1970-01-01T01:00:00
    Event size: 24
    Read bytes: 0

    === FormatDescriptionEvent ===
    Date: 2012-10-07T15:03:06
    Event size: 84
    Read bytes: 0

    === QueryEvent ===
    Date: 2012-10-07T15:03:16
    Event size: 64
    Read bytes: 64
    Schema: test
    Execution time: 0
    Query: CREATE DATABASE test

    === QueryEvent ===
    Date: 2012-10-07T15:03:16
    Event size: 151
    Read bytes: 151
    Schema: test
    Execution time: 0
    Query: CREATE TABLE test4 (id int NOT NULL AUTO_INCREMENT, data VARCHAR(255), data2 VARCHAR(255), PRIMARY KEY(id))

    === QueryEvent ===
    Date: 2012-10-07T15:03:16
    Event size: 49
    Read bytes: 49
    Schema: test
    Execution time: 0
    Query: BEGIN

    === TableMapEvent ===
    Date: 2012-10-07T15:03:16
    Event size: 31
    Read bytes: 30
    Table id: 781
    Schema: test
    Table: test4
    Columns: 3

    === WriteRowsEvent ===
    Date: 2012-10-07T15:03:16
    Event size: 27
    Read bytes: 10
    Table: test.test4
    Affected columns: 3
    Changed rows: 1
    Values:
    --
    * data : Hello
    * id : 1
    * data2 : World

    === XidEvent ===
    Date: 2012-10-07T15:03:16
    Event size: 8
    Read bytes: 8
    Transaction ID: 14097

    === QueryEvent ===
    Date: 2012-10-07T15:03:17
    Event size: 49
    Read bytes: 49
    Schema: test
    Execution time: 0
    Query: BEGIN

    === TableMapEvent ===
    Date: 2012-10-07T15:03:17
    Event size: 31
    Read bytes: 30
    Table id: 781
    Schema: test
    Table: test4
    Columns: 3

    === UpdateRowsEvent ===
    Date: 2012-10-07T15:03:17
    Event size: 45
    Read bytes: 11
    Table: test.test4
    Affected columns: 3
    Changed rows: 1
    Affected columns: 3
    Values:
    --
    * data : Hello => World
    * id : 1 => 1
    * data2 : World => Hello

    === XidEvent ===
    Date: 2012-10-07T15:03:17
    Event size: 8
    Read bytes: 8
    Transaction ID: 14098

    === QueryEvent ===
    Date: 2012-10-07T15:03:17
    Event size: 49
    Read bytes: 49
    Schema: test
    Execution time: 1
    Query: BEGIN

    === TableMapEvent ===
    Date: 2012-10-07T15:03:17
    Event size: 31
    Read bytes: 30
    Table id: 781
    Schema: test
    Table: test4
    Columns: 3

    === DeleteRowsEvent ===
    Date: 2012-10-07T15:03:17
    Event size: 27
    Read bytes: 10
    Table: test.test4
    Affected columns: 3
    Changed rows: 1
    Values:
    --
    * data : World
    * id : 1
    * data2 : Hello

    === XidEvent ===
    Date: 2012-10-07T15:03:17
    Event size: 8
    Read bytes: 8
    Transaction ID: 14099


Tests
========
<b>Be carefull</b> tests will reset the binary log of your MySQL server.

To run tests:

    python setup.py test



Licence
=======
Copyright 2012 Julien Duponchelle

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
