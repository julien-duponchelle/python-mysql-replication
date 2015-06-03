# -*- coding: utf-8 -*-

import pymysql
import unittest
import copy
from pymysqlreplication import BinLogStreamReader
import os
import sys

(major, minor, _, _, _) = sys.version_info
if (major, minor) < (2, 7):
    import unittest2
    base = unittest2.TestCase
else:
    base = unittest.TestCase


class PyMySQLReplicationTestCase(base):
    def ignoredEvents(self):
        return []

    def setUp(self):
        self.database = {
            "host": "localhost",
            "user": "root",
            "passwd": "",
            "use_unicode": True,
            "charset": "utf8",
            "db": "pymysqlreplication_test"
        }
        if os.getenv("TRAVIS") is not None:
            self.database["user"] = "travis"

        self.conn_control = None
        db = copy.copy(self.database)
        db["db"] = None
        self.connect_conn_control(db)
        self.execute("DROP DATABASE IF EXISTS pymysqlreplication_test")
        self.execute("CREATE DATABASE pymysqlreplication_test")
        db = copy.copy(self.database)
        self.connect_conn_control(db)
        self.stream = None
        self.resetBinLog()
        self.isMySQL56AndMore()

    def getMySQLVersion(self):
        """Return the MySQL version of the server
        If version is 5.6.10-log the result is 5.6.10
        """
        return self.execute("SELECT VERSION()").fetchone()[0].split('-')[0]

    def isMySQL56AndMore(self):
        version = float(self.getMySQLVersion().rsplit('.', 1)[0])
        if version >= 5.6:
            return True
        return False

    @property
    def supportsGTID(self):
        if not self.isMySQL56AndMore():
            return False
        return self.execute("SELECT @@global.gtid_mode ").fetchone()[0] == "ON"

    def connect_conn_control(self, db):
        if self.conn_control is not None:
            self.conn_control.close()
        self.conn_control = pymysql.connect(**db)

    def tearDown(self):
        self.conn_control.close()
        self.conn_control = None
        self.stream.close()
        self.stream = None

    def execute(self, query):
        c = self.conn_control.cursor()
        c.execute(query)
        return c

    def resetBinLog(self):
        self.execute("RESET MASTER")
        if self.stream is not None:
            self.stream.close()
        self.stream = BinLogStreamReader(self.database, server_id=1024,
                                         ignored_events=self.ignoredEvents())
