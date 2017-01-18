# -*- coding: utf-8 -*-
import struct

from pymysql.util import byte2int, int2byte


class BinLogEvent(object):
    def __init__(self, from_packet, event_size, table_map, ctl_connection,
                 only_tables = None,
                 only_schemas = None,
                 freeze_schema = False,
                 fail_on_table_metadata_unavailable = False,
                 representation_type = None):
        self.packet = from_packet
        self.table_map = table_map
        self.event_type = self.packet.event_type
        self.timestamp = self.packet.timestamp
        self.event_size = event_size
        self._ctl_connection = ctl_connection
        self._fail_on_table_metadata_unavailable = fail_on_table_metadata_unavailable
        # The event have been fully processed, if processed is false
        # the event will be skipped
        self._processed = True
        self.complete = True
        self.representation = representation_type.get_representation(BinLogEvent)(self)

    def _read_table_id(self):
        # Table ID is 6 byte
        # pad little-endian number
        table_id = self.packet.read(6) + int2byte(0) + int2byte(0)
        return struct.unpack('<Q', table_id)[0]

    def dump(self):
        print(self.representation.get_representation())
        self._dump()

    def _dump(self):
        """Core data dumped for the event"""
        pass


class GtidEvent(BinLogEvent):
    """GTID change in binlog event
    """
    def __init__(self, from_packet, event_size, table_map, ctl_connection, representation_type=None, **kwargs):
        super(GtidEvent, self).__init__(from_packet, event_size, table_map,
                                          ctl_connection, representation_type=representation_type, **kwargs)

        self.commit_flag = byte2int(self.packet.read(1)) == 1
        self.sid = self.packet.read(16)
        self.gno = struct.unpack('<Q', self.packet.read(8))[0]
        self._representation = representation_type.get_representation(self.__class__)(self)

    @property
    def gtid(self):
        """GTID = source_id:transaction_id
        Eg: 3E11FA47-71CA-11E1-9E33-C80AA9429562:23
        See: http://dev.mysql.com/doc/refman/5.6/en/replication-gtids-concepts.html"""
        gtid = "%s%s%s%s-%s%s-%s%s-%s%s-%s%s%s%s%s%s" %\
               tuple("{0:02x}".format(ord(c)) for c in self.sid)
        gtid += ":%d" % self.gno
        return gtid

    def _dump(self):
        print(self._representation.get_representation())

    def __repr__(self):
        return '<GtidEvent "%s">' % self.gtid


class RotateEvent(BinLogEvent):
    """Change MySQL bin log file

    Attributes:
        position: Position inside next binlog
        next_binlog: Name of next binlog file
    """
    def __init__(self, from_packet, event_size, table_map, ctl_connection, representation_type = None, **kwargs):
        super(RotateEvent, self).__init__(from_packet, event_size, table_map,
                                          ctl_connection, representation_type = representation_type, **kwargs)
        self.position = struct.unpack('<Q', self.packet.read(8))[0]
        self.next_binlog = self.packet.read(event_size - 8).decode()
        self._representation = representation_type.get_representation(self.__class__)(self)

    def dump(self):
        print(self._representation.get_representation())


class FormatDescriptionEvent(BinLogEvent):
    def __init__(self, from_packet, event_size, table_map, ctl_connection, representation_type = None, **kwargs):
        super(FormatDescriptionEvent, self).__init__(from_packet, event_size, table_map,
                                          ctl_connection, representation_type=representation_type, **kwargs)


class StopEvent(BinLogEvent):
    def __init__(self, from_packet, event_size, table_map, ctl_connection, representation_type = None, **kwargs):
        super(StopEvent, self).__init__(from_packet, event_size, table_map,
                                          ctl_connection, representation_type=representation_type, **kwargs)


class XidEvent(BinLogEvent):
    """A COMMIT event

    Attributes:
        xid: Transaction ID for 2PC
    """

    def __init__(self, from_packet, event_size, table_map, ctl_connection, representation_type = None, **kwargs):
        super(XidEvent, self).__init__(from_packet, event_size, table_map,
                                       ctl_connection, representation_type = representation_type, **kwargs)
        self._representation = representation_type.get_representation(self.__class__)(self)
        self.xid = struct.unpack('<Q', self.packet.read(8))[0]

    def _dump(self):
        super(XidEvent, self)._dump()
        print(self._representation.get_representation())


class QueryEvent(BinLogEvent):
    '''This evenement is trigger when a query is run of the database.
    Only replicated queries are logged.'''
    def __init__(self, from_packet, event_size, table_map, ctl_connection, representation_type = None, **kwargs):
        super(QueryEvent, self).__init__(from_packet, event_size, table_map,
                                         ctl_connection, representation_type = representation_type, **kwargs)

        self._representation = representation_type.get_representation(self.__class__)(self)
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
        print(self._representation.get_representation())


class BeginLoadQueryEvent(BinLogEvent):
    """

    Attributes:
        file_id
        block-data
    """
    def __init__(self, from_packet, event_size, table_map, ctl_connection, representation_type = None, **kwargs):
        super(BeginLoadQueryEvent, self).__init__(from_packet, event_size, table_map,
                                                     ctl_connection, representation_type = representation_type, **kwargs)

        self._representation = representation_type.get_representation(self.__class__)(self)
        # Payload
        self.file_id = self.packet.read_uint32()
        self.block_data = self.packet.read(event_size - 4)

    def _dump(self):
        super(BeginLoadQueryEvent, self)._dump()
        print(self._representation.get_representation())


class ExecuteLoadQueryEvent(BinLogEvent):
    """

    Attributes:
        slave_proxy_id
        execution_time
        schema_length
        error_code
        status_vars_length

        file_id
        start_pos
        end_pos
        dup_handling_flags
    """
    def __init__(self, from_packet, event_size, table_map, ctl_connection, representation_type = None, **kwargs):
        super(ExecuteLoadQueryEvent, self).__init__(from_packet, event_size, table_map,
                                                    ctl_connection, representation_type = representation_type,
                                                    **kwargs)

        self._representation = representation_type.get_representation(self.__class__)(self)
        # Post-header
        self.slave_proxy_id = self.packet.read_uint32()
        self.execution_time = self.packet.read_uint32()
        self.schema_length = self.packet.read_uint8()
        self.error_code = self.packet.read_uint16()
        self.status_vars_length = self.packet.read_uint16()

        # Payload
        self.file_id = self.packet.read_uint32()
        self.start_pos = self.packet.read_uint32()
        self.end_pos = self.packet.read_uint32()
        self.dup_handling_flags = self.packet.read_uint8()

    def _dump(self):
        super(ExecuteLoadQueryEvent, self)._dump()
        print(self._representation.get_representation())


class IntvarEvent(BinLogEvent):
    """

    Attributes:
        type
        value
    """
    def __init__(self, from_packet, event_size, table_map, ctl_connection, representation_type = None, **kwargs):
        super(IntvarEvent, self).__init__(from_packet, event_size, table_map,
                                          ctl_connection, representation_type = representation_type,
                                          **kwargs)

        self._representation = representation_type.get_representation(self.__class__)(self)
        # Payload
        self.type = self.packet.read_uint8()
        self.value = self.packet.read_uint32()

    def _dump(self):
        super(IntvarEvent, self)._dump()
        print(self._representation.get_representation())


class NotImplementedEvent(BinLogEvent):
    def __init__(self, from_packet, event_size, table_map, ctl_connection, **kwargs):
        super(NotImplementedEvent, self).__init__(
            from_packet, event_size, table_map, ctl_connection, **kwargs)
        self.packet.advance(event_size)
