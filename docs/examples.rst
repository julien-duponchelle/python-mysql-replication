########
Examples
########

You can found a list of working examples here: https://github.com/noplay/python-mysql-replication/tree/master/examples

PREREQUISITES

The user, you plan to use for the BinaryLogClient, must have REPLICATION SLAVE privilege. To get binlog filename and position, he must be granted at least one of REPLICATION CLIENT or SUPER as well. To get table info of mysql server, he also need SELECT privilege on information_schema.COLUMNS.
We suggest grant below privileges to the user:

:command:`GRANT REPLICATION SLAVE, REPLICATION CLIENT, SELECT ON *.* TO 'user'@'host'`
