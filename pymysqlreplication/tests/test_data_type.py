from pymysqlreplication.tests import base
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.event import *
from pymysqlreplication.constants.BINLOG import *
from pymysqlreplication.row_event import *

from decimal import Decimal
import datetime
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

    def test_timestamp(self):
        create_query = "CREATE TABLE test (test TIMESTAMP);"
        insert_query = "INSERT INTO test VALUES('1984-12-03 12:33:07')"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.rows[0]["values"]["test"], datetime.datetime(1984, 12, 3, 12, 33, 7)) 

    def test_longlong(self):
        create_query = "CREATE TABLE test (id BIGINT UNSIGNED NOT NULL, test BIGINT)"
        insert_query = "INSERT INTO test VALUES(18446744073709551615, -9223372036854775808)"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.rows[0]["values"]["id"], 18446744073709551615)
        self.assertEqual(event.rows[0]["values"]["test"], -9223372036854775808)

    def test_int24(self):
        create_query = "CREATE TABLE test (id MEDIUMINT UNSIGNED NOT NULL, test MEDIUMINT, test2 MEDIUMINT)"
        insert_query = "INSERT INTO test VALUES(16777215, 8388607, -8388608)"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.rows[0]["values"]["id"], 16777215)
        self.assertEqual(event.rows[0]["values"]["test"], 8388607)
        self.assertEqual(event.rows[0]["values"]["test2"], -8388608)

    def test_date(self):
        create_query = "CREATE TABLE test (test DATE);"
        insert_query = "INSERT INTO test VALUES('1984-12-03')"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.rows[0]["values"]["test"], datetime.date(1984, 12, 3)) 

    def test_time(self):
        create_query = "CREATE TABLE test (test TIME);"
        insert_query = "INSERT INTO test VALUES('12:33:07')"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.rows[0]["values"]["test"], datetime.time(12, 33, 7)) 

    def test_datetime(self):
        create_query = "CREATE TABLE test (test DATETIME);"
        insert_query = "INSERT INTO test VALUES('1984-12-03 12:33:07')"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.rows[0]["values"]["test"], datetime.datetime(1984, 12, 3, 12, 33, 7)) 

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

    def test_tiny_blob(self):
        create_query = "CREATE TABLE test (test TINYBLOB, test2 TINYTEXT) CHARACTER SET latin1 COLLATE latin1_bin;"
        insert_query = "INSERT INTO test VALUES('Hello', 'World')"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.rows[0]["values"]["test"], 'Hello') 
        self.assertEqual(event.rows[0]["values"]["test2"], 'World') 

    def test_medium_blob(self):
        create_query = "CREATE TABLE test (test MEDIUMBLOB, test2 MEDIUMTEXT) CHARACTER SET latin1 COLLATE latin1_bin;"
        insert_query = "INSERT INTO test VALUES('Hello', 'World')"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.rows[0]["values"]["test"], 'Hello') 
        self.assertEqual(event.rows[0]["values"]["test2"], 'World') 

    def test_long_blob(self):
        create_query = "CREATE TABLE test (test LONGBLOB, test2 LONGTEXT) CHARACTER SET latin1 COLLATE latin1_bin;"
        insert_query = "INSERT INTO test VALUES('Hello', 'World')"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.rows[0]["values"]["test"], 'Hello') 
        self.assertEqual(event.rows[0]["values"]["test2"], 'World') 

    def test_blob(self):
        create_query = "CREATE TABLE test (test BLOB, test2 TEXT) CHARACTER SET latin1 COLLATE latin1_bin;"
        insert_query = "INSERT INTO test VALUES('Hello', 'World')"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.rows[0]["values"]["test"], 'Hello') 
        self.assertEqual(event.rows[0]["values"]["test2"], 'World') 

    @unittest.skip("Not implemented yet")
    def test_var_string(self):
        pass
     
    def test_string(self):
        create_query = "CREATE TABLE test (test CHAR(12)) CHARACTER SET latin1 COLLATE latin1_bin;"
        insert_query = "INSERT INTO test VALUES('Hello')"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.rows[0]["values"]["test"], 'Hello') 

    @unittest.skip("Not implemented yet")
    def test_geometry(self):
        pass

    def test_null(self):
        create_query = "CREATE TABLE test ( \
            test TINYINT NULL DEFAULT NULL, \
            test2 TINYINT NULL DEFAULT NULL, \
            test3 TINYINT NULL DEFAULT NULL, \
            test4 TINYINT NULL DEFAULT NULL, \
            test5 TINYINT NULL DEFAULT NULL, \
            test6 TINYINT NULL DEFAULT NULL, \
            test7 TINYINT NULL DEFAULT NULL, \
            test8 TINYINT NULL DEFAULT NULL, \
            test9 TINYINT NULL DEFAULT NULL, \
            test10 TINYINT NULL DEFAULT NULL, \
            test11 TINYINT NULL DEFAULT NULL, \
            test12 TINYINT NULL DEFAULT NULL, \
            test13 TINYINT NULL DEFAULT NULL, \
            test14 TINYINT NULL DEFAULT NULL, \
            test15 TINYINT NULL DEFAULT NULL, \
            test16 TINYINT NULL DEFAULT NULL, \
            test17 TINYINT NULL DEFAULT NULL, \
            test18 TINYINT NULL DEFAULT NULL, \
            test19 TINYINT NULL DEFAULT NULL, \
            test20 TINYINT NULL DEFAULT NULL\
            )"
        insert_query = "INSERT INTO test (test, test2, test3, test7, test20) VALUES(NULL, -128, NULL, 42, 84)"
        event = self.create_and_insert_value(create_query, insert_query)
        self.assertEqual(event.rows[0]["values"]["test"], None)
        self.assertEqual(event.rows[0]["values"]["test2"], -128)
        self.assertEqual(event.rows[0]["values"]["test3"], None)        
        self.assertEqual(event.rows[0]["values"]["test7"], 42)
        self.assertEqual(event.rows[0]["values"]["test20"], 84)        

    @unittest.skip("Not implemented yet")
    def test_encoding(self):
        pass

__all__ = ["TestDataType"]

if __name__ == "__main__":
    import unittest
    unittest.main()
