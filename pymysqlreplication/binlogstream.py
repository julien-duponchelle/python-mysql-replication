import struct
from pymysql.util import byte2int, int2byte
from pymysql.constants.COMMAND import *
from constants.BINLOG import *
from pymysql.constants.FIELD_TYPE import *

class BinLogStreamReader(object):
    '''Connect to replication stream and read event'''
    
    def __init__(self, connection, resume_stream = False, blocking = False):
        '''
        resume_stream: Start for latest event of binlog or from older available event
        blocking: Read on stream is blocking
        '''
        self.__connection = connection

        cur = self.__connection.cursor()
        cur.execute("SHOW MASTER STATUS")
        (log_file, log_pos) = cur.fetchone()[:2]
        cur.close()


        # binlog_pos (4) -- position in the binlog-file to start the stream with
        # flags (2) BINLOG_DUMP_NON_BLOCK (0 or 1)
        # server_id (4) -- server id of this slave
        # binlog-filename (string.EOF) -- filename of the binlog on the master
        command = COM_BINLOG_DUMP
        prelude = struct.pack('<i', len(log_file) + 11) \
                + int2byte(command)
        if resume_stream:
            prelude += struct.pack('<I', log_pos)            
        else:
            prelude += struct.pack('<I', 4)
        if blocking:
            prelude += struct.pack('<h', 0)
        else:
            prelude += struct.pack('<h', 1)        
        prelude += struct.pack('<I', 3)
        self.__connection.wfile.write(prelude + log_file)
        self.__connection.wfile.flush()

        #Store table meta informations
        self.table_map = {}
        
    def fetchone(self):
        pkt = self.__connection.read_packet()
        if not pkt.is_ok_packet():
            return None
        binlog_event = BinLogPacketWrapper(pkt, self.table_map)
        if binlog_event.event_type == TABLE_MAP_EVENT:
            self.table_map[binlog_event.event.table_id] = binlog_event.event
        return binlog_event

    def __iter__(self):
        return iter(self.fetchone, None)

class BinLogPacketWrapper(object):
    """
    Bin Log Packet Wrapper. It uses an existing packet object, and wraps
    around it, exposing useful variables while still providing access
    to the original packet objects variables and methods.
    """

    def __init__(self, from_packet, table_map):
        if not from_packet.is_ok_packet():
            raise ValueError('Cannot create ' + str(self.__class__.__name__)
                + ' object from invalid packet type')
        
        # Ok Value
        self.packet = from_packet
        self.packet.advance(1)
  
        # Header
        self.timestamp = struct.unpack('<I', self.packet.read(4))[0]
        self.event_type = byte2int(self.packet.read(1))
        self.server_id = struct.unpack('<I', self.packet.read(4))[0]
        self.event_size = struct.unpack('<I', self.packet.read(4))[0]
        # position of the next event
        self.log_pos = struct.unpack('<I', self.packet.read(4))[0]
        self.flags = struct.unpack('<H', self.packet.read(2))[0]
        

        event_size_without_header = self.event_size - 19
        if self.event_type == QUERY_EVENT:
            self.event = BinLogQueryEvent(self.packet, event_size_without_header, table_map)
        elif self.event_type == UPDATE_ROWS_EVENT:
            self.event = UpdateRowsEvent(self.packet, event_size_without_header, table_map)
        elif self.event_type == WRITE_ROWS_EVENT:
            self.event = WriteRowsEvent(self.packet, event_size_without_header, table_map)
        elif self.event_type == DELETE_ROWS_EVENT:
            self.event = DeleteRowsEvent(self.packet, event_size_without_header, table_map)
        elif self.event_type == TABLE_MAP_EVENT:
            self.event = BinLogTableMapEvent(self.packet, event_size_without_header, table_map)
        else:
            self.event = None

    def __getattr__(self, key):
        if hasattr(self.packet, key):
            return getattr(self.packet, key)
        
        raise AttributeError(str(self.__class__)
            + " instance has no attribute '" + key + "'")


class BinLogEvent(object):
    def __init__(self, from_packet, event_size, table_map):
        self.packet = from_packet
        self.table_map = table_map

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


class DeleteRowsEvent(BinLogEvent):
    def __init__(self, from_packet, event_size, table_map):
        super(DeleteRowsEvent, self).__init__(from_packet, event_size, table_map)
        #Header
        self.table_id = self._read_table_id()
        self.flags = struct.unpack('<H', self.packet.read(2))[0]

        #Body
        self.number_of_columns = self.packet.read_length_coded_binary()
        self.columns_present_bitmap = self.packet.read((self.number_of_columns + 7) / 8)

        #TODO: nul-bitmap, length (bits set in 'columns-present-bitmap'+7)/8
        self.packet.advance((self.number_of_columns + 7) / 8)

        self.values = self._read_column_data()

    def dump(self):
        table = self.table_map[self.table_id]
        print "== Delete Rows Event =="
        print "Table: %s.%s" % (table.schema, table.table)
        print "Affected columns: %d" % (self.number_of_columns)
        print "Values:"
        for i in range(len(self.values)):
            print "* ", self.values[i]
        print


class WriteRowsEvent(BinLogEvent):
    def __init__(self, from_packet, event_size, table_map):
        super(WriteRowsEvent, self).__init__(from_packet, event_size, table_map)
        #Header
        self.table_id = self._read_table_id()
        self.flags = struct.unpack('<H', self.packet.read(2))[0]

        #Body
        self.number_of_columns = self.packet.read_length_coded_binary()
        self.columns_present_bitmap = self.packet.read((self.number_of_columns + 7) / 8)

        #TODO: nul-bitmap, length (bits set in 'columns-present-bitmap'+7)/8
        self.packet.advance((self.number_of_columns + 7) / 8)

        self.values = self._read_column_data()


    def dump(self):
        table = self.table_map[self.table_id]
        print "== Write Rows Event =="
        print "Table: %s.%s" % (table.schema, table.table)
        print "Affected columns: %d" % (self.number_of_columns)
        print "Values:"
        for i in range(len(self.values)):
            print "* ", self.values[i]
        print


class UpdateRowsEvent(BinLogEvent):
    def __init__(self, from_packet, event_size, table_map):
        super(UpdateRowsEvent,self).__init__(from_packet, event_size, table_map)
        #Header
        self.table_id = self._read_table_id()
        self.flags = struct.unpack('<H', self.packet.read(2))[0]

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
        table = self.table_map[self.table_id]
        print "== Update Rows Event =="
        print "Table: %s.%s" % (table.schema, table.table)
        print "Affected columns: %d" % (self.number_of_columns)
        print "Values:"
        for i in range(len(self.before_values)):
            print "* ", self.before_values[i] , " => ", self.after_values[i]
        print


class BinLogTableMapEvent(BinLogEvent):
    def __init__(self, from_packet, event_size, table_map):
        super(BinLogTableMapEvent, self).__init__(from_packet, event_size, table_map)

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
        #import sys
        #sys.exit(0)

class BinLogQueryEvent(BinLogEvent):
    def __init__(self, from_packet, event_size, table_map):
        super(BinLogQueryEvent, self).__init__(from_packet, event_size, table_map)

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
