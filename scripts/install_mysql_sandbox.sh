#!/usr/bin/env bash

set -x

apt-get install tree
apt-get install libaio1

curl -O http://www.cpan.org/authors/id/G/GM/GMAX/MySQL-Sandbox-3.1.05.tar.gz
tar xfz MySQL-Sandbox-3.1.05.tar.gz
cd MySQL-Sandbox-3.1.05
perl Makefile.PL
make install

