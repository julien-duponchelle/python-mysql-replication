# -*- coding: utf-8 -*-

import pymysql
import struct
import time
from distutils.version import LooseVersion

from pymysql.constants.COMMAND import COM_BINLOG_DUMP, COM_REGISTER_SLAVE
from pymysql.cursors import DictCursor

from .packet import BinLogPacketWrapper
from .constants.BINLOG import TABLE_MAP_EVENT, ROTATE_EVENT
from .gtid import GtidSet
from .event import (
    QueryEvent, RotateEvent, FormatDescriptionEvent,
    XidEvent, GtidEvent, StopEvent,
    BeginLoadQueryEvent, ExecuteLoadQueryEvent,
    HeartbeatLogEvent, NotImplementedEvent, MariadbGtidEvent)
from .exceptions import BinLogNotEnabled
from .row_event import (
    UpdateRowsEvent, WriteRowsEvent, DeleteRowsEvent, TableMapEvent)

try:
    from pymysql.constants.COMMAND import COM_BINLOG_DUMP_GTID
except ImportError:
    # Handle old pymysql versions
    # See: https://github.com/PyMySQL/PyMySQL/pull/261
    COM_BINLOG_DUMP_GTID = 0x1e

# 2013 Connection Lost
# 2006 MySQL server has gone away
MYSQL_EXPECTED_ERROR_CODES = [2013, 2006]

PYMYSQL_VERSION_LT_06 = pymysql.__version__ < LooseVersion("0.6")

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
                bytes(bytearray([COM_REGISTER_SLAVE])) +
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


