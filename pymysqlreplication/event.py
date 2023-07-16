# -*- coding: utf-8 -*-

import binascii
import struct
import datetime
from pymysqlreplication.constants.STATUS_VAR_KEY import *
from pymysqlreplication.exceptions import StatusVariableMismatch


class BinLogEvent(object):
    def __init__(self, from_packet, event_size, table_map, ctl_connection,
                 mysql_version=(0,0,0),
                 only_tables=None,
                 ignored_tables=None,
                 only_schemas=None,
                 ignored_schemas=None,
                 freeze_schema=False,
                 fail_on_table_metadata_unavailable=False,
                 ignore_decode_errors=False):
        self.packet = from_packet
        self.table_map = table_map
        self.event_type = self.packet.event_type
        self.timestamp = self.packet.timestamp
        self.event_size = event_size
        self._ctl_connection = ctl_connection
        self.mysql_version = mysql_version
        self._fail_on_table_metadata_unavailable = fail_on_table_metadata_unavailable
        self._ignore_decode_errors = ignore_decode_errors
        # The event have been fully processed, if processed is false
        # the event will be skipped
        self._processed = True
        self.complete = True

    def _read_table_id(self):
        # Table ID is 6 byte
        # pad little-endian number
        table_id = self.packet.read(6) + b"\x00\x00"
        return struct.unpack('<Q', table_id)[0]

    def dump(self):
        print("=== %s ===" % (self.__class__.__name__))
        print("Date: %s" % (datetime.datetime.fromtimestamp(self.timestamp)
                            .isoformat()))
        print("Log position: %d" % self.packet.log_pos)
        print("Event size: %d" % (self.event_size))
        print("Read bytes: %d" % (self.packet.read_bytes))
        self._dump()
        print()

    def _dump(self):
        """Core data dumped for the event"""
        pass


class GtidEvent(BinLogEvent):
    """GTID change in binlog event
    """
    def __init__(self, from_packet, event_size, table_map, ctl_connection, **kwargs):
        super(GtidEvent, self).__init__(from_packet, event_size, table_map,
                                          ctl_connection, **kwargs)

        self.commit_flag = struct.unpack("!B", self.packet.read(1))[0] == 1
        self.sid = self.packet.read(16)
        self.gno = struct.unpack('<Q', self.packet.read(8))[0]
        self.lt_type = self.packet.read(1)[0]

        if self.mysql_version >= (5, 7):
            self.last_committed = struct.unpack('<Q', self.packet.read(8))[0]
            self.sequence_number = struct.unpack('<Q', self.packet.read(8))[0]

    @property
    def gtid(self):
        """GTID = source_id:transaction_id
        Eg: 3E11FA47-71CA-11E1-9E33-C80AA9429562:23
        See: http://dev.mysql.com/doc/refman/5.6/en/replication-gtids-concepts.html"""
        nibbles = binascii.hexlify(self.sid).decode('ascii')
        gtid = '%s-%s-%s-%s-%s:%d' % (
            nibbles[:8], nibbles[8:12], nibbles[12:16], nibbles[16:20], nibbles[20:], self.gno
        )
        return gtid

    def _dump(self):
        print("Commit: %s" % self.commit_flag)
        print("GTID_NEXT: %s" % self.gtid)
        if hasattr(self, "last_committed"):
            print("last_committed: %d" % self.last_committed)
            print("sequence_number: %d" % self.sequence_number)

    def __repr__(self):
        return '<GtidEvent "%s">' % self.gtid


class MariadbGtidEvent(BinLogEvent):
    """
    GTID change in binlog event in MariaDB
    https://mariadb.com/kb/en/gtid_event/
    """
    def __init__(self, from_packet, event_size, table_map, ctl_connection, **kwargs):

        super(MariadbGtidEvent, self).__init__(from_packet, event_size, table_map, ctl_connection, **kwargs)

        self.server_id = self.packet.server_id
        self.gtid_seq_no = self.packet.read_uint64()
        self.domain_id = self.packet.read_uint32()
        self.flags = self.packet.read_uint8()
        self.gtid = "%d-%d-%d" % (self.domain_id, self.server_id, self.gtid_seq_no)

    def _dump(self):
        super(MariadbGtidEvent, self)._dump()
        print("Flags:", self.flags)
        print('GTID:', self.gtid)


