from pymysqlreplication.tests import base
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.event import *
from pymysqlreplication.constants.BINLOG import *
from pymysqlreplication.row_event import *

from decimal import Decimal
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


    def test_decimal(self):
        create_query = "CREATE TABLE test (test DECIMAL(2,1))"
        insert_query = "INSERT INTO test VALUES(4.2)"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.columns[0].precision, 2) 
        self.assertEqual(event.columns[0].decimals, 1) 
        self.assertEqual(event.rows[0]["values"]["test"], Decimal("4.2")) 


    def test_decimal_long_values(self):
        create_query = "CREATE TABLE test (\
            test DECIMAL(20,10) \
        )"
        insert_query = "INSERT INTO test VALUES(42000.123456)"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.rows[0]["values"]["test"], Decimal("42000.123456"))

    def test_decimal_negative_values(self):
        create_query = "CREATE TABLE test (\
            test DECIMAL(20,10) \
        )"
        insert_query = "INSERT INTO test VALUES(-42000.123456)"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.rows[0]["values"]["test"], Decimal("-42000.123456"))

    def test_decimal_two_values(self):
        create_query = "CREATE TABLE test (\
            test DECIMAL(2,1), \
            test2 DECIMAL(20,10) \
        )"
        insert_query = "INSERT INTO test VALUES(4.2, 42000.123456)"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.rows[0]["values"]["test"], Decimal("4.2"))
        self.assertEqual(event.rows[0]["values"]["test2"], Decimal("42000.123456")) 

    def test_tiny(self):
        create_query = "CREATE TABLE test (id TINYINT UNSIGNED NOT NULL, test TINYINT)"
        insert_query = "INSERT INTO test VALUES(255, -128)"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.rows[0]["values"]["id"], 255)
        self.assertEqual(event.rows[0]["values"]["test"], -128)

    def test_short(self):
        create_query = "CREATE TABLE test (id SMALLINT UNSIGNED NOT NULL, test SMALLINT)"
        insert_query = "INSERT INTO test VALUES(65535, -32768)"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.rows[0]["values"]["id"], 65535)
        self.assertEqual(event.rows[0]["values"]["test"], -32768)

    def test_long(self):
        create_query = "CREATE TABLE test (id INT UNSIGNED NOT NULL, test INT)"
        insert_query = "INSERT INTO test VALUES(4294967295, -2147483648)"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.rows[0]["values"]["id"], 4294967295)
        self.assertEqual(event.rows[0]["values"]["test"], -2147483648)

    def test_float(self):
        create_query = "CREATE TABLE test (id FLOAT NOT NULL, test FLOAT)"
        insert_query = "INSERT INTO test VALUES(42.42, -84.84)"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(round(event.rows[0]["values"]["id"], 2), 42.42)
        self.assertEqual(round(event.rows[0]["values"]["test"],2 ), -84.84)

    def test_double(self):
        create_query = "CREATE TABLE test (id DOUBLE NOT NULL, test DOUBLE)"
        insert_query = "INSERT INTO test VALUES(42.42, -84.84)"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(round(event.rows[0]["values"]["id"], 2), 42.42)
        self.assertEqual(round(event.rows[0]["values"]["test"],2 ), -84.84)

    @unittest.skip("Not implemented yet")
    def test_timestamp(self):
        pass

    @unittest.skip("Not implemented yet")
    def test_longlong(self):
        pass

    def test_int24(self):
        create_query = "CREATE TABLE test (id MEDIUMINT UNSIGNED NOT NULL, test MEDIUMINT, test2 MEDIUMINT)"
        insert_query = "INSERT INTO test VALUES(16777215, 8388607, -8388608)"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.rows[0]["values"]["id"], 16777215)
        self.assertEqual(event.rows[0]["values"]["test"], 8388607)
        self.assertEqual(event.rows[0]["values"]["test2"], -8388608)
        

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

    def test_varchar(self):
        create_query = "CREATE TABLE test (test VARCHAR(242)) CHARACTER SET latin1 COLLATE latin1_bin;"
        insert_query = "INSERT INTO test VALUES('Hello')"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.rows[0]["values"]["test"], 'Hello')
        self.assertEqual(event.columns[0].max_length, 242)

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

    @unittest.skip("Not implemented yet")
    def test_var_string(self):
        pass
     
    def test_string(self):
        create_query = "CREATE TABLE test (test CHAR(255)) CHARACTER SET latin1 COLLATE latin1_bin;"
        insert_query = "INSERT INTO test VALUES('Hello')"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.rows[0]["values"]["test"], 'Hello') 

    @unittest.skip("Not implemented yet")
    def test_geometry(self):
        pass

    @unittest.skip("Not implemented yet")
    def test_null(self):
        pass

    @unittest.skip("Not implemented yet")
    def test_encoding(self):
        pass

__all__ = ["TestDataType"]

if __name__ == "__main__":
    import unittest
    unittest.main()
