import copy
import pymysql


class MetadataAdapter(object):
    def __init__(self, connection_settings):
        self.connection_settings = copy.deepcopy(connection_settings)
        self.connection_settings["db"] = "information_schema"
        self.connection_settings["cursorclass"] = pymysql.cursors.DictCursor
        self.connection = None

    def get_charset(self):
        self.get_cursor()

        return self.connection.charset

    def get_table_information(self, schema, table):
        for i in range(1, 3):
            try:
                cursor = self.get_cursor()
                cursor.execute("""
                    SELECT
                        COLUMN_NAME, COLLATION_NAME, CHARACTER_SET_NAME,
                        COLUMN_COMMENT, COLUMN_TYPE
                    FROM
                        columns
                    WHERE
                        table_schema = %s AND table_name = %s
                    """, (schema, table))

                return cursor.fetchall()
            except pymysql.OperationalError as error:
                code, message = error.args
                # 2013: Connection Lost
                if code == 2013:
                    self.connection = None
                    continue
                else:
                    raise error

    def get_cursor(self):
        if self.connection is None:
            self.connection = pymysql.connect(**self.connection_settings)

        return self.connection.cursor()

