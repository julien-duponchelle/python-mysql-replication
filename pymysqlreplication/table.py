# -*- coding: utf-8 -*-


class Table(object):
    def __init__(self, column_schemas, table_id, schema, table, columns, primary_key = None):
        if primary_key is None:
            primary_key = [c.data["name"] for c in columns if c.data["is_primary"]]
            if len(primary_key) == 0:
                primary_key = ''
            elif len(primary_key) == 1:
                primary_key, = primary_key
            else:
                primary_key = tuple(primary_key)

        self.data = {
            "column_schemas": column_schemas,
            "table_id": table_id,
            "schema": schema,
            "table": table,
            "columns": columns,
            "primary_key": primary_key
        }

    def __getattr__(self, item):
        try:
            return self.data[item]
        except KeyError:
            raise AttributeError

    def __eq__(self, other):
        return self.data == other.data

    def __ne__(self, other):
        return self.__eq__(other)

    def serializable_data(self):
        return self.data
