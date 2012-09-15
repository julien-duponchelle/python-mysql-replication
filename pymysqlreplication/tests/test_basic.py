import base
from pymysqlreplication import BinLogStreamReader

class TestBinLogStreamReader(base.PyMySQLReplicationTestCase):
    def test_open_stream(self):
        """ test opening stream"""
        stream = BinLogStreamReader(self.conn_test)


__all__ = ["TestBinLogStreamReader"]

if __name__ == "__main__":
    import unittest
    unittest.main()
