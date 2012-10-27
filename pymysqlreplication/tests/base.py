import pymysql
import unittest
import copy
from pymysqlreplication import BinLogStreamReader

class PyMySQLReplicationTestCase(unittest.TestCase):
    '''Test the module. Be carefull it will reset your MySQL server'''
    database =  {"host":"localhost",
        "user":"root",
        "passwd":"",
        "use_unicode": True,
        "charset": "utf8",
        "db": "pymysqlreplication_test"
    }

    def setUp(self):
        self.conn_control = pymysql.connect(**self.database)
        self.execute("DROP DATABASE IF EXISTS pymysqlreplication_test")
        self.execute("CREATE DATABASE pymysqlreplication_test")
        db = copy.copy(self.database)
        self.connect_conn_control(db)
        self.stream = None
        self.resetBinLog()

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

    def resetBinLog(self):
        self.execute("RESET MASTER")
        if self.stream is not None:
            self.stream.close()
        self.stream = BinLogStreamReader(connection_settings = self.database)

