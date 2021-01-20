#! /usr/bin/env python3
# -*- coding:utf-8 -*-

"""
# Description:
#     xxx
#
# Version:
#     1.0 created by wl_lw at 2021-01-20
# Usage:
#       xxx
#
# Note:
#    add an argument "parse_queue" to AsyncBinLogStreamReamder, parse_queue is an QQueue object.
# Requirement:
#    quick-queue
"""
import pymysql
import struct
from distutils.version import LooseVersion

from pymysql.constants.COMMAND import COM_BINLOG_DUMP, COM_REGISTER_SLAVE
from pymysql.cursors import DictCursor
from pymysql.util import int2byte

from pymysqlreplication.packet import BinLogPacketWrapper
from pymysqlreplication.constants.BINLOG import TABLE_MAP_EVENT, ROTATE_EVENT
from pymysqlreplication.gtid import GtidSet
from pymysqlreplication.event import (
    QueryEvent, RotateEvent, FormatDescriptionEvent,
    XidEvent, GtidEvent, StopEvent,
    BeginLoadQueryEvent, ExecuteLoadQueryEvent,
    HeartbeatLogEvent, NotImplementedEvent)
from pymysqlreplication.exceptions import BinLogNotEnabled
from pymysqlreplication.row_event import (
    UpdateRowsEvent, WriteRowsEvent, DeleteRowsEvent, TableMapEvent)
from pymysqlreplication import BinLogStreamReader


try:
    from pymysql.constants.COMMAND import COM_BINLOG_DUMP_GTID
except ImportError:
    # Handle old pymysql versions
    # See: https://github.com/PyMySQL/PyMySQL/pull/261
    COM_BINLOG_DUMP_GTID = 0x1e

# 2013 Connection Lost
# 2006 MySQL server has gone away
MYSQL_EXPECTED_ERROR_CODES = [2013, 2006]


class ReportSlave(object):

    """Represent the values that you may report when connecting as a slave
    to a master. SHOW SLAVE HOSTS related"""

    hostname = ''
    username = ''
    password = ''
    port = 0

    def __init__(self, value):
        """
        Attributes:
            value: string or tuple
                   if string, then it will be used hostname
                   if tuple it will be used as (hostname, user, password, port)
        """

        if isinstance(value, (tuple, list)):
            try:
                self.hostname = value[0]
                self.username = value[1]
                self.password = value[2]
                self.port = int(value[3])
            except IndexError:
                pass
        elif isinstance(value, dict):
            for key in ['hostname', 'username', 'password', 'port']:
                try:
                    setattr(self, key, value[key])
                except KeyError:
                    pass
        else:
            self.hostname = value

    def __repr__(self):
        return '<ReportSlave hostname=%s username=%s password=%s port=%d>' %\
            (self.hostname, self.username, self.password, self.port)

    def encoded(self, server_id, master_id=0):
        """
        server_id: the slave server-id
        master_id: usually 0. Appears as "master id" in SHOW SLAVE HOSTS
                   on the master. Unknown what else it impacts.
        """

        # 1              [15] COM_REGISTER_SLAVE
        # 4              server-id
        # 1              slaves hostname length
        # string[$len]   slaves hostname
        # 1              slaves user len
        # string[$len]   slaves user
        # 1              slaves password len
        # string[$len]   slaves password
        # 2              slaves mysql-port
        # 4              replication rank
        # 4              master-id

        lhostname = len(self.hostname.encode())
        lusername = len(self.username.encode())
        lpassword = len(self.password.encode())

        packet_len = (1 +  # command
                      4 +  # server-id
                      1 +  # hostname length
                      lhostname +
                      1 +  # username length
                      lusername +
                      1 +  # password length
                      lpassword +
                      2 +  # slave mysql port
                      4 +  # replication rank
                      4)  # master-id

        MAX_STRING_LEN = 257  # one byte for length + 256 chars

        return (struct.pack('<i', packet_len) +
                int2byte(COM_REGISTER_SLAVE) +
                struct.pack('<L', server_id) +
                struct.pack('<%dp' % min(MAX_STRING_LEN, lhostname + 1),
                            self.hostname.encode()) +
                struct.pack('<%dp' % min(MAX_STRING_LEN, lusername + 1),
                            self.username.encode()) +
                struct.pack('<%dp' % min(MAX_STRING_LEN, lpassword + 1),
                            self.password.encode()) +
                struct.pack('<H', self.port) +
                struct.pack('<l', 0) +
                struct.pack('<l', master_id))


