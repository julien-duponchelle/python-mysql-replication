import struct
import decimal

from .event import BinLogEvent
from pymysql.util import byte2int, int2byte
from pymysql.constants import FIELD_TYPE
from .column import Column


class RowsEvent(BinLogEvent):
    def __init__(self, from_packet, event_size, table_map, ctl_connection):
        super(RowsEvent, self).__init__(from_packet, event_size, table_map, ctl_connection)
        self.__rows = None

        #Header
        self.table_id = self._read_table_id()
        self.flags = struct.unpack('<H', self.packet.read(2))[0]

        #Body
        self.number_of_columns = self.packet.read_length_coded_binary()
        self.columns = self.table_map[self.table_id].columns

        #Aditionnal informations
        self.schema = self.table_map[self.table_id].schema
        self.table = self.table_map[self.table_id].table

    def _read_column_data(self):
        '''Use for WRITE, UPDATE and DELETE events. Return an array of column data'''
        values = {}

        for i in range(0, len(self.columns)):
            column = self.columns[i]
            name = self.table_map[self.table_id].columns[i].name
            unsigned = self.table_map[self.table_id].columns[i].unsigned
            if column.type == FIELD_TYPE.TINY:
                if unsigned:
                    values[name] = struct.unpack("<B", self.packet.read(1))[0]
                else:
                    values[name] = struct.unpack("<b", self.packet.read(1))[0]
            elif column.type == FIELD_TYPE.SHORT:
                if unsigned:
                    values[name] = struct.unpack("<H", self.packet.read(2))[0]
                else:
                    values[name] = struct.unpack("<h", self.packet.read(2))[0]
            elif column.type == FIELD_TYPE.LONG:
                if unsigned:
                    values[name] = struct.unpack("<I", self.packet.read(4))[0]
                else:
                    values[name] = struct.unpack("<i", self.packet.read(4))[0]
            elif column.type == FIELD_TYPE.INT24:
                if unsigned:
                    values[name] = self.packet.read_uint24()                    
                else:
                    values[name] = self.packet.read_int24()
            elif column.type == FIELD_TYPE.FLOAT:
                values[name] = struct.unpack("<f", self.packet.read(4))[0]
            elif column.type == FIELD_TYPE.DOUBLE:
                values[name] = struct.unpack("<d", self.packet.read(8))[0]
            elif column.type == FIELD_TYPE.VARCHAR:
                values[name] = self.packet.read_length_coded_string()
            elif column.type == FIELD_TYPE.STRING:
                values[name] = self.packet.read_length_coded_string()
            elif column.type == FIELD_TYPE.NEWDECIMAL:
                values[name] = self.read_new_decimal(column)
            else:
                raise NotImplementedError("Unknown MySQL column type: %d" % (column.type))
        return values

    def read_new_decimal(self, column):
        '''Read MySQL's new decimal format introduced in MySQL 5'''
        
        # This project was a great source of inspiration for
        # understanding this storage format.
        # https://github.com/jeremycole/mysql_binlog

        digits_per_integer = 9
        compressed_bytes = [0, 1, 1, 2, 2, 3, 3, 4, 4, 4]
        integral = (column.precision - column.decimals)
        uncomp_integral = int(integral / digits_per_integer)
        uncomp_fractional = int(column.decimals / digits_per_integer)
        comp_integral = integral - (uncomp_integral * digits_per_integer)
        comp_fractional = column.decimals - (uncomp_fractional * digits_per_integer)

        # Support negative
        # The sign is encoded in the high bit of the the byte
        # But this bit can also be used in the value
        value = struct.unpack('<B', self.packet.read(1))[0]
        if value & 0x80 != 0:
            res = ""
            mask = 0
        else:
            mask = -1
            res = "-"
        self.packet.unread(struct.pack('<B', value ^ 0x80))


        size = compressed_bytes[comp_integral]

        if size > 0:
            value = self.packet.read_int_be_by_size(size) ^ mask 
            res += str(value)

        for i in range(0, uncomp_integral):
            value = struct.unpack('>i', self.packet.read(4))[0] ^ mask
            res += str(value)

        res += "."

        for i in range(0, uncomp_fractional):
            value = struct.unpack('>i', self.packet.read(4))[0] ^ mask
            res += str(value)

        size = compressed_bytes[comp_fractional]
        if size > 0:
            value = self.packet.read_int_be_by_size(size) ^ mask
            res += str(value)

        return decimal.Decimal(res)

    def _dump(self):
        super(RowsEvent, self)._dump()
        print("Table: %s.%s" % (self.schema, self.table))
        print("Affected columns: %d" % (self.number_of_columns))
        print("Changed rows: %d" % (len(self.rows)))

    def _fetch_rows(self):
        self.__rows = []
        while self.packet.read_bytes + 1 < self.event_size:
            self.__rows.append(self._fetch_one_row())
    
    def __getattr__(self, name):
        if name == "rows":
            if self.__rows is None:
                self._fetch_rows()
            return self.__rows


