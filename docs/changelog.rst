##########
Changelog
##########

0.3 07/07/2014
===============
* use NotImplementedEvent instead of raising an Exception
* Python 3 fix
* Add 2006 to Mysql expected error codes

0.2 13/10/2013
===============
* pymysql 0.6 support
* fix smallint24
* fix new decimal support
* TINYINT(1) to bool mapping
* change names of events to V2 from default
* Fix broken "dates" - zero years..
* add support for NULL_EVENT, INTVAR_EVENT and GTID_LOG_EVENT
* Skip invalid packets
* Display log pos inside events dump
* Handle utf8 name for queries

0.1 01/05/2013
===============
First public version
