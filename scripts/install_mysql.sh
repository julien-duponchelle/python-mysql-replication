#!/usr/bin/env bash

set -x

# Remove old mysql version
/etc/init.d/mysql stop || true
apt-get remove mysql-common mysql-server-5.5 mysql-server-core-5.5 mysql-client-5.5 mysql-client-core-5.5
apt-get autoremove

VERSION=$1

docker pull percona:$VERSION

# Cleanup old mysql datas
rm -rf /var/ramfs/mysql/
rm -rf /var/ramfs/mysql-ctl/
rm -rf /var/ramfs/mysql8/
mkdir /var/ramfs/mysql/
mkdir /var/ramfs/mysql-ctl/
mkdir /var/ramfs/mysql8/
chmod 777 /var/ramfs/mysql/
chmod 777 /var/ramfs/mysql-ctl/
chmod 777 /var/ramfs/mysql8/
rm -rf /var/run/mysqld/
mkdir /var/run/mysqld/
chmod 777 /var/run/mysqld/

OPTIONS=""
# Replication
OPTIONS="$OPTIONS --log_bin=mysql-bin"
OPTIONS="$OPTIONS --binlog-format=row"
# Gtid
OPTIONS="$OPTIONS --log_slave_updates"
OPTIONS="$OPTIONS --gtid_mode=ON"
OPTIONS="$OPTIONS --enforce-gtid-consistency=ON"

MASTER_OPTIONS="$OPTIONS --server-id=1"
MASTER_OPTIONS="$MASTER_OPTIONS --datadir=/var/ramfs/mysql/"
MASTER_OPTIONS="$MASTER_OPTIONS --socket=/var/run/mysqld/mysqld.sock"

docker run --publish 3306:3306 \
	-d --name master \
	-e MYSQL_ALLOW_EMPTY_PASSWORD=yes\
	-v /var/ramfs/mysql/:/var/ramfs/mysql/\
	percona:$VERSION\
	$MASTER_OPTIONS
#	-v /var/run/mysqld/:/var/run/mysqld/\

CTL_OPTIONS="$OPTIONS --server-id=2"
CTL_OPTIONS="$CTL_OPTIONS --socket=/var/run/mysqld/mysqld-ctl.sock"
CTL_OPTIONS="$CTL_OPTIONS --datadir=/var/ramfs/mysql-ctl/"
CTL_OPTIONS="$CTL_OPTIONS --pid-file=/var/lib/mysql/mysql-ctl.pid"

docker run --publish 3307:3306 \
	-d --name ctl \
	-e MYSQL_ALLOW_EMPTY_PASSWORD=yes\
	-v /var/ramfs/mysql-ctl/:/var/ramfs/mysql-ctl/\
	percona:$VERSION\
	$CTL_OPTIONS
#	-v /var/run/mysqld/:/var/run/mysqld/\

EIGHT_OPTIONS="$OPTIONS --server-id=3"
EIGHT_OPTIONS="$EIGHT_OPTIONS --socket=/var/run/mysqld/mysqld8.sock"
EIGHT_OPTIONS="$EIGHT_OPTIONS --datadir=/var/ramfs/mysql8/"
EIGHT_OPTIONS="$EIGHT_OPTIONS --pid-file=/var/lib/mysql/mysql8.pid"

docker run --publish 3308:3306 \
	-d --name eight \
	-e MYSQL_ALLOW_EMPTY_PASSWORD=yes\
	-v /var/ramfs/mysql8/:/var/ramfs/mysql8/\
	percona:8.0\
	$EIGHT_OPTIONS

for i in $(seq 0 40); do
	sleep 1;
	mysql -u root --host=127.0.0.1 --port=3306 -e 'SELECT VERSION();'
	if [ $? -eq 0 ]; then
		break 2;
	fi
done

for i in $(seq 0 40); do
	sleep 1;
	mysql -u root --host=127.0.0.1 --port=3307 -e 'SELECT VERSION();'
	if [ $? -eq 0 ]; then
		break 2;
	fi
done

for i in $(seq 0 40); do
	sleep 1;
	mysql -u root --host=127.0.0.1 --port=3308 -e 'SELECT VERSION();'
	if [ $? -eq 0 ]; then
		break 2;
	fi
done

docker logs master
docker logs ctl
docker logs eight

mysql -u root --host=127.0.0.1 --port=3306 -e 'CREATE DATABASE pymysqlreplication_test;'
mysql -u root --host=127.0.0.1 --port=3307 -e "CREATE DATABASE pymysqlreplication_test;"
mysql -u root --host=127.0.0.1 --port=3308 -e "CREATE DATABASE pymysqlreplication_test;"
