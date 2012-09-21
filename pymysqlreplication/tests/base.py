import pymysql
import unittest
import copy
from pymysqlreplication import BinLogStreamReader

class PyMySQLReplicationTestCase(unittest.TestCase):
    '''Test the module. Be carefull it will reset your MySQL server'''
    database =  {"host":"localhost","user":"root", "passwd":"","use_unicode": True}

    def setUp(self):
        self.conn_control = pymysql.connect(**self.database)
        self.execute("CREATE DATABASE pymysqlreplication_test")
        db = copy.copy(self.database)
        db["db"] = "pymysqlreplication_test"
        self.conn_control = pymysql.connect(**db)
        self.resetBinLog()

    def tearDown(self):
        self.execute("DROP DATABASE pymysqlreplication_test")
        self.conn_control.close()
        self.conn_test.close()

    def execute(self, query):
        c = self.conn_control.cursor()
        c.execute(query)

    def resetBinLog(self):
        self.execute("RESET MASTER")
        self.conn_test = pymysql.connect(**self.database)
        self.stream = BinLogStreamReader(self.conn_test)

