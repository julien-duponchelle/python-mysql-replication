# -*- coding: utf-8 -*-

import struct

from pymysql.util import byte2int

from pymysqlreplication import constants, event, row_event

# Constants from PyMYSQL source code
NULL_COLUMN = 251
UNSIGNED_CHAR_COLUMN = 251
UNSIGNED_SHORT_COLUMN = 252
UNSIGNED_INT24_COLUMN = 253
UNSIGNED_INT64_COLUMN = 254
UNSIGNED_CHAR_LENGTH = 1
UNSIGNED_SHORT_LENGTH = 2
UNSIGNED_INT24_LENGTH = 3
UNSIGNED_INT64_LENGTH = 8


class BinLogPacketWrapper(object):
    """
    Bin Log Packet Wrapper. It uses an existing packet object, and wraps
    around it, exposing useful variables while still providing access
    to the original packet objects variables and methods.
    """

    __event_map = {
        # event
        constants.QUERY_EVENT: event.QueryEvent,
        constants.ROTATE_EVENT: event.RotateEvent,
        constants.FORMAT_DESCRIPTION_EVENT: event.FormatDescriptionEvent,
        constants.XID_EVENT: event.XidEvent,
        constants.INTVAR_EVENT: event.IntvarEvent,
        constants.GTID_LOG_EVENT: event.GtidEvent,
        constants.STOP_EVENT: event.StopEvent,
        constants.BEGIN_LOAD_QUERY_EVENT: event.BeginLoadQueryEvent,
        constants.EXECUTE_LOAD_QUERY_EVENT: event.ExecuteLoadQueryEvent,
        # row_event
        constants.UPDATE_ROWS_EVENT_V1: row_event.UpdateRowsEvent,
        constants.WRITE_ROWS_EVENT_V1: row_event.WriteRowsEvent,
        constants.DELETE_ROWS_EVENT_V1: row_event.DeleteRowsEvent,
        constants.UPDATE_ROWS_EVENT_V2: row_event.UpdateRowsEvent,
        constants.WRITE_ROWS_EVENT_V2: row_event.WriteRowsEvent,
        constants.DELETE_ROWS_EVENT_V2: row_event.DeleteRowsEvent,
        constants.TABLE_MAP_EVENT: row_event.TableMapEvent,
        #5.6 GTID enabled replication events
        constants.ANONYMOUS_GTID_LOG_EVENT: event.NotImplementedEvent,
        constants.PREVIOUS_GTIDS_LOG_EVENT: event.NotImplementedEvent

    }

    def __init__(self, from_packet, table_map, ctl_connection, use_checksum,
                 allowed_events,
                 only_tables,
                 only_schemas,
                 freeze_schema):
        # -1 because we ignore the ok byte
        self.read_bytes = 0
        # Used when we want to override a value in the data buffer
        self.__data_buffer = b''

        self.packet = from_packet
        self.charset = ctl_connection.charset

        # OK value
        # timestamp
        # event_type
        # server_id
        # log_pos
        # flags
        unpack = struct.unpack('<cIcIIIH', self.packet.read(20))

        # Header
        self.timestamp = unpack[1]
        self.event_type = byte2int(unpack[2])
        self.server_id = unpack[3]
        self.event_size = unpack[4]
        # position of the next event
        self.log_pos = unpack[5]
        self.flags = unpack[6]

        # MySQL 5.6 and more if binlog-checksum = CRC32
        if use_checksum:
            event_size_without_header = self.event_size - 23
        else:
            event_size_without_header = self.event_size - 19

        self.event = None
        event_class = self.__event_map.get(self.event_type, event.NotImplementedEvent)

        if event_class not in allowed_events:
            return
        self.event = event_class(self, event_size_without_header, table_map,
                                 ctl_connection,
                                 only_tables = only_tables,
                                 only_schemas = only_schemas,
                                 freeze_schema = freeze_schema)
        if self.event._processed == False:
            self.event = None

    def read(self, size):
        size = int(size)
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
        size = int(size)
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
            return self.unpack_uint16(self.read(UNSIGNED_SHORT_LENGTH))
        elif c == UNSIGNED_INT24_COLUMN:
            return self.unpack_int24(self.read(UNSIGNED_INT24_LENGTH))
        elif c == UNSIGNED_INT64_COLUMN:
            return self.unpack_int64(self.read(UNSIGNED_INT64_LENGTH))

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
        return self.read(length).decode()

    def __getattr__(self, key):
        if hasattr(self.packet, key):
            return getattr(self.packet, key)

        raise AttributeError("%s instance has no attribute '%s'" %
                             (self.__class__, key))

    def read_int_be_by_size(self, size):
        '''Read a big endian integer values based on byte number'''
        if size == 1:
            return struct.unpack('>b', self.read(size))[0]
        elif size == 2:
            return struct.unpack('>h', self.read(size))[0]
        elif size == 3:
            return self.read_int24_be()
        elif size == 4:
            return struct.unpack('>i', self.read(size))[0]
        elif size == 5:
            return self.read_int40_be()
        elif size == 8:
            return struct.unpack('>l', self.read(size))[0]

    def read_uint_by_size(self, size):
        '''Read a little endian integer values based on byte number'''
        if size == 1:
            return self.read_uint8()
        elif size == 2:
            return self.read_uint16()
        elif size == 3:
            return self.read_uint24()
        elif size == 4:
            return self.read_uint32()
        elif size == 5:
            return self.read_uint40()
        elif size == 6:
            return self.read_uint48()
        elif size == 7:
            return self.read_uint56()
        elif size == 8:
            return self.read_uint64()

    def read_length_coded_pascal_string(self, size):
        """Read a string with length coded using pascal style.
        The string start by the size of the string
        """
        length = self.read_uint_by_size(size)
        return self.read(length)

    def read_int24(self):
        a, b, c = struct.unpack("BBB", self.read(3))
        res = a | (b << 8) | (c << 16)
        if res >= 0x800000:
            res -= 0x1000000
        return res

    def read_int24_be(self):
        a, b, c = struct.unpack('BBB', self.read(3))
        res = (a << 16) | (b << 8) | c
        if res >= 0x800000:
            res -= 0x1000000
        return res

    def read_uint8(self):
        return struct.unpack('<B', self.read(1))[0]

    def read_uint16(self):
        return struct.unpack('<H', self.read(2))[0]

    def read_uint24(self):
        a, b, c = struct.unpack("<BBB", self.read(3))
        return a + (b << 8) + (c << 16)

    def read_uint32(self):
        return struct.unpack('<I', self.read(4))[0]

    def read_uint40(self):
        a, b = struct.unpack("<BI", self.read(5))
        return a + (b << 8)

    def read_int40_be(self):
        a, b = struct.unpack(">IB", self.read(5))
        return b + (a << 8)

    def read_uint48(self):
        a, b, c = struct.unpack("<HHH", self.read(6))
        return a + (b << 16) + (c << 32)

    def read_uint56(self):
        a, b, c = struct.unpack("<BHI", self.read(7))
        return a + (b << 8) + (c << 24)

    def read_uint64(self):
        return struct.unpack('<Q', self.read(8))[0]

    def read_int64(self):
        return struct.unpack('<q', self.read(8))[0]

    def unpack_uint16(self, n):
        return struct.unpack('<H', n[0:2])[0]

    def unpack_int24(self, n):
        try:
            return struct.unpack('B', n[0])[0] \
                + (struct.unpack('B', n[1])[0] << 8) \
                + (struct.unpack('B', n[2])[0] << 16)
        except TypeError:
            return n[0] + (n[1] << 8) + (n[2] << 16)

    def unpack_int32(self, n):
        try:
            return struct.unpack('B', n[0])[0] \
                + (struct.unpack('B', n[1])[0] << 8) \
                + (struct.unpack('B', n[2])[0] << 16) \
                + (struct.unpack('B', n[3])[0] << 24)
        except TypeError:
            return n[0] + (n[1] << 8) + (n[2] << 16) + (n[3] << 24)
