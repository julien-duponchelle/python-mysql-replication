import struct
import decimal
from datetime import datetime
from pymysql.util import byte2int, int2byte
from pymysql.connections import unpack_uint16, unpack_int24,unpack_int64 
from pymysql.constants import FIELD_TYPE
from column import Column

class BinLogEvent(object):
    def __init__(self, from_packet, event_size, table_map):
        self.packet = from_packet
        self.table_map = table_map
        self.event_type = self.packet.event_type
        self.timestamp = self.packet.timestamp
        self.event_size = event_size

    def _read_table_id(self):
        # Table ID is 6 byte
        table_id = self.packet.read(6) + int2byte(0) + int2byte(0)   # pad little-endian number
        return struct.unpack('<Q', table_id)[0]

    def dump(self):
        print "=== %s ===" % (self.__class__.__name__)
        print "Date: %s" % (datetime.fromtimestamp(self.timestamp).isoformat())
        print "Event size: %d" % (self.event_size)
        print "Read bytes: %d" % (self.packet.read_bytes)
        self._dump()
        print
    
    def _dump(self):
        '''Core data dumped for the event'''
        pass


class RowsEvent(BinLogEvent):
    def __init__(self, from_packet, event_size, table_map):
        super(RowsEvent, self).__init__(from_packet, event_size, table_map)
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
        values = []

        for column in self.columns:
            if column.type == FIELD_TYPE.LONG:
                values.append(struct.unpack("<i", self.packet.read(4))[0])
            elif column.type == FIELD_TYPE.VARCHAR:
                values.append(self.packet.read_length_coded_string())
            elif column.type == FIELD_TYPE.STRING:
                values.append(self.packet.read_length_coded_string())
            elif column.type == FIELD_TYPE.NEWDECIMAL:
                values.append(self.read_new_decimal(column))
            else:
                raise NotImplementedError("Unknown MySQL column type: %d" % (column))
        return values

    def read_new_decimal(self, column):
        '''Read MySQL's new decimal format introduced in MySQL 5'''
        
        # This project was a great source of inspiration for
        # understanding this storage format.
        # https://github.com/jeremycole/mysql_binlog

        digits_per_integer = 9
        compressed_bytes = [0, 1, 1, 2, 2, 3, 3, 4, 4, 4]
        integral = (column.precision - column.decimals)
        uncomp_integral = integral / digits_per_integer
        uncomp_fractional = column.decimals / digits_per_integer
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
        print "Table: %s.%s" % (self.schema, self.table)
        print "Affected columns: %d" % (self.number_of_columns)
        print "Changed rows: %d" % (len(self.rows))

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
    def __init__(self, from_packet, event_size, table_map):
        super(DeleteRowsEvent, self).__init__(from_packet, event_size, table_map)
        self.columns_present_bitmap = self.packet.read((self.number_of_columns + 7) / 8)

    def _fetch_one_row(self):
        row = {}

        #TODO: nul-bitmap, length (bits set in 'columns-present-bitmap'+7)/8
        self.packet.advance((self.number_of_columns + 7) / 8)
        row["values"] = self._read_column_data()
        return row

    def _dump(self):
        super(DeleteRowsEvent, self)._dump()
        print "Values:"
        for row in self.rows:
            print "--"
            for i in range(len(row["values"])):
                print "* ", row["values"][i]

class WriteRowsEvent(RowsEvent):
    def __init__(self, from_packet, event_size, table_map):
        super(WriteRowsEvent, self).__init__(from_packet, event_size, table_map)
        self.columns_present_bitmap = self.packet.read((self.number_of_columns + 7) / 8)

    def _fetch_one_row(self):
        row = {}

        #TODO: nul-bitmap, length (bits set in 'columns-present-bitmap'+7)/8
        self.packet.advance((self.number_of_columns + 7) / 8)
        row["values"] = self._read_column_data()
        return row

    def _dump(self):
        super(WriteRowsEvent, self)._dump()
        print "Values:"
        for row in self.rows:
            print "--"
            for i in range(len(row["values"])):
                print "* ", row["values"][i]


class UpdateRowsEvent(RowsEvent):
    def __init__(self, from_packet, event_size, table_map):
        super(UpdateRowsEvent,self).__init__(from_packet, event_size, table_map)
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
        print "Affected columns: %d" % (self.number_of_columns)
        print "Values:"
        for row in self.rows:
            print "--"
            for i in range(len(row["before_values"])):
                print " * ", row["before_values"][i] , " => ", row["after_values"][i]


class TableMapEvent(BinLogEvent):
    def __init__(self, from_packet, event_size, table_map):
        super(TableMapEvent, self).__init__(from_packet, event_size, table_map)

        # Post-Header
        self.table_id = self._read_table_id() 
        self.flags = struct.unpack('<H', self.packet.read(2))[0]


        # Payload
        self.schema_length =  byte2int(self.packet.read(1))
        self.schema =  self.packet.read(self.schema_length)
        self.packet.advance(1)
        self.table_length =  byte2int(self.packet.read(1))
        self.table =  self.packet.read(self.table_length)
        self.packet.advance(1)
        self.column_count = self.packet.read_length_coded_binary()

        self.columns = []

        #Read columns meta data
        column_types = list(self.packet.read(self.column_count))
        metadata_length = self.packet.read_length_coded_binary()
        for column_type in column_types:
            col = Column(byte2int(column_type), from_packet)
            self.columns.append(col)


        # TODO: get this informations instead of trashing data
        # n              NULL-bitmask, length: (column-length * 8) / 7

    def _dump(self):
        super(TableMapEvent, self)._dump()
        print "Table id: %d" % (self.table_id)
        print "Schema: %s" % (self.schema)
        print "Table: %s" % (self.table)
        print "Columns: %s" % (self.column_count)


class RotateEvent(BinLogEvent):
    pass


class FormatDescriptionEvent(BinLogEvent):
    pass


class XidEvent(BinLogEvent):
    """
        A COMMIT event

        Attributes:
            xid: Transaction ID for 2PC
    """

    def __init__(self, from_packet, event_size, table_map):
        super(XidEvent, self).__init__(from_packet, event_size, table_map)
        self.xid = struct.unpack('<Q', self.packet.read(8))[0]

    def _dump(self):
        super(XidEvent, self)._dump()
        print "Transaction ID: %d" % (self.xid)


class QueryEvent(BinLogEvent):
    def __init__(self, from_packet, event_size, table_map):
        super(QueryEvent, self).__init__(from_packet, event_size, table_map)

        # Post-header
        self.slave_proxy_id = struct.unpack('<I', self.packet.read(4))[0]
        self.execution_time = struct.unpack('<I', self.packet.read(4))[0]
        self.schema_length =  byte2int(self.packet.read(1))
        self.error_code = struct.unpack('<H', self.packet.read(2))[0]
        self.status_vars_length = struct.unpack('<H', self.packet.read(2))[0]

        # Payload
        self.status_vars = self.packet.read(self.status_vars_length)
        self.schema =  self.packet.read(self.schema_length)
        self.packet.advance(1)

        self.query = self.packet.read(event_size - 13 - self.status_vars_length - self.schema_length - 1)
        #string[EOF]    query

    def _dump(self):
        super(QueryEvent, self)._dump()
        print "Schema: %s" % (self.schema)
        print "Execution time: %d" % (self.execution_time) 
        print "Query: %s" % (self.query)

