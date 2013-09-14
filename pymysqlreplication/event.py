# -*- coding: utf-8 -*-

import struct
from datetime import datetime

from pymysql.util import byte2int, int2byte


class BinLogEvent(object):
    def __init__(self, from_packet, event_size, table_map, metadata_adapter):
        self.packet = from_packet
        self.table_map = table_map
        self.event_type = self.packet.event_type
        self.timestamp = self.packet.timestamp
        self.event_size = event_size
        self.metadata_adapter = metadata_adapter

    def _read_table_id(self):
        # Table ID is 6 byte
        # pad little-endian number
        table_id = self.packet.read(6) + int2byte(0) + int2byte(0)
        return struct.unpack('<Q', table_id)[0]

    def dump(self):
        print("=== %s ===" % self.__class__.__name__)
        print("Date: %s" % (datetime.fromtimestamp(self.timestamp)
                            .isoformat()))
        print("Log position: %d" % self.packet.log_pos)
        print("Event size: %d" % self.event_size)
        print("Read bytes: %d" % self.packet.read_bytes)
        self._dump()
        print()

    def _dump(self):
        """Core data dumped for the event"""
        pass


class RotateEvent(BinLogEvent):
    """Change MySQL bin log file

    Attributes:
        position: Position inside next binlog
        next_binlog: Name of next binlog file
    """
    def __init__(self, from_packet, event_size, table_map, metadata_adapter):
        super(RotateEvent, self).__init__(from_packet, event_size, table_map,
                                          metadata_adapter)
        self.position = struct.unpack('<Q', self.packet.read(8))[0]
        self.next_binlog = self.packet.read(event_size - 8).decode()

    def dump(self):
        print("=== %s ===" % (self.__class__.__name__))
        print("Position: %d" % self.position)
        print("Next binlog file: %s" % self.next_binlog)
        print()


class FormatDescriptionEvent(BinLogEvent):
    pass


class XidEvent(BinLogEvent):
    """A COMMIT event

    Attributes:
        xid: Transaction ID for 2PC
    """

    def __init__(self, from_packet, event_size, table_map, metadata_adapter):
        super(XidEvent, self).__init__(from_packet, event_size, table_map,
                                       metadata_adapter)
        self.xid = struct.unpack('<Q', self.packet.read(8))[0]

    def _dump(self):
        super(XidEvent, self)._dump()
        print("Transaction ID: %d" % self.xid)


class QueryEvent(BinLogEvent):
    """This event is triggered when a query is run on the database.
    Only replicated queries are logged."""
    def __init__(self, from_packet, event_size, table_map, metadata_adapter):
        super(QueryEvent, self).__init__(from_packet, event_size, table_map,
                                         metadata_adapter)

        # Post-header
        self.slave_proxy_id = self.packet.read_uint32()
        self.execution_time = self.packet.read_uint32()
        self.schema_length = byte2int(self.packet.read(1))
        self.error_code = self.packet.read_uint16()
        self.status_vars_length = self.packet.read_uint16()

        # Payload
        self.status_vars = self.packet.read(self.status_vars_length)
        self.schema = self.packet.read(self.schema_length)
        self.packet.advance(1)

        self.query = self.packet.read(event_size - 13 - self.status_vars_length
                                      - self.schema_length - 1).decode("utf-8")
        #string[EOF]    query

    def _dump(self):
        super(QueryEvent, self)._dump()
        print("Schema: %s" % self.schema)
        print("Execution time: %d" % self.execution_time)
        print("Query: %s" % self.query)


class NotImplementedEvent(BinLogEvent):
    def __init__(self, from_packet, event_size, table_map, metadata_adapter):
        super(NotImplementedEvent, self).__init__(
            from_packet, event_size, table_map, metadata_adapter)
        self.packet.advance(event_size)
