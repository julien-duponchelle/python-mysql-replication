#!/usr/bin/env bash

mkdir $HOME/bins
mkdir $HOME/sandboxes

cd $HOME/bins
if [ ! -f "5.7.14" ]; then
  echo 'Downloading MySQL 5.7.14'
  curl -O http://cdn.mysql.com/Downloads/MySQL-5.7/mysql-5.7.14-linux-glibc2.5-x86_64.tar.gz
  tar xfz mysql-5.7.14-linux-glibc2.5-x86_64.tar.gz
  ln -s mysql-5.7.14-linux-glibc2.5-x86_64 5.7.14
fi

export SANDBOX_BINARY=$HOME/bins
export SANDBOX_HOME=$HOME/sandboxes
make_sandbox 5.7.14 -- --no_confirm --no_run

CNF=$SANDBOX_HOME/msb_5_7_14/my.sandbox.cnf

echo 'log-bin=mysql-bin'         | tee -a $CNF
echo 'server-id=1'               | tee -a $CNF
echo 'binlog-format =row'        | tee -a $CNF
echo 'gtid_mode=ON'              | tee -a $CNF
echo 'enforce_gtid_consistency'  | tee -a $CNF
echo 'log_slave_updates'         | tee -a $CNF

cat $CNF

$SANDBOX_HOME/msb_5_7_14/start

MYSQL=$SANDBOX_BINARY/5.7.14/bin/mysql
$MYSQL --version
$MYSQL -e 'SELECT VERSION();'
# $MYSQL -u root -e "GRANT ALL PRIVILEGES ON *.* TO ''@'localhost';"
$MYSQL -e 'CREATE DATABASE pymysqlreplication_test;'
$MYSQL -e 'show variables;'
