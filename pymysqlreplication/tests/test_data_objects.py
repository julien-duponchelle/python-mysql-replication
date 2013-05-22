import unittest

from pymysqlreplication.column import Column
from pymysqlreplication.table import Table

from pymysqlreplication.tests import base

__all__ = ["TestDataObjects"]


class TestDataObjects(base.PyMySQLReplicationTestCase):
    def test_column(self):
        col = Column(1,
                     {"COLUMN_NAME": "test",
                      "COLLATION_NAME": "utf8_general_ci",
                      "CHARACTER_SET_NAME": "UTF8",
                      "COLUMN_COMMENT": "",
                      "COLUMN_TYPE": "tinyint(2)"},
                     None)

        serialized = col.serializable_data()
        self.assertIn("type", serialized)
        self.assertIn("name", serialized)
        self.assertIn("collation_name", serialized)
        self.assertIn("character_set_name", serialized)
        self.assertIn("comment", serialized)
        self.assertIn("unsigned", serialized)
        self.assertIn("type_is_bool", serialized)

        self.assertEqual(col, Column(**serialized))

    def test_table(self):
        tbl = Table(1, "test_schema", "test_table", [], [])

        serialized = tbl.serializable_data()
        self.assertIn("table_id", serialized)
        self.assertIn("schema", serialized)
        self.assertIn("table", serialized)
        self.assertIn("columns", serialized)
        self.assertIn("column_schemas", serialized)

        self.assertEqual(tbl, Table(**serialized))


if __name__ == "__main__":
    unittest.main()