class RotateEvent(BinLogEvent):
    """Change MySQL bin log file

    Attributes:
        position: Position inside next binlog
        next_binlog: Name of next binlog file
    """
    def __init__(self, from_packet, event_size, table_map, ctl_connection, **kwargs):
        super(RotateEvent, self).__init__(from_packet, event_size, table_map,
                                          ctl_connection, **kwargs)
        self.position = struct.unpack('<Q', self.packet.read(8))[0]
        self.next_binlog = self.packet.read(event_size - 8).decode()

    def dump(self):
        print("=== %s ===" % (self.__class__.__name__))
        print("Position: %d" % self.position)
        print("Next binlog file: %s" % self.next_binlog)
        print()


class XAPrepareEvent(BinLogEvent):
    """An XA prepare event is generated for a XA prepared transaction.
    Like Xid_event it contans XID of the *prepared* transaction

    Attributes:
        one_phase: current XA transaction commit method
        xid: serialized XID representation of XA transaction
    """
    def __init__(self, from_packet, event_size, table_map, ctl_connection, **kwargs):
        super(XAPrepareEvent, self).__init__(from_packet, event_size, table_map,
                                          ctl_connection, **kwargs)

        # one_phase is True: XA COMMIT ... ONE PHASE
        # one_phase is False: XA PREPARE
        self.one_phase = (self.packet.read(1) != b'\x00')
        self.xid_format_id = struct.unpack('<I', self.packet.read(4))[0]
        gtrid_length = struct.unpack('<I', self.packet.read(4))[0]
        bqual_length = struct.unpack('<I', self.packet.read(4))[0]
        self.xid_gtrid = self.packet.read(gtrid_length)
        self.xid_bqual = self.packet.read(bqual_length)

    @property
    def xid(self):
        return self.xid_gtrid.decode() + self.xid_bqual.decode()

    def _dump(self):
        print("One phase: %s" % self.one_phase)
        print("XID formatID: %d" % self.xid_format_id)
        print("XID: %s" % self.xid)


class FormatDescriptionEvent(BinLogEvent):
    def __init__(self, from_packet, event_size, table_map, ctl_connection, **kwargs):
        super(FormatDescriptionEvent, self).__init__(from_packet, event_size, table_map,
                                          ctl_connection, **kwargs)
        self.binlog_version = struct.unpack('<H', self.packet.read(2))
        self.mysql_version_str = self.packet.read(50).rstrip(b'\0').decode()
        numbers = self.mysql_version_str.split('-')[0]
        self.mysql_version = tuple(map(int, numbers.split('.')))

    def _dump(self):
        print("Binlog version: %s" % self.binlog_version)
        print("MySQL version: %s" % self.mysql_version_str)


class StopEvent(BinLogEvent):
    pass


class XidEvent(BinLogEvent):
    """A COMMIT event

    Attributes:
        xid: Transaction ID for 2PC
    """

    def __init__(self, from_packet, event_size, table_map, ctl_connection, **kwargs):
        super(XidEvent, self).__init__(from_packet, event_size, table_map,
                                       ctl_connection, **kwargs)
        self.xid = struct.unpack('<Q', self.packet.read(8))[0]

    def _dump(self):
        super(XidEvent, self)._dump()
        print("Transaction ID: %d" % (self.xid))


class HeartbeatLogEvent(BinLogEvent):
    """A Heartbeat event
    Heartbeats are sent by the master only if there are no unsent events in the
    binary log file for a period longer than the interval defined by
    MASTER_HEARTBEAT_PERIOD connection setting.

    A mysql server will also play those to the slave for each skipped
    events in the log. I (baloo) believe the intention is to make the slave
    bump its position so that if a disconnection occurs, the slave only
    reconnects from the last skipped position (see Binlog_sender::send_events
    in sql/rpl_binlog_sender.cc). That makes 106 bytes of data for skipped
    event in the binlog. *this is also the case with GTID replication*. To
    mitigate such behavior, you are expected to keep the binlog small (see
    max_binlog_size, defaults to 1G).
    In any case, the timestamp is 0 (as in 1970-01-01T00:00:00).

    Attributes:
        ident: Name of the current binlog
    """

    def __init__(self, from_packet, event_size, table_map, ctl_connection, **kwargs):
        super(HeartbeatLogEvent, self).__init__(from_packet, event_size,
                                                table_map, ctl_connection,
                                                **kwargs)
        self.ident = self.packet.read(event_size).decode()

    def _dump(self):
        super(HeartbeatLogEvent, self)._dump()
        print("Current binlog: %s" % (self.ident))


