import struct

from pymysqlreplication import constants, event, row_event
from pymysqlreplication.constants import FIELD_TYPE
from pymysqlreplication.util.bytes import *

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

JSONB_TYPE_SMALL_OBJECT = 0x0
JSONB_TYPE_LARGE_OBJECT = 0x1
JSONB_TYPE_SMALL_ARRAY = 0x2
JSONB_TYPE_LARGE_ARRAY = 0x3
JSONB_TYPE_LITERAL = 0x4
JSONB_TYPE_INT16 = 0x5
JSONB_TYPE_UINT16 = 0x6
JSONB_TYPE_INT32 = 0x7
JSONB_TYPE_UINT32 = 0x8
JSONB_TYPE_INT64 = 0x9
JSONB_TYPE_UINT64 = 0xA
JSONB_TYPE_DOUBLE = 0xB
JSONB_TYPE_STRING = 0xC
JSONB_TYPE_OPAQUE = 0xF

JSONB_LITERAL_NULL = 0x0
JSONB_LITERAL_TRUE = 0x1
JSONB_LITERAL_FALSE = 0x2

JSONB_SMALL_OFFSET_SIZE = 2
JSONB_LARGE_OFFSET_SIZE = 4
JSONB_KEY_ENTRY_SIZE_SMALL = 2 + JSONB_SMALL_OFFSET_SIZE
JSONB_KEY_ENTRY_SIZE_LARGE = 2 + JSONB_LARGE_OFFSET_SIZE
JSONB_VALUE_ENTRY_SIZE_SMALL = 1 + JSONB_SMALL_OFFSET_SIZE
JSONB_VALUE_ENTRY_SIZE_LARGE = 1 + JSONB_LARGE_OFFSET_SIZE


def is_json_inline_value(type: bytes, is_small: bool) -> bool:
    if type in [JSONB_TYPE_UINT16, JSONB_TYPE_INT16, JSONB_TYPE_LITERAL]:
        return True
    elif type in [JSONB_TYPE_INT32, JSONB_TYPE_UINT32]:
        return not is_small
    return False


def parse_json(type: bytes, data: bytes):
    if type == JSONB_TYPE_SMALL_OBJECT:
        v = parse_json_object_or_array(data, True, True)
    elif type == JSONB_TYPE_LARGE_OBJECT:
        v = parse_json_object_or_array(data, False, True)
    elif type == JSONB_TYPE_SMALL_ARRAY:
        v = parse_json_object_or_array(data, True, False)
    elif type == JSONB_TYPE_LARGE_ARRAY:
        v = parse_json_object_or_array(data, False, False)
    elif type == JSONB_TYPE_LITERAL:
        v = parse_literal(data)
    elif type == JSONB_TYPE_INT16:
        v = parse_int16(data)
    elif type == JSONB_TYPE_UINT16:
        v = parse_uint16(data)
    elif type == JSONB_TYPE_INT32:
        v = parse_int32(data)
    elif type == JSONB_TYPE_UINT32:
        v = parse_uint32(data)
    elif type == JSONB_TYPE_INT64:
        v = parse_int64(data)
    elif type == JSONB_TYPE_UINT64:
        v = parse_uint64(data)
    elif type == JSONB_TYPE_DOUBLE:
        v = parse_double(data)
    elif type == JSONB_TYPE_STRING:
        length, n = decode_variable_length(data)
        v = parse_string(n, length, data)
    elif type == JSONB_TYPE_OPAQUE:
        v = parse_opaque(data)
    else:
        raise ValueError(f"Json type {type} is not handled")
    return v


def parse_json_object_or_array(bytes, is_small, is_object):
    offset_size = JSONB_SMALL_OFFSET_SIZE if is_small else JSONB_LARGE_OFFSET_SIZE
    count = decode_count(bytes, is_small)
    size = decode_count(bytes[offset_size:], is_small)
    if is_small:
        key_entry_size = JSONB_KEY_ENTRY_SIZE_SMALL
        value_entry_size = JSONB_VALUE_ENTRY_SIZE_SMALL
    else:
        key_entry_size = JSONB_KEY_ENTRY_SIZE_LARGE
        value_entry_size = JSONB_VALUE_ENTRY_SIZE_LARGE
    if is_data_short(bytes, size):
        raise ValueError(
            "Before MySQL 5.7.22, json type generated column may have invalid value"
        )

    header_size = 2 * offset_size + count * value_entry_size

    if is_object:
        header_size += count * key_entry_size

    if header_size > size:
        raise ValueError("header size > size")

    keys = []
    if is_object:
        keys = []
        for i in range(count):
            entry_offset = 2 * offset_size + key_entry_size * i
            key_offset = decode_count(bytes[entry_offset:], is_small)
            key_length = decode_uint(bytes[entry_offset + offset_size :])
            keys.append(bytes[key_offset : key_offset + key_length])

    values = {}
    for i in range(count):
        entry_offset = 2 * offset_size + value_entry_size * i
        if is_object:
            entry_offset += key_entry_size * count
        json_type = bytes[entry_offset]
        if is_json_inline_value(json_type, is_small):
            values[i] = parse_json(
                json_type, bytes[entry_offset + 1 : entry_offset + value_entry_size]
            )
            continue
        value_offset = decode_count(bytes[entry_offset + 1 :], is_small)
        if is_data_short(bytes, value_offset):
            return None
        values[i] = parse_json(json_type, bytes[value_offset:])
    if not is_object:
        return list(values.values())
    out = {}
    for i in range(count):
        out[keys[i]] = values[i]
    return out


