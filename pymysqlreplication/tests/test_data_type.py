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
    def test_decimal(self):
        pass

    @unittest.skip("Not implemented yet")
    def test_tiny(self):
        pass

    @unittest.skip("Not implemented yet")
    def test_short(self):
        pass

    def test_long(self):
        create_query = "CREATE TABLE test (id INT NOT NULL)"
        insert_query = "INSERT INTO test VALUES(1)"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.rows[0]["values"][0], 1)   

    @unittest.skip("Not implemented yet")
    def test_float(self):
        pass

    @unittest.skip("Not implemented yet")
    def test_double(self):
        pass

    @unittest.skip("Not implemented yet")
    def test_timestamp(self):
        pass

    @unittest.skip("Not implemented yet")
    def test_longlong(self):
        pass

    @unittest.skip("Not implemented yet")
    def test_int24(self):
        pass

    @unittest.skip("Not implemented yet")
    def test_date(self):
        pass

    @unittest.skip("Not implemented yet")
    def test_time(self):
        pass

    @unittest.skip("Not implemented yet")
    def test_datetime(self):
        pass

    @unittest.skip("Not implemented yet")
    def test_year(self):
        pass

    @unittest.skip("Not implemented yet")
    def test_newdate(self):
        pass

    @unittest.skip("Not implemented yet")
    def test_varchar(self):
        pass

    @unittest.skip("Not implemented yet")
    def test_bit(self):
        pass
            
    @unittest.skip("Not implemented yet")
    def test_newdate(self):
        pass

    @unittest.skip("Not implemented yet")
    def test_newdecimal(self):
        pass

    @unittest.skip("Not implemented yet")
    def test_enum(self):
        pass
     
    @unittest.skip("Not implemented yet")
    def test_set(self):
        pass

    @unittest.skip("Not implemented yet")
    def test_tiny_blob(self):
        pass

    @unittest.skip("Not implemented yet")
    def test_medium_blob(self):
        pass

    @unittest.skip("Not implemented yet")
    def test_long_blob(self):
        pass

    @unittest.skip("Not implemented yet")
    def test_blob(self):
        pass

    def test_var_string(self):
        create_query = "CREATE TABLE test (test VARCHAR(255))"
        insert_query = "INSERT INTO test VALUES('Hello')"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.rows[0]["values"][0], 'Hello')   
     
    @unittest.skip("Not implemented yet")
    def test_string(self):
        pass

    @unittest.skip("Not implemented yet")
    def test_geometry(self):
        pass
     

__all__ = ["TestDataType"]

if __name__ == "__main__":
    import unittest
    unittest.main()
