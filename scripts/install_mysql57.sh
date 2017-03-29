#!/usr/bin/env bash

set -x

# Remove old mysql version
/etc/init.d/mysql stop || true
apt-get remove mysql-common mysql-server-5.5 mysql-server-core-5.5 mysql-client-5.5 mysql-client-core-5.5
apt-get autoremove

# Config
sed -i'' 's/table_cache/table_open_cache/' /etc/mysql/my.cnf
sed -i'' 's/log_slow_queries/slow_query_log/' /etc/mysql/my.cnf

# Install new mysql version
echo deb http://repo.mysql.com/apt/ubuntu/ trusty mysql-5.7 | tee /etc/apt/sources.list.d/mysql.list
apt-key add .mysql/dev.mysql.com.gpg.key
apt-get update
env DEBIAN_FRONTEND=noninteractive apt-get install -o Dpkg::Options::='--force-confold' -q -y mysql-server mysql-client

# Cleanup old mysql datas
rm -rf /var/ramfs/mysql/
rm -rf /var/ramfs/mysql-ctl/
mkdir /var/ramfs/mysql/
mkdir /var/ramfs/mysql-ctl/
chown -R mysql /var/ramfs/mysql/
chown -R mysql /var/ramfs/mysql-ctl/

# Config
echo '[mysqld]'            | tee /etc/mysql/conf.d/replication.cnf
echo 'log-bin=mysql-bin'   | tee -a /etc/mysql/conf.d/replication.cnf
echo 'server-id=1'         | tee -a /etc/mysql/conf.d/replication.cnf
echo 'binlog-format = row' | tee -a /etc/mysql/conf.d/replication.cnf

/etc/init.d/mysql stop || true

# Install new datas
mysql_install_db --defaults-file=/etc/mysql/my.cnf --basedir=/usr --datadir=/var/ramfs/mysql-ctl --user=mysql --insecure --verbose
mysql_install_db --defaults-file=/etc/mysql/my.cnf --basedir=/usr --datadir=/var/ramfs/mysql --insecure --user=mysql --verbose

# Enable GTID
echo '[mysqld]'                       | tee /etc/mysql/conf.d/gtid.cnf
echo 'gtid_mode=ON'                   | tee -a /etc/mysql/conf.d/gtid.cnf
echo 'enforce_gtid_consistency'       | tee -a /etc/mysql/conf.d/gtid.cnf
echo 'binlog_format=ROW'              | tee -a /etc/mysql/conf.d/gtid.cnf
echo 'log_slave_updates'              | tee -a /etc/mysql/conf.d/gtid.cnf

# Start mysql (avoid errors to have logs)
/etc/init.d/mysql start || true
mysql_upgrade
/etc/init.d/mysql restart || true
tail -1000 /var/log/syslog
nohup mysqld_safe --log-bin=mysql-ctl-bin.log --server-id 2 --binlog-format=row --gtid_mode=on --enforce-gtid-consistency=on --log_slave-updates -P 3307 --socket=/var/run/mysqld/mysqld-ctl.sock --datadir=/var/ramfs/mysql-ctl --pid-file=/var/lib/mysql/mysql-ctl.pid &
#Give it time to start
sleep 5
tail -1000 nohup.out

mysql --version
mysql -e 'SELECT VERSION();'
mysql -u root -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'127.0.0.1'; FLUSH PRIVILEGES;"
mysql -u root --port=3307 --socket=/var/run/mysqld/mysqld-ctl.sock -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost'; FLUSH PRIVILEGES;"

mysql -e 'CREATE DATABASE pymysqlreplication_test;'
mysql -u root --port=3307 --socket=/var/run/mysqld/mysqld-ctl.sock -e "CREATE DATABASE pymysqlreplication_test;"
