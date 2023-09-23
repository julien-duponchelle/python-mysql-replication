import unittest
from pymysqlreplication.column import Column
from pymysqlreplication.table import Table
from pymysqlreplication.event import GtidEvent

from pymysqlreplication.tests import base

__all__ = ["TestDataObjects"]


class TestDataObjects(base.PyMySQLReplicationTestCase):
    def ignoredEvents(self):
        return [GtidEvent]

    def test_column_serializable(self):
        col = Column(1, None)

        serialized = col.serializable_data()
        self.assertIn("type", serialized)
        self.assertEqual(col, Column(**serialized))

    def test_table(self):
        tbl = Table(1, "test_schema", "test_table", [], [])

        serialized = tbl.serializable_data()
        self.assertIn("table_id", serialized)
        self.assertIn("schema", serialized)
        self.assertIn("table", serialized)
        self.assertIn("columns", serialized)

        self.assertEqual(tbl, Table(**serialized))


if __name__ == "__main__":
    unittest.main()