def parse_literal(data: bytes):
    json_type = data[0]
    if json_type == JSONB_LITERAL_NULL:
        return None
    elif json_type == JSONB_LITERAL_TRUE:
        return True
    elif json_type == JSONB_LITERAL_FALSE:
        return False

    raise ValueError("NOT LITERAL TYPE")


def parse_opaque(data: bytes):
    if is_data_short(data, 1):
        return None
    type_ = data[0]
    data = data[1:]

    length, n = decode_variable_length(data)
    data = data[n : n + length]

    if type_ in [FIELD_TYPE.NEWDECIMAL, FIELD_TYPE.DECIMAL]:
        return decode_decimal(data)
    elif type_ in [FIELD_TYPE.TIME, FIELD_TYPE.TIME2]:
        return decode_time(data)
    elif type_ in [FIELD_TYPE.DATE, FIELD_TYPE.DATETIME, FIELD_TYPE.DATETIME2]:
        return decode_datetime(data)
    else:
        return data.decode(errors="ignore")


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
        constants.PREVIOUS_GTIDS_LOG_EVENT: event.PreviousGtidsEvent,
        constants.STOP_EVENT: event.StopEvent,
        constants.BEGIN_LOAD_QUERY_EVENT: event.BeginLoadQueryEvent,
        constants.EXECUTE_LOAD_QUERY_EVENT: event.ExecuteLoadQueryEvent,
        constants.HEARTBEAT_LOG_EVENT: event.HeartbeatLogEvent,
        constants.XA_PREPARE_EVENT: event.XAPrepareEvent,
        constants.ROWS_QUERY_LOG_EVENT: event.RowsQueryLogEvent,
        constants.RAND_EVENT: event.RandEvent,
        constants.USER_VAR_EVENT: event.UserVarEvent,
        # row_event
        constants.UPDATE_ROWS_EVENT_V1: row_event.UpdateRowsEvent,
        constants.WRITE_ROWS_EVENT_V1: row_event.WriteRowsEvent,
        constants.DELETE_ROWS_EVENT_V1: row_event.DeleteRowsEvent,
        constants.UPDATE_ROWS_EVENT_V2: row_event.UpdateRowsEvent,
        constants.WRITE_ROWS_EVENT_V2: row_event.WriteRowsEvent,
        constants.DELETE_ROWS_EVENT_V2: row_event.DeleteRowsEvent,
        constants.TABLE_MAP_EVENT: row_event.TableMapEvent,
        # 5.6 GTID enabled replication events
        constants.ANONYMOUS_GTID_LOG_EVENT: event.NotImplementedEvent,
        # MariaDB GTID
        constants.MARIADB_ANNOTATE_ROWS_EVENT: event.MariadbAnnotateRowsEvent,
        constants.MARIADB_BINLOG_CHECKPOINT_EVENT: event.MariadbBinLogCheckPointEvent,
        constants.MARIADB_GTID_EVENT: event.MariadbGtidEvent,
        constants.MARIADB_GTID_GTID_LIST_EVENT: event.MariadbGtidListEvent,
        constants.MARIADB_START_ENCRYPTION_EVENT: event.MariadbStartEncryptionEvent,
    }

    def __init__(
        self,
        from_packet,
        table_map,
        ctl_connection,
        mysql_version,
        use_checksum,
        allowed_events,
        only_tables,
        ignored_tables,
        only_schemas,
        ignored_schemas,
        freeze_schema,
        ignore_decode_errors,
        verify_checksum,
        optional_meta_data,
    ):
        # -1 because we ignore the ok byte
        self.read_bytes = 0
        # Used when we want to override a value in the data buffer
        self.__data_buffer = b""

        self.packet = from_packet
        self.charset = ctl_connection.charset

        # OK value
        # timestamp
        # event_type
        # server_id
        # log_pos
        # flags
        unpack = struct.unpack("<cIBIIIH", self.packet.read(20))

        # Header
        self.timestamp = unpack[1]
        self.event_type = unpack[2]
        self.server_id = unpack[3]
        self.event_size = unpack[4]
        # position of the next event
        self.log_pos = unpack[5]
        self.flags = unpack[6]

        # MySQL 5.6 and more if binlog-checksum = CRC32
        if use_checksum:
            event_size_without_header = self.event_size - 23
        else:
            verify_checksum = False
            event_size_without_header = self.event_size - 19

        self.event = None
        event_class = self.__event_map.get(self.event_type, event.NotImplementedEvent)

        if event_class not in allowed_events:
            return

        self.event = event_class(
            self,
            event_size_without_header,
            table_map,
            ctl_connection,
            mysql_version=mysql_version,
            only_tables=only_tables,
            ignored_tables=ignored_tables,
            only_schemas=only_schemas,
            ignored_schemas=ignored_schemas,
            freeze_schema=freeze_schema,
            ignore_decode_errors=ignore_decode_errors,
            verify_checksum=verify_checksum,
            optional_meta_data=optional_meta_data,
        )
        if not self.event._processed:
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
        """Push again data in data buffer. It's use when you want
        to extract a bit from a value a let the rest of the code normally
        read the datas"""
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
        c = struct.unpack("!B", self.read(1))[0]
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

        raise AttributeError(f"{self.__class__} instance has no attribute '{key}'")

    def read_int_be_by_size(self, size):
        """Read a big endian integer values based on byte number"""
        if size == 1:
            return struct.unpack(">b", self.read(size))[0]
        elif size == 2:
            return struct.unpack(">h", self.read(size))[0]
        elif size == 3:
            return self.read_int24_be()
        elif size == 4:
            return struct.unpack(">i", self.read(size))[0]
        elif size == 5:
            return self.read_int40_be()
        elif size == 8:
            return struct.unpack(">l", self.read(size))[0]

    def read_uint_by_size(self, size):
        """Read a little endian integer values based on byte number"""
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

    def read_variable_length_string(self):
        """Read a variable length string where the first 1-5 bytes stores the
        length of the string.

        For each byte, the first bit being high indicates another byte must be
        read.
        """
        byte = 0x80
        length = 0
        bits_read = 0
        while byte & 0x80 != 0:
            byte = struct.unpack("!B", self.read(1))[0]
            length = length | ((byte & 0x7F) << bits_read)
            bits_read = bits_read + 7
        return self.read(length)

    def read_int24(self):
        a, b, c = struct.unpack("BBB", self.read(3))
        res = a | (b << 8) | (c << 16)
        if res >= 0x800000:
            res -= 0x1000000
        return res

    def read_int24_be(self):
        a, b, c = struct.unpack("BBB", self.read(3))
        res = (a << 16) | (b << 8) | c
        if res >= 0x800000:
            res -= 0x1000000
        return res

    def read_uint8(self):
        return struct.unpack("<B", self.read(1))[0]

    def read_int16(self):
        return struct.unpack("<h", self.read(2))[0]

    def read_uint16(self):
        return struct.unpack("<H", self.read(2))[0]

    def read_uint24(self):
        a, b, c = struct.unpack("<BBB", self.read(3))
        return a + (b << 8) + (c << 16)

    def read_uint32(self):
        return struct.unpack("<I", self.read(4))[0]

    def read_int32(self):
        return struct.unpack("<i", self.read(4))[0]

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
        return struct.unpack("<Q", self.read(8))[0]

    def read_int64(self):
        return struct.unpack("<q", self.read(8))[0]

    def unpack_uint16(self, n):
        return struct.unpack("<H", n[0:2])[0]

    def unpack_int24(self, n):
        try:
            return (
                struct.unpack("B", n[0])[0]
                + (struct.unpack("B", n[1])[0] << 8)
                + (struct.unpack("B", n[2])[0] << 16)
            )
        except TypeError:
            return n[0] + (n[1] << 8) + (n[2] << 16)

    def unpack_int32(self, n):
        try:
            return (
                struct.unpack("B", n[0])[0]
                + (struct.unpack("B", n[1])[0] << 8)
                + (struct.unpack("B", n[2])[0] << 16)
                + (struct.unpack("B", n[3])[0] << 24)
            )
        except TypeError:
            return n[0] + (n[1] << 8) + (n[2] << 16) + (n[3] << 24)

    def read_binary_json(self, size):
        length = self.read_uint_by_size(size)
        if length == 0:
            # handle NULL value
            return None
        data = self.read(length)
        return parse_json(data[0], data[1:])

    def read_string(self):
        """Read a 'Length Coded String' from the data buffer.

        Read __data_buffer until NULL character (0 = \0 = \x00)

        Returns:
            Binary string parsed from __data_buffer
        """
        string = b""
        while True:
            char = self.read(1)
            if char == b"\0":
                break
            string += char

        return string

    def bytes_to_read(self):
        return len(self.packet._data) - self.packet._position