class QueryEvent(BinLogEvent):
    '''This event is trigger when a query is run of the database.
    Only replicated queries are logged.'''
    def __init__(self, from_packet, event_size, table_map, ctl_connection, **kwargs):
        super(QueryEvent, self).__init__(from_packet, event_size, table_map,
                                         ctl_connection, **kwargs)

        # Post-header
        self.slave_proxy_id = self.packet.read_uint32()
        self.execution_time = self.packet.read_uint32()
        self.schema_length = struct.unpack("!B", self.packet.read(1))[0]
        self.error_code = self.packet.read_uint16()
        self.status_vars_length = self.packet.read_uint16()

        # Payload
        status_vars_end_pos = self.packet.read_bytes + self.status_vars_length
        while self.packet.read_bytes < status_vars_end_pos: # while 남은 data length가 얼마만큼? OR read_bytes
            # read KEY for status variable
            status_vars_key = self.packet.read_uint8()
            # read VALUE for status variable
            self._read_status_vars_value_for_key(status_vars_key)

        self.schema = self.packet.read(self.schema_length)
        self.packet.advance(1)

        self.query = self.packet.read(event_size - 13 - self.status_vars_length
                                      - self.schema_length - 1).decode("utf-8")
        #string[EOF]    query

    def _dump(self):
        super(QueryEvent, self)._dump()
        print("Schema: %s" % (self.schema))
        print("Execution time: %d" % (self.execution_time))
        print("Query: %s" % (self.query))

    def _read_status_vars_value_for_key(self, key):
        """parse status variable VALUE for given KEY

        A status variable in query events is a sequence of status KEY-VALUE pairs.
        Parsing logic from mysql-server source code edited by dongwook-chan
        https://github.com/mysql/mysql-server/blob/beb865a960b9a8a16cf999c323e46c5b0c67f21f/libbinlogevents/src/statement_events.cpp#L181-L336

        Args:
            key: key for status variable
        """
        if key == Q_FLAGS2_CODE:                      # 0x00
            self.flags2 = self.packet.read_uint32()
        elif key == Q_SQL_MODE_CODE:                   # 0x01
            self.sql_mode = self.packet.read_uint64()
        elif key == Q_CATALOG_CODE:                   # 0x02 for MySQL 5.0.x
            pass
        elif key == Q_AUTO_INCREMENT:                 # 0x03
            self.auto_increment_increment = self.packet.read_uint16()
            self.auto_increment_offset = self.packet.read_uint16()
        elif key == Q_CHARSET_CODE:                   # 0x04
            self.character_set_client = self.packet.read_uint16()
            self.collation_connection = self.packet.read_uint16()
            self.collation_server = self.packet.read_uint16()
        elif key == Q_TIME_ZONE_CODE:                 # 0x05
            time_zone_len = self.packet.read_uint8()
            if time_zone_len:
                self.time_zone = self.packet.read(time_zone_len) 
        elif key == Q_CATALOG_NZ_CODE:                # 0x06
            catalog_len = self.packet.read_uint8()
            if catalog_len:
                self.catalog_nz_code = self.packet.read(catalog_len)
        elif key == Q_LC_TIME_NAMES_CODE:             # 0x07
            self.lc_time_names_number = self.packet.read_uint16()
        elif key == Q_CHARSET_DATABASE_CODE:          # 0x08
            self.charset_database_number = self.packet.read_uint16()
        elif key == Q_TABLE_MAP_FOR_UPDATE_CODE:      # 0x09
            self.table_map_for_update = self.packet.read_uint64()
        elif key == Q_MASTER_DATA_WRITTEN_CODE:       # 0x0A
            pass
        elif key == Q_INVOKER:                        # 0x0B
            user_len = self.packet.read_uint8()
            if user_len:
                self.user = self.packet.read(user_len)
            host_len = self.packet.read_uint8()
            if host_len:
                self.host = self.packet.read(host_len)
        elif key == Q_UPDATED_DB_NAMES:               # 0x0C
            mts_accessed_dbs = self.packet.read_uint8()
            """
            mts_accessed_dbs < 254:
                `mts_accessed_dbs` is equal to the number of dbs
                acessed by the query event.
            mts_accessed_dbs == 254:
                This is the case where the number of dbs accessed
                is 1 and the name of the only db is ""
                Since no further parsing required(empty name), return.
            """
            if mts_accessed_dbs == 254:
                return
            dbs = []
            for i in range(mts_accessed_dbs):
                db = self.packet.read_string()
                dbs.append(db)
            self.mts_accessed_db_names = dbs
        elif key == Q_MICROSECONDS:                   # 0x0D
            self.microseconds = self.packet.read_uint24()
        elif key == Q_COMMIT_TS:                      # 0x0E
            pass
        elif key == Q_COMMIT_TS2:                     # 0x0F
            pass
        elif key == Q_EXPLICIT_DEFAULTS_FOR_TIMESTAMP:# 0x10
            self.explicit_defaults_ts = self.packet.read_uint8()
        elif key == Q_DDL_LOGGED_WITH_XID:            # 0x11
            self.ddl_xid = self.packet.read_uint64()
        elif key == Q_DEFAULT_COLLATION_FOR_UTF8MB4:  # 0x12
            self.default_collation_for_utf8mb4_number = self.packet.read_uint16()
        elif key == Q_SQL_REQUIRE_PRIMARY_KEY:        # 0x13
            self.sql_require_primary_key = self.packet.read_uint8()
        elif key == Q_DEFAULT_TABLE_ENCRYPTION:       # 0x14
            self.default_table_encryption = self.packet.read_uint8()
        elif key == Q_HRNOW:
            self.hrnow = self.packet.read_uint24()
        elif key == Q_XID:
            self.xid = self.packet.read_uint64()
        else:
            raise StatusVariableMismatch

