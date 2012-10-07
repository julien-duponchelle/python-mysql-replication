import struct
import copy
import pymysql
import pymysql.cursors
from pymysql.util import byte2int, int2byte
from pymysql.constants.COMMAND import *
from constants.BINLOG import *
from event import *
from row_event import *

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


class BinLogStreamReader(object):
    '''Connect to replication stream and read event'''
    
    def __init__(self, connection_settings = {}, resume_stream = False, blocking = False, only_events = None):
        '''
        resume_stream: Start for latest event of binlog or from older available event
        blocking: Read on stream is blocking
        only_events: Array of allowed events
        '''
        self.__stream_connection = pymysql.connect(**connection_settings)
        ctl_connection_settings = copy.copy(connection_settings)
        ctl_connection_settings['db'] = 'information_schema'
        ctl_connection_settings['cursorclass'] = pymysql.cursors.DictCursor
        self.__ctl_connection = pymysql.connect(**ctl_connection_settings)
        self.__connected = False
        self.__resume_stream = resume_stream
        self.__blocking = blocking
        self.__only_events = only_events

        #Store table meta informations
        self.table_map = {}

    def close(self):
        self.__stream_connection.close()
        self.__ctl_connection.close()

    def __connect_to_stream(self):
        cur = self.__stream_connection.cursor()
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
        if self.__resume_stream:
            prelude += struct.pack('<I', log_pos)            
        else:
            prelude += struct.pack('<I', 4)
        if self.__blocking:
            prelude += struct.pack('<h', 0)
        else:
            prelude += struct.pack('<h', 1)        
        prelude += struct.pack('<I', 3)
        self.__stream_connection.wfile.write(prelude + log_file)
        self.__stream_connection.wfile.flush()
        self.__connected = True
        
    def fetchone(self):
        if self.__connected == False:
            self.__connect_to_stream()
        while True:
            pkt = self.__stream_connection.read_packet()
            if not pkt.is_ok_packet():
                return None
            binlog_event = BinLogPacketWrapper(pkt, self.table_map, self.__ctl_connection)
            if binlog_event.event_type == TABLE_MAP_EVENT:
                self.table_map[binlog_event.event.table_id] = binlog_event.event
            if self.__filter_event(binlog_event.event):
                continue
            return binlog_event.event

    def __filter_event(self, event):
        if self.__only_events is not None:
            for allowed_event in self.__only_events:
                if isinstance(event, allowed_event):
                    return False
            return True
        return False

    def __iter__(self):
        return iter(self.fetchone, None)

class BinLogPacketWrapper(object):
    """
    Bin Log Packet Wrapper. It uses an existing packet object, and wraps
    around it, exposing useful variables while still providing access
    to the original packet objects variables and methods.
    """

    __event_map = {
        QUERY_EVENT: QueryEvent,
        UPDATE_ROWS_EVENT: UpdateRowsEvent,
        WRITE_ROWS_EVENT: WriteRowsEvent,
        DELETE_ROWS_EVENT: DeleteRowsEvent,
        TABLE_MAP_EVENT: TableMapEvent,
        ROTATE_EVENT: RotateEvent,
        FORMAT_DESCRIPTION_EVENT: FormatDescriptionEvent,
        XID_EVENT: XidEvent
    }

    def __init__(self, from_packet, table_map, ctl_connection):
        if not from_packet.is_ok_packet():
            raise ValueError('Cannot create ' + str(self.__class__.__name__)
                + ' object from invalid packet type')
       
        self.read_bytes = 0 #-1 because we ignore the ok byte
        self.__data_buffer = '' #Used when we want to override a value in the data buffer 

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
        try:
            event_class = self.__event_map[self.event_type]
        except KeyError:
            raise NotImplementedError("Unknown MySQL bin log event type: " + hex(self.event_type))
        self.event = event_class(self, event_size_without_header, table_map, ctl_connection)

    def read(self, size):
        self.read_bytes += size
        if len(self.__data_buffer) > 0:
            data = self.__data_buffer[:size]
            self.__data_buffer = self.__data_buffer[size:]
            if len(data) == size:
                return data
            else:
                return data + self.packet.read(size - len(data))
        return self.packet.read(size)

    def unread(self, data):
        '''Push again data in data buffer. It's use when you want
        to extract a bit from a value a let the rest of the code normally
        read the datas'''
        self.read_bytes -= len(data)
        self.__data_buffer += data

    def advance(self, size):
        self.read_bytes += size
        buffer_len = len(self.__data_buffer)
        if buffer_len > 0:
            self.__data_buffer = self.__data_buffer[size:]
            if size > buffer_len:
                self.packet.advance(size - buffer_len)
        else:
            self.packet.advance(size)

    def read_length_coded_binary(self):
        """Read a 'Length Coded Binary' number from the data buffer.

        Length coded numbers can be anywhere from 1 to 9 bytes depending
        on the value of the first byte.

        From PyMYSQL source code
        """
        c = byte2int(self.read(1))
        if c == NULL_COLUMN:
          return None
        if c < UNSIGNED_CHAR_COLUMN:
          return c
        elif c == UNSIGNED_SHORT_COLUMN:
            return unpack_int16(self.read(UNSIGNED_INT16_LENGTH))
        elif c == UNSIGNED_INT24_COLUMN:
          return unpack_int24(self.read(UNSIGNED_INT24_LENGTH))
        elif c == UNSIGNED_INT64_COLUMN:
          return unpack_int64(self.read(UNSIGNED_INT64_LENGTH))

    def read_length_coded_string(self):
        """Read a 'Length Coded String' from the data buffer.

        A 'Length Coded String' consists first of a length coded
        (unsigned, positive) integer represented in 1-9 bytes followed by
        that many bytes of binary data.  (For example "cat" would be "3cat".)

        From PyMYSQL source code
        """
        length = self.read_length_coded_binary()
        if length is None:
            return None
        return self.read(length)

    def __getattr__(self, key):
        if hasattr(self.packet, key):
            return getattr(self.packet, key)
        
        raise AttributeError(str(self.__class__)
            + " instance has no attribute '" + key + "'")

    def read_int_be_by_size(self, size):
        '''Read a big endian integer values based on byte number'''
        if size == 1:
            return struct.unpack('>b', self.read(size))[0]
        elif size == 2:
            return struct.unpack('>h', self.read(size))[0]
        elif size == 4:
            return struct.unpack('>i', self.read(size))[0]
        elif size == 8:
            return struct.unpack('>l', self.read(size))[0]
