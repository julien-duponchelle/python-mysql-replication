import struct
from datetime import datetime
from pymysql.util import byte2int, int2byte
from pymysql.constants.FIELD_TYPE import *

#Constants from PyMYSQL source code
NULL_COLUMN = 251
UNSIGNED_CHAR_COLUMN = 251
UNSIGNED_SHORT_COLUMN = 252
UNSIGNED_INT24_COLUMN = 253
UNSIGNED_INT64_COLUMN = 254
UNSIGNED_CHAR_LENGTH = 1
UNSIGNED_SHORT_LENGTH = 2
UNSIGNED_INT24_LENGTH = 3
UNSIGNED_INT64_LENGTH = 8



class BinLogEvent(object):
    def __init__(self, from_packet, event_size, table_map):
        self.packet = from_packet
        self.table_map = table_map
        self.event_type = self.packet.event_type
        self.timestamp = self.packet.timestamp
        self.event_size = event_size
        self._read_bytes = 0

    def _read_table_id(self):
        # Table ID is 6 byte
        table_id = self._packet_read(6) + int2byte(0) + int2byte(0)   # pad little-endian number
        return struct.unpack('<Q', table_id)[0]

    def _read_column_data(self):
        '''Use for WRITE, UPDATE and DELETE events. Return an array of column data'''
        values = []

        for column in self.table_map[self.table_id].column_type_def:
            if column == LONG:
                values.append(struct.unpack("<I", self._packet_read(4))[0])
            elif column == VARCHAR:
                values.append(self._packet_read_length_coded_string())
        return values

    def _packet_read(self, size):
        self._read_bytes += size
        return self.packet.read(size)

    def _packet_advance(self, size):
        self._read_bytes += size
        self.packet.advance(size)

    def _packet_read_length_coded_binary(self):
        """Read a 'Length Coded Binary' number from the data buffer.

        Length coded numbers can be anywhere from 1 to 9 bytes depending
        on the value of the first byte.

        From PyMYSQL source code
        """
        c = byte2int(self._packet_read(1))
        if c == NULL_COLUMN:
          return None
        if c < UNSIGNED_CHAR_COLUMN:
          return c
        elif c == UNSIGNED_SHORT_COLUMN:
          return unpack_uint16(self._packet_read(UNSIGNED_SHORT_LENGTH))
        elif c == UNSIGNED_INT24_COLUMN:
          return unpack_int24(self._packet_read(UNSIGNED_INT24_LENGTH))
        elif c == UNSIGNED_INT64_COLUMN:
          # TODO: what was 'longlong'?  confirm it wasn't used?
          return unpack_int64(self._packet_read(UNSIGNED_INT64_LENGTH))

    def _packet_read_length_coded_string(self):
        """Read a 'Length Coded String' from the data buffer.

        A 'Length Coded String' consists first of a length coded
        (unsigned, positive) integer represented in 1-9 bytes followed by
        that many bytes of binary data.  (For example "cat" would be "3cat".)

        From PyMYSQL source code
        """
        length = self._packet_read_length_coded_binary()
        if length is None:
            return None
        return self._packet_read(length)

    def dump(self):
        print "=== %s ===" % (self.__class__.__name__)
        print "Date: %s" % (datetime.fromtimestamp(self.timestamp).isoformat())
        print "Event size: %d" % (self.event_size)
        print "Read bytes: %d" % (self._read_bytes)
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
        self.flags = struct.unpack('<H', self._packet_read(2))[0]

        #Body
        self.number_of_columns = self.packet.read_length_coded_binary()

        self.table = self.table_map[self.table_id]

    def _dump(self):
        super(RowsEvent, self)._dump()
        print "Table: %s.%s" % (self.table.schema, self.table.table)
        print "Affected columns: %d" % (self.number_of_columns)
        print "Changed rows: %d" % (len(self.rows))

    def _fetch_rows(self):
        self.__rows = []
        while self._read_bytes + 1 < self.event_size:
            self.__rows.append(self._fetch_one_row())
    
    def __getattr__(self, name):
        if name == "rows":
            if self.__rows is None:
                self._fetch_rows()
            return self.__rows

class DeleteRowsEvent(RowsEvent):
    def __init__(self, from_packet, event_size, table_map):
        super(DeleteRowsEvent, self).__init__(from_packet, event_size, table_map)
        self.columns_present_bitmap = self._packet_read((self.number_of_columns + 7) / 8)

    def _fetch_one_row(self):
        row = {}

        #TODO: nul-bitmap, length (bits set in 'columns-present-bitmap'+7)/8
        self._packet_advance((self.number_of_columns + 7) / 8)
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
        self.columns_present_bitmap = self._packet_read((self.number_of_columns + 7) / 8)

    def _fetch_one_row(self):
        row = {}

        #TODO: nul-bitmap, length (bits set in 'columns-present-bitmap'+7)/8
        self._packet_advance((self.number_of_columns + 7) / 8)
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
        self.columns_present_bitmap = self._packet_read((self.number_of_columns + 7) / 8)
        self.columns_present_bitmap2 = self._packet_read((self.number_of_columns + 7) / 8)

    def _fetch_one_row(self):
        row = {}
        #TODO: nul-bitmap, length (bits set in 'columns-present-bitmap'+7)/8
        self._packet_advance((self.number_of_columns + 7) / 8)

        row["before_values"] = self._read_column_data()

        #TODO: nul-bitmap, length (bits set in 'columns-present-bitmap'+7)/8
        self._packet_advance((self.number_of_columns + 7) / 8)

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
        self.flags = struct.unpack('<H', self._packet_read(2))[0]


        # Payload
        self.schema_length =  byte2int(self._packet_read(1))
        self.schema =  self._packet_read(self.schema_length)
        self._packet_advance(1)
        self.table_length =  byte2int(self._packet_read(1))
        self.table =  self._packet_read(self.table_length)
        self._packet_advance(1)
        self.column_count = self.packet.read_length_coded_binary()

        self.column_type_def = []
        for column in list(self._packet_read(self.column_count)):
            self.column_type_def.append(byte2int(column))


        # TODO: get this informations instead of trashing data
        # lenenc-str     column-def
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
        self.xid = struct.unpack('<Q', self._packet_read(8))[0]

    def _dump(self):
        super(XidEvent, self)._dump()
        print "Transaction ID: %d" % (self.xid)


class QueryEvent(BinLogEvent):
    def __init__(self, from_packet, event_size, table_map):
        super(QueryEvent, self).__init__(from_packet, event_size, table_map)

        # Post-header
        self.slave_proxy_id = struct.unpack('<I', self._packet_read(4))[0]
        self.execution_time = struct.unpack('<I', self._packet_read(4))[0]
        self.schema_length =  byte2int(self._packet_read(1))
        self.error_code = struct.unpack('<H', self._packet_read(2))[0]
        self.status_vars_length = struct.unpack('<H', self._packet_read(2))[0]

        # Payload
        self.status_vars = self._packet_read(self.status_vars_length)
        self.schema =  self._packet_read(self.schema_length)
        self._packet_advance(1)

        self.query = self._packet_read(event_size - 13 - self.status_vars_length - self.schema_length - 1)
        #string[EOF]    query

    def _dump(self):
        super(QueryEvent, self)._dump()
        print "Schema: %s" % (self.schema)
        print "Execution time: %d" % (self.execution_time) 
        print "Query: %s" % (self.query)