class BeginLoadQueryEvent(BinLogEvent):
    """

    Attributes:
        file_id
        block-data
    """
    def __init__(self, from_packet, event_size, table_map, ctl_connection, **kwargs):
        super(BeginLoadQueryEvent, self).__init__(from_packet, event_size, table_map,
                                                     ctl_connection, **kwargs)

        # Payload
        self.file_id = self.packet.read_uint32()
        self.block_data = self.packet.read(event_size - 4)

    def _dump(self):
        super(BeginLoadQueryEvent, self)._dump()
        print("File id: %d" % (self.file_id))
        print("Block data: %s" % (self.block_data))


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
    def __init__(self, from_packet, event_size, table_map, ctl_connection, **kwargs):
        super(ExecuteLoadQueryEvent, self).__init__(from_packet, event_size, table_map,
                                                        ctl_connection, **kwargs)

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
        print("Slave proxy id: %d" % (self.slave_proxy_id))
        print("Execution time: %d" % (self.execution_time))
        print("Schema length: %d" % (self.schema_length))
        print("Error code: %d" % (self.error_code))
        print("Status vars length: %d" % (self.status_vars_length))
        print("File id: %d" % (self.file_id))
        print("Start pos: %d" % (self.start_pos))
        print("End pos: %d" % (self.end_pos))
        print("Dup handling flags: %d" % (self.dup_handling_flags))


class IntvarEvent(BinLogEvent):
    """

    Attributes:
        type
        value
    """
    def __init__(self, from_packet, event_size, table_map, ctl_connection, **kwargs):
        super(IntvarEvent, self).__init__(from_packet, event_size, table_map,
                                          ctl_connection, **kwargs)

        # Payload
        self.type = self.packet.read_uint8()
        self.value = self.packet.read_uint32()

    def _dump(self):
        super(IntvarEvent, self)._dump()
        print("type: %d" % (self.type))
        print("Value: %d" % (self.value))


class NotImplementedEvent(BinLogEvent):
    def __init__(self, from_packet, event_size, table_map, ctl_connection, **kwargs):
        super(NotImplementedEvent, self).__init__(
            from_packet, event_size, table_map, ctl_connection, **kwargs)
        self.packet.advance(event_size)
