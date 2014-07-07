# -*- coding: utf-8 -*-


class Table(object):
    def __init__(self, column_schemas, table_id, schema, table, columns):
        self.data = {
            "column_schemas": column_schemas,
            "table_id": table_id,
            "schema": schema,
            "table": table,
            "columns": columns,
            "primary_keys": [c.data["name"] for c in columns
                             if c.data["is_primary"]]
        }

    def __getattr__(self, item):
        if item in self.data:
            return self.data[item]
        else:
            raise AttributeError

    def __eq__(self, other):
        return self.data == other.data

    def __ne__(self, other):
        return self.__eq__(other)

    def serializable_data(self):
        return self.data
