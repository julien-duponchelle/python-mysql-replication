###########
Limitations
###########

GEOMETRY
=========
GEOMETRY field is not decoded you will get the raw data.

binlog_row_image
================
Only [binlog_row_image=full](http://dev.mysql.com/doc/refman/5.6/en/replication-options-binary-log.html#sysvar_binlog_row_image) is supported (it's the default value).

BOOLEAN and BOOL
================
Boolean is returned as TINYINT(1) because it's the reality.

http://dev.mysql.com/doc/refman/5.6/en/numeric-type-overview.html

Our discussion about it:
https://github.com/noplay/python-mysql-replication/pull/16
