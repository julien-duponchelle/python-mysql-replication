#############
Developement
#############

Contributions
=============

You can report issues and contribute to the project on: https://github.com/noplay/python-mysql-replication

The standard way to contribute code to the project is to fork the Github
project and open a pull request with your changes:
https://github.com/noplay/python-mysql-replication

Don't hesitate to open an issue with what you want to changes if
you want to discuss about it before coding.


Tests
======

When it's possible we have an unit test.

*pymysqlreplication/tests/* contains the test suite. The test suite
use the standard *unittest* Python module.

**Be carefull** tests will reset the binary log of your MySQL server.

Make sure you have the following configuration set in your mysql config file (usually my.cnf on development env):

::

    log-bin=mysql-bin
    server-id=1
    binlog-format    = row #Very important if you want to receive write, update and delete row events
    gtid_mode=ON
    log-slave_updates=true
    enforce_gtid_consistency


To run tests:

::

    python setup.py test


Each pull request is tested on Travis CI:
https://travis-ci.org/noplay/python-mysql-replication

Build the documentation
========================

The documentation is available in docs folder. You can
build it using Sphinx:

::

    cd docs
    pip install sphinx
    make html

