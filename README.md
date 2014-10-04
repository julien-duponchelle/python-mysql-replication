python-mysql-replication
========================

<a href="https://travis-ci.org/noplay/python-mysql-replication"><img src="https://travis-ci.org/noplay/python-mysql-replication.svg?branch=master"></a>&nbsp;
<a href="https://pypi.python.org/pypi/mysql-replication"><img src="http://img.shields.io/pypi/dm/mysql-replication.svg"></a>

Pure Python Implementation of MySQL replication protocol build on top of PyMYSQL. This allow you to receive event like insert, update, delete with their datas and raw SQL queries.

Use cases
===========

* MySQL to NoSQL database replication
* MySQL to search engine replication
* Invalidate cache when something change in database
* Audit
* Real time analytics

Documentation
==============

A work in progress documentation is available here: https://python-mysql-replication.readthedocs.org/en/latest/

Instruction about building documentation is available here:
https://python-mysql-replication.readthedocs.org/en/latest/developement.html


Installation
=============

```
pip install mysql-replication
```

Mailling List
==============

You can get support and discuss about new features on:
https://groups.google.com/d/forum/python-mysql-replication



Project status
================

The current project is a proof of concept of what you can do with the MySQL
replication log.

The project is test with:
* MySQL 5.5 and 5.6
* Python >= 2.6.7
* Python 3.3 and 3.4 (3.2 is not supported)
* PyPy (really faster than the standard Python interpreter)

It's not tested in real production situation.

Limitations
=============

https://python-mysql-replication.readthedocs.org/en/latest/limitations.html

Projects using this library
===========================

* MySQL River Plugin for ElasticSearch: https://github.com/scharron/elasticsearch-river-mysql
* Ditto: MySQL to MemSQL replicator https://github.com/memsql/ditto
* ElasticMage: Full Magento integration with ElasticSearch https://github.com/ElasticMage/elasticmage
* Cache buster: an automatic cache invalidation system https://github.com/rackerlabs/cache-busters
* Zabbix collector for OpenTSDB https://github.com/OpenTSDB/tcollector/blob/master/collectors/0/zabbix_bridge.py
* Meepo: Event sourcing and event broadcasting for datebases. https://github.com/eleme/meepo

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

```python
from pymysqlreplication import BinLogStreamReader

mysql_settings = {'host': '127.0.0.1', 'port': 3306, 'user': 'root', 'passwd': ''}

stream = BinLogStreamReader(connection_settings = mysql_settings)

for binlogevent in stream:
    binlogevent.dump()

stream.close()
```

For this SQL sessions:

```sql
CREATE DATABASE test;
use test;
CREATE TABLE test4 (id int NOT NULL AUTO_INCREMENT, data VARCHAR(255), data2 VARCHAR(255), PRIMARY KEY(id));
INSERT INTO test4 (data,data2) VALUES ("Hello", "World");
UPDATE test4 SET data = "World", data2="Hello" WHERE id = 1;
DELETE FROM test4 WHERE id = 1;
```

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
When it's possible we have an unit test.

More information is available here:
https://python-mysql-replication.readthedocs.org/en/latest/developement.html

Changelog
==========
https://python-mysql-replication.readthedocs.org/en/latest/changelog.html

Similar projects
==================
* Kodoma: Ruby-binlog based MySQL replication listener https://github.com/y310/kodama
* MySQL Hadoop Applier: C++ version http://dev.mysql.com/tech-resources/articles/mysql-hadoop-applier.html

Special thanks
================
* MySQL binlog from Jeremy Cole was a great source of knowledge about MySQL replication protocol https://github.com/jeremycole/mysql_binlog
* Samuel Charron for his help https://github.com/scharron

Contributors
==============

Major contributor:
* bjoernhaeuser for his bugs fixing, improvements and community support https://github.com/bjoernhaeuser

Other contributors:
* Dvir Volk for bug fix https://github.com/dvirsky
* Lior Sion code cleanup and improvements https://github.com/liorsion
* Lx Yu code improvements, primary keys detections https://github.com/lxyu
* Young King for pymysql 0.6 support https://github.com/youngking
* David Reid checksum checking fix https://github.com/dreid
* Alex Gaynor fix smallint24 https://github.com/alex
* lifei NotImplementedEvent https://github.com/lifei
* Maralla Python 3.4 fix https://github.com/maralla
* Daniel Gavrila more MySQL error codes https://github.com/danielduduta
* Bernardo Sulzbach code cleanup https://github.com/mafagafo
* Darioush Jalali Python 2.6 backport https://github.com/darioush
* Arthur Gautier gtid https://github.com/baloo

Thanks to GetResponse for their support

Licence
=======
Copyright 2012-2014 Julien Duponchelle

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


