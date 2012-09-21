import base
from pymysqlreplication.event import *
from pymysqlreplication.constants.BINLOG import *
import time

class TestBinLogStreamReader(base.PyMySQLReplicationTestCase):
    def test_read_query_event(self):
        query = "CREATE TABLE test (id INT NOT NULL AUTO_INCREMENT, data VARCHAR (50) NOT NULL, PRIMARY KEY (id))"
        self.execute(query)

        #RotateEvent
        self.stream.fetchone()
        #FormatDescription
        self.stream.fetchone()

        event = self.stream.fetchone()
        self.assertIsInstance(event.event, QueryEvent)
        self.assertEqual(event.event.query, query)

    def test_write_row_event(self):
        query = "CREATE TABLE test (id INT NOT NULL AUTO_INCREMENT, data VARCHAR (50) NOT NULL, PRIMARY KEY (id))"
        self.execute(query)
        query = "INSERT INTO test (data) VALUES('Hello World')"
        self.execute(query)
        self.execute("COMMIT")

        #RotateEvent
        self.stream.fetchone()
        #FormatDescription
        self.stream.fetchone()
        #QueryEvent for the Create Table
        self.stream.fetchone()

        #QueryEvent for the BEGIN
        self.stream.fetchone()

        event = self.stream.fetchone()
        self.assertIsInstance(event.event, TableMapEvent)

        event = self.stream.fetchone()
        self.assertEqual(event.event_type, WRITE_ROWS_EVENT)        
        self.assertIsInstance(event.event, WriteRowsEvent)
        self.assertEqual(event.event.values[0], 1)        
        self.assertEqual(event.event.values[1], "Hello World")        

    def test_delete_row_event(self):
        query = "CREATE TABLE test (id INT NOT NULL AUTO_INCREMENT, data VARCHAR (50) NOT NULL, PRIMARY KEY (id))"
        self.execute(query)
        query = "INSERT INTO test (data) VALUES('Hello World')"
        self.execute(query)

        self.resetBinLog()
        
        query = "DELETE FROM test WHERE id = 1"
        self.execute(query)
        self.execute("COMMIT")

        #RotateEvent
        self.stream.fetchone()
        #FormatDescription
        self.stream.fetchone()

        #QueryEvent for the BEGIN
        self.stream.fetchone()

        event = self.stream.fetchone()
        self.assertIsInstance(event.event, TableMapEvent)

        event = self.stream.fetchone()
        self.assertEqual(event.event_type, DELETE_ROWS_EVENT)        
        self.assertIsInstance(event.event, DeleteRowsEvent)
        self.assertEqual(event.event.values[0], 1)        
        self.assertEqual(event.event.values[1], "Hello World")   

__all__ = ["TestBinLogStreamReader"]

if __name__ == "__main__":
    import unittest
    unittest.main()