class AsyncBinLogStreamReader(BinLogStreamReader):
    report_slave = None

    def __init__(self, connection_settings, server_id,
                 ctl_connection_settings=None, resume_stream=False,
                 blocking=False, only_events=None, log_file=None,
                 log_pos=None, filter_non_implemented_events=True,
                 ignored_events=None, auto_position=None,
                 only_tables=None, ignored_tables=None,
                 only_schemas=None, ignored_schemas=None,
                 freeze_schema=False, skip_to_timestamp=None,
                 report_slave=None, slave_uuid=None,
                 pymysql_wrapper=None,
                 fail_on_table_metadata_unavailable=False,
                 slave_heartbeat=None,
                 parse_queue=None):

        self.__connection_settings = connection_settings
        self.__connection_settings.setdefault("charset", "utf8")

        self.__connected_stream = False
        self.__connected_ctl = False
        self.__resume_stream = resume_stream
        self.__blocking = blocking
        self._ctl_connection_settings = ctl_connection_settings
        if ctl_connection_settings:
            self._ctl_connection_settings.setdefault("charset", "utf8")

        self.__only_tables = only_tables
        self.__ignored_tables = ignored_tables
        self.__only_schemas = only_schemas
        self.__ignored_schemas = ignored_schemas
        self.__freeze_schema = freeze_schema
        self.__allowed_events = self._allowed_event_list(
            only_events, ignored_events, filter_non_implemented_events)
        self.__fail_on_table_metadata_unavailable = fail_on_table_metadata_unavailable

        # We can't filter on packet level TABLE_MAP and rotate event because
        # we need them for handling other operations
        self.__allowed_events_in_packet = frozenset(
            [TableMapEvent, RotateEvent]).union(self.__allowed_events)

        self.__server_id = server_id
        self.__use_checksum = False
        self.__mysql_version = (0, 0)
        self.parse_queue = parse_queue

        # Store table meta information
        self.table_map = {}
        self.log_pos = log_pos
        self.log_file = log_file
        self.auto_position = auto_position
        self.skip_to_timestamp = skip_to_timestamp

        if report_slave:
            self.report_slave = ReportSlave(report_slave)
        self.slave_uuid = slave_uuid
        self.slave_heartbeat = slave_heartbeat

        if pymysql_wrapper:
            self.pymysql_wrapper = pymysql_wrapper
        else:
            self.pymysql_wrapper = pymysql.connect

    def close(self):
        if self.__connected_stream:
            self._stream_connection.close()
            self.__connected_stream = False
        if self.__connected_ctl:
            # break reference cycle between stream reader and underlying
            # mysql connection object
            self._ctl_connection._get_table_information = None
            self._ctl_connection.close()
            self.__connected_ctl = False

    def __connect_to_ctl(self):
        if not self._ctl_connection_settings:
            self._ctl_connection_settings = dict(self.__connection_settings)
        self._ctl_connection_settings["db"] = "information_schema"
        self._ctl_connection_settings["cursorclass"] = DictCursor
        self._ctl_connection = self.pymysql_wrapper(**self._ctl_connection_settings)
        self._ctl_connection._get_table_information = self.__get_table_information
        self.__mysql_version = self.__check_mysql_version()
        self.__connected_ctl = True

    def __checksum_enabled(self):
        """Return True if binlog-checksum = CRC32. Only for MySQL > 5.6"""
        cur = self._stream_connection.cursor()
        cur.execute("SHOW GLOBAL VARIABLES LIKE 'BINLOG_CHECKSUM'")
        result = cur.fetchone()
        cur.close()

        if result is None:
            return False
        var, value = result[:2]
        if value == 'NONE':
            return False
        return True

    def __check_mysql_version(self):
        """Return mysql version formatted (x, y), for compality with mariadb"""
        cur = self._ctl_connection.cursor()
        cur.execute("select version()")
        result = cur.fetchone()
        cur.close()
        self.__mysql_version = tuple(int(i) for i in result.get('version()').split('.')[:2])
        return self.__mysql_version

    def _register_slave(self):
        if not self.report_slave:
            return

        packet = self.report_slave.encoded(self.__server_id)

        if pymysql.__version__ < LooseVersion("0.6"):
            self._stream_connection.wfile.write(packet)
            self._stream_connection.wfile.flush()
            self._stream_connection.read_packet()
        else:
            self._stream_connection._write_bytes(packet)
            self._stream_connection._next_seq_id = 1
            self._stream_connection._read_packet()

    def __connect_to_stream(self):
        # log_pos (4) -- position in the binlog-file to start the stream with
        # flags (2) BINLOG_DUMP_NON_BLOCK (0 or 1)
        # server_id (4) -- server id of this slave
        # log_file (string.EOF) -- filename of the binlog on the master
        self._stream_connection = self.pymysql_wrapper(**self.__connection_settings)

        self.__use_checksum = self.__checksum_enabled()

        # If checksum is enabled we need to inform the server about the that
        # we support it
        if self.__use_checksum:
            cur = self._stream_connection.cursor()
            cur.execute("set @master_binlog_checksum= @@global.binlog_checksum")
            cur.close()

        if self.slave_uuid:
            cur = self._stream_connection.cursor()
            cur.execute("set @slave_uuid= '%s'" % self.slave_uuid)
            cur.close()

        if self.slave_heartbeat:
            # 4294967 is documented as the max value for heartbeats
            net_timeout = float(self.__connection_settings.get('read_timeout',
                                                               4294967))
            # If heartbeat is too low, the connection will disconnect before,
            # this is also the behavior in mysql
            heartbeat = float(min(net_timeout / 2., self.slave_heartbeat))
            if heartbeat > 4294967:
                heartbeat = 4294967

            # master_heartbeat_period is nanoseconds
            heartbeat = int(heartbeat * 1000000000)
            cur = self._stream_connection.cursor()
            cur.execute("set @master_heartbeat_period= %d" % heartbeat)
            cur.close()

        self._register_slave()

        if not self.auto_position:
            # only when log_file and log_pos both provided, the position info is
            # valid, if not, get the current position from master
            if self.log_file is None or self.log_pos is None:
                cur = self._stream_connection.cursor()
                cur.execute("SHOW MASTER STATUS")
                master_status = cur.fetchone()
                if master_status is None:
                    raise BinLogNotEnabled()
                self.log_file, self.log_pos = master_status[:2]
                cur.close()

            prelude = struct.pack('<i', len(self.log_file) + 11) \
                      + int2byte(COM_BINLOG_DUMP)

            if self.__resume_stream:
                prelude += struct.pack('<I', self.log_pos)
            else:
                prelude += struct.pack('<I', 4)

            flags = 0
            if not self.__blocking:
                flags |= 0x01  # BINLOG_DUMP_NON_BLOCK
            prelude += struct.pack('<H', flags)

            prelude += struct.pack('<I', self.__server_id)
            prelude += self.log_file.encode()
        else:
            # Format for mysql packet master_auto_position
            #
            # All fields are little endian
            # All fields are unsigned

            # Packet length   uint   4bytes
            # Packet type     byte   1byte   == 0x1e
            # Binlog flags    ushort 2bytes  == 0 (for retrocompatibilty)
            # Server id       uint   4bytes
            # binlognamesize  uint   4bytes
            # binlogname      str    Nbytes  N = binlognamesize
            #                                Zeroified
            # binlog position uint   4bytes  == 4
            # payload_size    uint   4bytes

            # What come next, is the payload, where the slave gtid_executed
            # is sent to the master
            # n_sid           ulong  8bytes  == which size is the gtid_set
            # | sid           uuid   16bytes UUID as a binary
            # | n_intervals   ulong  8bytes  == how many intervals are sent
            # |                                 for this gtid
            # | | start       ulong  8bytes  Start position of this interval
            # | | stop        ulong  8bytes  Stop position of this interval

            # A gtid set looks like:
            #   19d69c1e-ae97-4b8c-a1ef-9e12ba966457:1-3:8-10,
            #   1c2aad49-ae92-409a-b4df-d05a03e4702e:42-47:80-100:130-140
            #
            # In this particular gtid set,
            # 19d69c1e-ae97-4b8c-a1ef-9e12ba966457:1-3:8-10
            # is the first member of the set, it is called a gtid.
            # In this gtid, 19d69c1e-ae97-4b8c-a1ef-9e12ba966457 is the sid
            # and have two intervals, 1-3 and 8-10, 1 is the start position of
            # the first interval 3 is the stop position of the first interval.

            gtid_set = GtidSet(self.auto_position)
            encoded_data_size = gtid_set.encoded_length

            header_size = (2 +  # binlog_flags
                           4 +  # server_id
                           4 +  # binlog_name_info_size
                           4 +  # empty binlog name
                           8 +  # binlog_pos_info_size
                           4)  # encoded_data_size

            prelude = b'' + struct.pack('<i', header_size + encoded_data_size) \
                      + int2byte(COM_BINLOG_DUMP_GTID)

            flags = 0
            if not self.__blocking:
                flags |= 0x01  # BINLOG_DUMP_NON_BLOCK
            flags |= 0x04  # BINLOG_THROUGH_GTID

            # binlog_flags (2 bytes)
            # see:
            #  https://dev.mysql.com/doc/internals/en/com-binlog-dump-gtid.html
            prelude += struct.pack('<H', flags)

            # server_id (4 bytes)
            prelude += struct.pack('<I', self.__server_id)
            # binlog_name_info_size (4 bytes)
            prelude += struct.pack('<I', 3)
            # empty_binlog_name (4 bytes)
            prelude += b'\0\0\0'
            # binlog_pos_info (8 bytes)
            prelude += struct.pack('<Q', 4)

            # encoded_data_size (4 bytes)
            prelude += struct.pack('<I', gtid_set.encoded_length)
            # encoded_data
            prelude += gtid_set.encoded()

        if pymysql.__version__ < LooseVersion("0.6"):
            self._stream_connection.wfile.write(prelude)
            self._stream_connection.wfile.flush()
        else:
            self._stream_connection._write_bytes(prelude)
            self._stream_connection._next_seq_id = 1
        self.__connected_stream = True

    def _allowed_event_list(self, only_events, ignored_events,
                            filter_non_implemented_events):
        if only_events is not None:
            events = set(only_events)
        else:
            events = set((
                QueryEvent,
                RotateEvent,
                StopEvent,
                FormatDescriptionEvent,
                XidEvent,
                GtidEvent,
                BeginLoadQueryEvent,
                ExecuteLoadQueryEvent,
                UpdateRowsEvent,
                WriteRowsEvent,
                DeleteRowsEvent,
                TableMapEvent,
                HeartbeatLogEvent,
                NotImplementedEvent,
                ))
        if ignored_events is not None:
            for e in ignored_events:
                events.remove(e)
        if filter_non_implemented_events:
            try:
                events.remove(NotImplementedEvent)
            except KeyError:
                pass
        return frozenset(events)

    def __get_table_information(self, schema, table):
        for i in range(1, 3):
            try:
                if not self.__connected_ctl:
                    self.__connect_to_ctl()

                cur = self._ctl_connection.cursor()
                cur.execute("""
                    SELECT
                        COLUMN_NAME, COLLATION_NAME, CHARACTER_SET_NAME,
                        COLUMN_COMMENT, COLUMN_TYPE, COLUMN_KEY, ORDINAL_POSITION
                    FROM
                        information_schema.columns
                    WHERE
                        table_schema = %s AND table_name = %s
                    ORDER BY ORDINAL_POSITION
                    """, (schema, table))

                return cur.fetchall()
            except pymysql.OperationalError as error:
                code, message = error.args
                if code in MYSQL_EXPECTED_ERROR_CODES:
                    self.__connected_ctl = False
                    continue
                else:
                    raise error

    def fetch_one_event(self):
        self.parse_queue.enqueue_background()
        while True:
            if not self.__connected_stream:
                self.__connect_to_stream()

            try:
                if pymysql.__version__ < LooseVersion("0.6"):
                    pkt = self._stream_connection.read_packet()
                else:
                    pkt = self._stream_connection._read_packet()
            except pymysql.OperationalError as error:
                code, message = error.args
                if code in MYSQL_EXPECTED_ERROR_CODES:
                    self._stream_connection.close()
                    self.__connected_stream = False
                    continue
                raise

            if pkt.is_eof_packet():
                self.close()
                pkt = None

            if not pkt.is_ok_packet():
                continue

            self.parse_queue.put(pkt)

    def parse_binlog_event(self):
        parse_queue = self.parse_queue
        while True:
            pkt = parse_queue.get()
            if not pkt:
                continue

            if not self.__connected_ctl:
                self.__connect_to_ctl()

            binlog_event = BinLogPacketWrapper(pkt, self.table_map,
                                               self._ctl_connection,
                                               self.__use_checksum,
                                               self.__allowed_events_in_packet,
                                               self.__only_tables,
                                               self.__ignored_tables,
                                               self.__only_schemas,
                                               self.__ignored_schemas,
                                               self.__freeze_schema,
                                               self.__fail_on_table_metadata_unavailable,
                                               self.__mysql_version)

            if binlog_event.event_type == ROTATE_EVENT:
                self.log_pos = binlog_event.event.position
                self.log_file = binlog_event.event.next_binlog
                self.table_map = {}
            elif binlog_event.log_pos:
                self.log_pos = binlog_event.log_pos

            if self.skip_to_timestamp and binlog_event.timestamp < self.skip_to_timestamp:
                continue

            if binlog_event.event_type == TABLE_MAP_EVENT and \
                    binlog_event.event is not None:
                self.table_map[binlog_event.event.table_id] = \
                    binlog_event.event.get_table()

            # event is none if we have filter it on packet level
            # we filter also not allowed events
            if binlog_event.event is None or (binlog_event.event.__class__ not in self.__allowed_events):
                continue

            return binlog_event.event

    def __iter__(self):
        return iter(self.parse_binlog_event, None)
