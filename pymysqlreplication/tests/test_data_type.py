import base
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.event import *
from pymysqlreplication.constants.BINLOG import *
import time
import unittest

class TestDataType(base.PyMySQLReplicationTestCase):
    def create_and_insert_value(self, create_query, insert_query):
        self.execute(create_query)
        self.execute(insert_query)
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
        self.assertIsInstance(event, TableMapEvent)

        event = self.stream.fetchone()
        self.assertEqual(event.event_type, WRITE_ROWS_EVENT)        
        self.assertIsInstance(event, WriteRowsEvent)
        return event

    @unittest.skip("Not implemented yet")
    def test_decimal():
        pass

    @unittest.skip("Not implemented yet")
    def test_tiny():
        pass

    @unittest.skip("Not implemented yet")
    def test_short():
        pass

    def test_long(self):
        create_query = "CREATE TABLE test (id INT NOT NULL)"
        insert_query = "INSERT INTO test VALUES(1)"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.rows[0]["values"][0], 1)   

    @unittest.skip("Not implemented yet")
    def test_float():
        pass

    @unittest.skip("Not implemented yet")
    def test_double():
        pass

    @unittest.skip("Not implemented yet")
    def test_timestamp():
        pass

    @unittest.skip("Not implemented yet")
    def test_longlong():
        pass

    @unittest.skip("Not implemented yet")
    def test_int24():
        pass

    @unittest.skip("Not implemented yet")
    def test_date():
        pass

    @unittest.skip("Not implemented yet")
    def test_time():
        pass

    @unittest.skip("Not implemented yet")
    def test_datetime():
        pass

    @unittest.skip("Not implemented yet")
    def test_year():
        pass

    @unittest.skip("Not implemented yet")
    def test_newdate():
        pass

    @unittest.skip("Not implemented yet")
    def test_varchar():
        pass

    @unittest.skip("Not implemented yet")
    def test_bit():
        pass
            
    @unittest.skip("Not implemented yet")
    def test_newdate():
        pass

    @unittest.skip("Not implemented yet")
    def test_newdecimal():
        pass

    @unittest.skip("Not implemented yet")
    def test_enum():
        pass
     
    @unittest.skip("Not implemented yet")
    def test_set():
        pass

    @unittest.skip("Not implemented yet")
    def test_tiny_blob():
        pass

    @unittest.skip("Not implemented yet")
    def test_medium_blob():
        pass

    @unittest.skip("Not implemented yet")
    def test_long_blob():
        pass

    @unittest.skip("Not implemented yet")
    def test_blob():
        pass

    @unittest.skip("Not implemented yet")
    def test_var_string():
        pass
     
    @unittest.skip("Not implemented yet")
    def test_string():
        pass

    @unittest.skip("Not implemented yet")
    def test_geometry():
        pass
     

__all__ = ["TestDataType"]

if __name__ == "__main__":
    import unittest
    unittest.main()