class DeleteRowsEvent(RowsEvent):
    def __init__(self, from_packet, event_size, table_map, ctl_connection):
        super(DeleteRowsEvent, self).__init__(from_packet, event_size, table_map, ctl_connection)
        self.columns_present_bitmap = self.packet.read((self.number_of_columns + 7) / 8)

    def _fetch_one_row(self):
        row = {}

        #TODO: nul-bitmap, length (bits set in 'columns-present-bitmap'+7)/8
        self.packet.advance((self.number_of_columns + 7) / 8)
        row["values"] = self._read_column_data()
        return row

    def _dump(self):
        super(DeleteRowsEvent, self)._dump()
        print("Values:")
        for row in self.rows:
            print("--")
            for key in row["values"]:
                print("*", key, ":", row["values"][key])

class WriteRowsEvent(RowsEvent):
    def __init__(self, from_packet, event_size, table_map, ctl_connection):
        super(WriteRowsEvent, self).__init__(from_packet, event_size, table_map, ctl_connection)
        self.columns_present_bitmap = self.packet.read((self.number_of_columns + 7) / 8)

    def _fetch_one_row(self):
        row = {}

        #TODO: nul-bitmap, length (bits set in 'columns-present-bitmap'+7)/8
        self.packet.advance((self.number_of_columns + 7) / 8)
        row["values"] = self._read_column_data()
        return row

    def _dump(self):
        super(WriteRowsEvent, self)._dump()
        print("Values:")
        for row in self.rows:
            print("--")
            for key in row["values"]:
                print("*", key, ":", row["values"][key])


class UpdateRowsEvent(RowsEvent):
    def __init__(self, from_packet, event_size, table_map, ctl_connection):
        super(UpdateRowsEvent,self).__init__(from_packet, event_size, table_map, ctl_connection)
        #Body
        self.columns_present_bitmap = self.packet.read((self.number_of_columns + 7) / 8)
        self.columns_present_bitmap2 = self.packet.read((self.number_of_columns + 7) / 8)

    def _fetch_one_row(self):
        row = {}
        #TODO: nul-bitmap, length (bits set in 'columns-present-bitmap'+7)/8
        self.packet.advance((self.number_of_columns + 7) / 8)

        row["before_values"] = self._read_column_data()

        #TODO: nul-bitmap, length (bits set in 'columns-present-bitmap'+7)/8
        self.packet.advance((self.number_of_columns + 7) / 8)

        row["after_values"] = self._read_column_data()
        return row

    def _dump(self):
        super(UpdateRowsEvent, self)._dump()
        print("Affected columns: %d" % (self.number_of_columns))
        print("Values:")
        for row in self.rows:
            print("--")
            for key in row["before_values"]:
                print("*", key, ":", row["before_values"][key], "=>", row["after_values"][key])


class TableMapEvent(BinLogEvent):
    '''This evenement describe the structure of a table.
    It's send before a change append on a table.
    A end user of the lib should have no usage of this'''
    def __init__(self, from_packet, event_size, table_map, ctl_connection):
        super(TableMapEvent, self).__init__(from_packet, event_size, table_map, ctl_connection)

        # Post-Header
        self.table_id = self._read_table_id() 
        self.flags = struct.unpack('<H', self.packet.read(2))[0]


        # Payload
        self.schema_length =  byte2int(self.packet.read(1))
        self.schema = self.packet.read(self.schema_length).decode()
        self.packet.advance(1)
        self.table_length =  byte2int(self.packet.read(1))
        self.table = self.packet.read(self.table_length).decode()
        self.packet.advance(1)
        self.column_count = self.packet.read_length_coded_binary()

        self.columns = []

        column_schemas = self.__get_table_informations(self.schema, self.table)

        #Read columns meta data
        column_types = list(self.packet.read(self.column_count))
        metadata_length = self.packet.read_length_coded_binary()
        for i in range(0, len(column_types)):
            column_type = column_types[i]
            column_schema = column_schemas[i]
            col = Column(byte2int(column_type), column_schema, from_packet)
            self.columns.append(col)


        # TODO: get this informations instead of trashing data
        # n              NULL-bitmask, length: (column-length * 8) / 7

    def __get_table_informations(self, schema, table):
        #TODO: Cache this information
        cur = self._ctl_connection.cursor()
        cur.execute("""SELECT * FROM columns WHERE table_schema = %s AND table_name = %s""", (schema, table))
        return cur.fetchall()

    def _dump(self):
        super(TableMapEvent, self)._dump()
        print("Table id: %d" % (self.table_id))
        print("Schema: %s" % (self.schema))
        print("Table: %s" % (self.table))
        print("Columns: %s" % (self.column_count))