class BinLogStreamReader(object):

    """Connect to replication stream and read event
    """
    report_slave = None

    def __init__(self, connection_settings, server_id,
                 ctl_connection_settings=None, resume_stream=False,
                 blocking=False, only_events=None, log_file=None,
                 log_pos=None, end_log_pos=None,
                 filter_non_implemented_events=True,
                 ignored_events=None, auto_position=None,
                 only_tables=None, ignored_tables=None,
                 only_schemas=None, ignored_schemas=None,
                 freeze_schema=False, skip_to_timestamp=None,
                 report_slave=None, slave_uuid=None,
                 pymysql_wrapper=None,
                 fail_on_table_metadata_unavailable=False,
                 slave_heartbeat=None,
                 is_mariadb=False):
        """
        Parameters:
            connection_settings: a dict of parameters passed to `pymysql.connect`
                or `pymysql_wrapper`, of which "db" parameter is not necessary
            pymysql_wrapper: custom replacement for `pymysql.connect`
            ctl_connection_settings: Connection settings for cluster holding
                schema information, which could be None, in which case
                `connection_settings` will be used as ctl_connection_settings,
                except for that "db" will be replaced to "information_schema"
            resume_stream: True or False. control the start point of the returned
                events, only works when `auto_position` is None.
                `fetchone` will fetch data from:
                1.the begining of `log_file`: if `resume_stream` is False
                2.`log_pos` of `log_file`: if resume_stream is True, and it's
                  the first time to fetch the data
                3.the event right next to the last fetched event: when resume_stream
                  is True and it's not the first time to fetch data
                note: the log position will be set back to the begging of `log_file`
                      each time the client is disconnected and then reconnected
                      to the mysql server (OperationalError 2006/2013) if resume_stream
                      is False. so it's suggested to set resume_stream to True.

            blocking: When master has finished reading/sending binlog it will
                      send EOF instead of blocking connection.
            only_events: Array of allowed events
            ignored_events: Array of ignored events
            log_file: Set replication start log file. if ether `log_file` or
                `log_pos` is None, and auto_position is None, then log_pos
                and log_file will be set as the values returned by the query
                "SHOW MASTER STATUS"
            log_pos: Set replication start log pos (resume_stream should be
                true). if ether `log_file` or `log_pos` is None, and auto_position
                is None, then log_pos and log_file will be set as the values
                returned by the query "SHOW MASTER STATUS", and log_pos will
                be set as 4 (the start position of any log file) if resume_stream
                is a false value
            end_log_pos: Set replication end log pos
            auto_position: a string of replicated GTIDs. all the events except
                for thoses included in `auto_position` and those purged by
                the source server will be sent to the client. a valid `auto_position`
                looks like:
                19d69c1e-ae97-4b8c-a1ef-9e12ba966457:1-3:8-10,
                1c2aad49-ae92-409a-b4df-d05a03e4702e:42-47:80-100:130-140
            only_tables: An array with the tables you want to watch (only works
                         in binlog_format ROW)
            ignored_tables: An array with the tables you want to skip
            only_schemas: An array with the schemas you want to watch
            ignored_schemas: An array with the schemas you want to skip
            freeze_schema: If true do not support ALTER TABLE. It's faster.
            skip_to_timestamp: Ignore all events until reaching specified
                               timestamp.
            report_slave: Report slave in SHOW SLAVE HOSTS.
            slave_uuid: Report slave_uuid in SHOW SLAVE HOSTS.
            fail_on_table_metadata_unavailable: Should raise exception if we
                                                can't get table information on
                                                row_events
            slave_heartbeat: (seconds) Should master actively send heartbeat on
                             connection. This also reduces traffic in GTID
                             replication on replication resumption (in case
                             many event to skip in binlog). See
                             MASTER_HEARTBEAT_PERIOD in mysql documentation
                             for semantics
            is_mariadb: Flag to indicate it's a MariaDB server, used with auto_position
                    to point to Mariadb specific GTID.

        Notes:
            the log position will be set back to the begging of `log_file`
            each time the client is disconnected and then auto-reconnected
            to the mysql server (OperationalError 2006/2013) if resume_stream
            is False. so it's suggested to set resume_stream to True.
        """

        self.__connection_settings = connection_settings
        self.__connection_settings.setdefault("charset", "utf8")

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

        # Store table meta information
        self.table_map = {}
        self.log_pos = log_pos
        self.end_log_pos = end_log_pos
        self.log_file = log_file
        self.auto_position = auto_position
        self.skip_to_timestamp = skip_to_timestamp
        self.is_mariadb = is_mariadb

        if end_log_pos:
            self.is_past_end_log_pos = False

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
        if getattr(self, '_ctl_connection', None):
            # break reference cycle between stream reader and underlying
            # mysql connection object
            self._ctl_connection._get_table_information = None
            if self._ctl_connection.open:
                self._ctl_connection.close()

    def __connect_to_ctl(self, force_reconnect=False):
        if self.__connected_ctl:
            if not force_reconnect:
                return
            self._ctl_connection.close()
        if not self._ctl_connection_settings:
            self._ctl_connection_settings = dict(self.__connection_settings)
        self._ctl_connection_settings["db"] = "information_schema"
        self._ctl_connection_settings["cursorclass"] = DictCursor
        self._ctl_connection = self.pymysql_wrapper(**self._ctl_connection_settings)
        self._ctl_connection._get_table_information = self.__get_table_information

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

    def _register_slave(self):
        if not self.report_slave:
            return

        packet = self.report_slave.encoded(self.__server_id)

        if PYMYSQL_VERSION_LT_06:
            self._stream_connection.wfile.write(packet)
            self._stream_connection.wfile.flush()
            self._stream_connection.read_packet()
        else:
            self._stream_connection._write_bytes(packet)
            self._stream_connection._next_seq_id = 1
            self._stream_connection._read_packet()

    @property
    def __connected_stream(self):
        return bool(getattr(self, '_stream_connection', None) and \
                    self._stream_connection.open)

    @property
    def __connected_ctl(self):
        return bool(getattr(self, '_ctl_connection', None) and \
                    self._ctl_connection.open)

    def __connect_to_stream(self, force_reconnect=False):
        if self.__connected_stream:
            if not force_reconnect:
                return
            self._stream_connection.close()

        # log_pos (4) -- position in the binlog-file to start the stream with
        # flags (2) BINLOG_DUMP_NON_BLOCK (0 or 1)
        # server_id (4) -- server id of this slave
        # log_file (string.EOF) -- filename of the binlog on the master
        self._stream_connection = self.pymysql_wrapper(**self.__connection_settings)
        if PYMYSQL_VERSION_LT_06:
            self._stream_connection._read_packet = self._stream_connection.read_packet

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
            heartbeat = float(min(net_timeout/2., self.slave_heartbeat, 4294967))

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
                + bytes(bytearray([COM_BINLOG_DUMP]))

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
            if self.is_mariadb:
                # https://mariadb.com/kb/en/5-slave-registration/
                cur = self._stream_connection.cursor()

                cur.execute("SET @mariadb_slave_capability=4")
                cur.execute("SET @slave_connect_state='%s'" % self.auto_position)
                cur.execute("SET @slave_gtid_strict_mode=1")
                cur.execute("SET @slave_gtid_ignore_duplicates=0")
                cur.close()

                # https://mariadb.com/kb/en/com_binlog_dump/
                header_size = (
                        4 +  # binlog pos
                        2 +  # binlog flags
                        4 +  # slave server_id,
                        4    # requested binlog file name , set it to empty
                )

                prelude = struct.pack('<i', header_size) + bytes(bytearray([COM_BINLOG_DUMP]))

                # binlog pos
                prelude += struct.pack('<i', 4)

                flags = 0
                if not self.__blocking:
                    flags |= 0x01  # BINLOG_DUMP_NON_BLOCK
                
                # binlog flags
                prelude += struct.pack('<H', flags)

                # server id (4 bytes)
                prelude += struct.pack('<I', self.__server_id)

                # empty_binlog_name (4 bytes)
                prelude += b'\0\0\0\0'
                
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

                prelude = b'' + struct.pack('<i', header_size + encoded_data_size)\
                    + bytes(bytearray([COM_BINLOG_DUMP_GTID]))

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
                # empty_binlog_namapprovale (4 bytes)
                prelude += b'\0\0\0'
                # binlog_pos_info (8 bytes)
                prelude += struct.pack('<Q', 4)

                # encoded_data_size (4 bytes)
                prelude += struct.pack('<I', gtid_set.encoded_length)
                # encoded_data
                prelude += gtid_set.encoded()

        if PYMYSQL_VERSION_LT_06:
            self._stream_connection.wfile.write(prelude)
            self._stream_connection.wfile.flush()
        else:
            self._stream_connection._write_bytes(prelude)
            self._stream_connection._next_seq_id = 1

    def fetchone(self, force_reconnect=False):
        self.__prefetch(force_reconnect=force_reconnect)
        return self.__fetchone()

    def __prefetch(self, force_reconnect=False):
        self.__connect_to_ctl(force_reconnect=force_reconnect)
        self.__connect_to_stream(force_reconnect=force_reconnect)

    def __fetchone(self):
        # let `__fetchone` be as light weight as possible.
        while True:
            if self.end_log_pos and self.is_past_end_log_pos:
                return None

            try:
                pkt = self._stream_connection._read_packet()
            except pymysql.OperationalError as error:
                code, message = error.args
                if code in MYSQL_EXPECTED_ERROR_CODES:
                    self.__connect_to_stream(force_reconnect=True)
                    continue
                raise

            if pkt.is_eof_packet():
                self.close()
                return None

            if not pkt.is_ok_packet():
                continue

            binlog_event = BinLogPacketWrapper(pkt, self.table_map,
                                               self._ctl_connection,
                                               self.__use_checksum,
                                               self.__allowed_events_in_packet,
                                               self.__only_tables,
                                               self.__ignored_tables,
                                               self.__only_schemas,
                                               self.__ignored_schemas,
                                               self.__freeze_schema,
                                               self.__fail_on_table_metadata_unavailable)

            if binlog_event.event_type == ROTATE_EVENT:
                self.log_pos = binlog_event.event.position
                self.log_file = binlog_event.event.next_binlog
                # Table Id in binlog are NOT persistent in MySQL - they are in-memory identifiers
                # that means that when MySQL master restarts, it will reuse same table id for different tables
                # which will cause errors for us since our in-memory map will try to decode row data with
                # wrong table schema.
                # The fix is to rely on the fact that MySQL will also rotate to a new binlog file every time it
                # restarts. That means every rotation we see *could* be a sign of restart and so potentially
                # invalidates all our cached table id to schema mappings. This means we have to load them all
                # again for each logfile which is potentially wasted effort but we can't really do much better
                # without being broken in restart case
                self.table_map = {}
            elif binlog_event.log_pos:
                self.log_pos = binlog_event.log_pos

            if self.end_log_pos and self.log_pos >= self.end_log_pos:
                # We're currently at, or past, the specified end log position.
                self.is_past_end_log_pos = True

            # This check must not occur before clearing the ``table_map`` as a
            # result of a RotateEvent.
            #
            # The first RotateEvent in a binlog file has a timestamp of
            # zero.  If the server has moved to a new log and not written a
            # timestamped RotateEvent at the end of the previous log, the
            # RotateEvent at the beginning of the new log will be ignored
            # if the caller provided a positive ``skip_to_timestamp``
            # value.  This will result in the ``table_map`` becoming
            # corrupt.
            #
            # https://dev.mysql.com/doc/internals/en/event-data-for-specific-event-types.html
            # From the MySQL Internals Manual:
            #
            #   ROTATE_EVENT is generated locally and written to the binary
            #   log on the master. It is written to the relay log on the
            #   slave when FLUSH LOGS occurs, and when receiving a
            #   ROTATE_EVENT from the master. In the latter case, there
            #   will be two rotate events in total originating on different
            #   servers.
            #
            #   There are conditions under which the terminating
            #   log-rotation event does not occur. For example, the server
            #   might crash.
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
                MariadbGtidEvent
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
            self.__connect_to_ctl()
            try:

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
                    continue
                else:
                    raise error

    def __iter__(self):
        self.__prefetch(force_reconnect=False)
        return iter(self.__fetchone, None)
