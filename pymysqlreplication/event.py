import struct
from pymysql.util import byte2int, int2byte
from pymysql.constants.FIELD_TYPE import *

class BinLogEvent(object):
    def __init__(self, from_packet, event_size, table_map):
        self.packet = from_packet
        self.table_map = table_map
        self.event_type = self.packet.event_type
        self.timestamp = self.packet.timestamp

    def _read_table_id(self):
        # Table ID is 6 byte
        table_id = self.packet.read(6) + int2byte(0) + int2byte(0)   # pad little-endian number
        return struct.unpack('<Q', table_id)[0]

    def _read_column_data(self):
        '''Use for WRITE, UPDATE and DELETE events. Return an array of column data'''
        values = []

        for column in self.table_map[self.table_id].column_type_def:
            if column == LONG:
                values.append(struct.unpack("<I", self.packet.read(4))[0])
            elif column == VARCHAR:
                values.append(self.packet.read_length_coded_string())
        return values


class RowsEvent(BinLogEvent):
    def __init__(self, from_packet, event_size, table_map):
        super(RowsEvent, self).__init__(from_packet, event_size, table_map)

        #Header
        self.table_id = self._read_table_id()
        self.flags = struct.unpack('<H', self.packet.read(2))[0]

        self.table = self.table_map[self.table_id]


class DeleteRowsEvent(RowsEvent):
    def __init__(self, from_packet, event_size, table_map):
        super(DeleteRowsEvent, self).__init__(from_packet, event_size, table_map)
        #Body
        self.number_of_columns = self.packet.read_length_coded_binary()
        self.columns_present_bitmap = self.packet.read((self.number_of_columns + 7) / 8)

        #TODO: nul-bitmap, length (bits set in 'columns-present-bitmap'+7)/8
        self.packet.advance((self.number_of_columns + 7) / 8)

        self.values = self._read_column_data()

    def dump(self):
        table = self.table_map[self.table_id]
        print "== Delete Rows Event =="
        print "Table: %s.%s" % (self.table.schema, self.table.table)
        print "Affected columns: %d" % (self.number_of_columns)
        print "Values:"
        for i in range(len(self.values)):
            print "* ", self.values[i]
        print


class WriteRowsEvent(RowsEvent):
    def __init__(self, from_packet, event_size, table_map):
        super(WriteRowsEvent, self).__init__(from_packet, event_size, table_map)
        #Body
        self.number_of_columns = self.packet.read_length_coded_binary()
        self.columns_present_bitmap = self.packet.read((self.number_of_columns + 7) / 8)

        #TODO: nul-bitmap, length (bits set in 'columns-present-bitmap'+7)/8
        self.packet.advance((self.number_of_columns + 7) / 8)

        self.values = self._read_column_data()


    def dump(self):
        print "== Write Rows Event =="
        print "Table: %s.%s" % (self.table.schema, self.table.table)
        print "Affected columns: %d" % (self.number_of_columns)
        print "Values:"
        for i in range(len(self.values)):
            print "* ", self.values[i]
        print


class UpdateRowsEvent(RowsEvent):
    def __init__(self, from_packet, event_size, table_map):
        super(UpdateRowsEvent,self).__init__(from_packet, event_size, table_map)
        #Body
        self.number_of_columns = self.packet.read_length_coded_binary()
        self.columns_present_bitmap = self.packet.read((self.number_of_columns + 7) / 8)
        self.columns_present_bitmap2 = self.packet.read((self.number_of_columns + 7) / 8)

        #TODO: nul-bitmap, length (bits set in 'columns-present-bitmap'+7)/8
        self.packet.advance((self.number_of_columns + 7) / 8)

        self.before_values = self._read_column_data()

        #TODO: nul-bitmap, length (bits set in 'columns-present-bitmap'+7)/8
        self.packet.advance((self.number_of_columns + 7) / 8)

        self.after_values = self._read_column_data()

    def dump(self):
        print "== Update Rows Event =="
        print "Table: %s.%s" % (self.table.schema, self.table.table)
        print "Affected columns: %d" % (self.number_of_columns)
        print "Values:"
        for i in range(len(self.before_values)):
            print "* ", self.before_values[i] , " => ", self.after_values[i]
        print


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

        self.column_type_def = []
        for column in list(self.packet.read(self.column_count)):
            self.column_type_def.append(byte2int(column))


        # TODO: get this informations instead of trashing data
        # lenenc-str     column-def
        # n              NULL-bitmask, length: (column-length * 8) / 7

    def dump(self):
        print "== Table Map Event =="
        print "Table id: %d" % (self.table_id)
        print "Schema: %s" % (self.schema)
        print "Table: %s" % (self.table)
        print "Columns: %s" % (self.column_count)

        print

class RotateEvent(BinLogEvent):
    def dump(self):
        print "== Rotate Event =="
        print

class FormatDescriptionEvent(BinLogEvent):
    def dump(self):
        print "== Format Description Event =="
        print
 
class XidEvent(BinLogEvent):
    def dump(self):
        print "== Xid Event =="
        print

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

    def dump(self):
        print "== Query Event =="
        print "Schema: %s" % (self.schema)
        print "Execution time: %d" % (self.execution_time) 
        print "Query: %s" % (self.query)

        print

