import base
from pymysqlreplication.event import *

class TestBinLogStreamReader(base.PyMySQLReplicationTestCase):
    def test_read_query_event(self):
        query = "CREATE TABLE test (id INT NOT NULL AUTO_INCREMENT, data VARCHAR (50) NOT NULL, PRIMARY KEY (id))"
        self.execute(query)

        #RotateEvent
        self.stream.fetchone()
        #FormatDescription
        self.stream.fetchone()

        event = self.stream.fetchone()
        self.assertIsInstance(event.event, BinLogQueryEvent)
        self.assertEqual(event.event.query, query)

__all__ = ["TestBinLogStreamReader"]

if __name__ == "__main__":
    import unittest
    unittest.main()
