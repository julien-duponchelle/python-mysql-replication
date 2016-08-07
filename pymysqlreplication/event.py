# -*- coding: utf-8 -*-

import struct
import datetime
import sqlparse

from pymysql.util import byte2int, int2byte


class BinLogEvent(object):
    def __init__(self, from_packet, event_size, table_map, ctl_connection,
                 only_tables=None,
                 only_schemas=None,
                 freeze_schema=False):
        self.packet = from_packet
        self.table_map = table_map
        self.event_type = self.packet.event_type
        self.timestamp = self.packet.timestamp
        self.event_size = event_size
        self._ctl_connection = ctl_connection
        # The event have been fully processed, if processed is false
        # the event will be skipped
        self._processed = True
        self.complete = True

    def _read_table_id(self):
        # Table ID is 6 byte
        # pad little-endian number
        table_id = self.packet.read(6) + int2byte(0) + int2byte(0)
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

        self.commit_flag = byte2int(self.packet.read(1)) == 1
        self.sid = self.packet.read(16)
        self.gno = struct.unpack('<Q', self.packet.read(8))[0]

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
        print("Commit: %s" % self.commit_flag)
        print("GTID_NEXT: %s" % self.gtid)

    def __repr__(self):
        return '<GtidEvent "%s">' % self.gtid


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


class FormatDescriptionEvent(BinLogEvent):
    pass


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


class QueryEvent(BinLogEvent):
    '''This evenement is trigger when a query is run of the database.
    Only replicated queries are logged.'''

    def __init__(self, from_packet, event_size, table_map, ctl_connection, **kwargs):
        super(QueryEvent, self).__init__(from_packet, event_size, table_map,
                                         ctl_connection, **kwargs)

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
        # string[EOF]    query

        self.ddl_sql = None
        self.ddl_schema = None
        self.ddl_table = None

        self.__only_tables = kwargs["only_tables"]
        self.__only_schemas = kwargs["only_schemas"]
        self.__sys_schemas = ['mysql', 'information_schema',
                              'innodb', 'sys', 'performance_schema']

    def parse_query(self):
        """Capture and parse schema changing queries.
        """

        sql = self.query
        parsed = sqlparse.parse(sql)[0]
        sql_token_types = []

        # A main statement is the starting DDL or DML command in the query.
        main_statement_counter = 0

        # Keywords can be many things (FROM, WHERE, TABLE, SCHEMA etc.),
        # but we only care about the first one in a query,
        # which for DDLs should be either 'database', 'schema' or 'table'
        keyword_counter = 0
        first_keyword = ''

        # In the MySQL DDL syntax, the first entity identifier is the one
        # which will be modified.
        # slparse returns <schema>.<table> combinations in one Identifier
        # instance. So we'll have to do some further parsing further down the
        # line.
        entity_counter = 0
        entity_identifier = ''
        chars_to_remove = str.maketrans({"'": None, '"': None, "`": None})

        # Validate that we're dealing with a DDL statement.
        for i, t in enumerate(parsed.tokens):
            sql_token_types.append(t.ttype)
            if main_statement_counter == 0 and \
                    t.ttype in [sqlparse.tokens.Keyword.DDL,
                                sqlparse.tokens.Keyword.DML]:
                if t.ttype != sqlparse.tokens.Keyword.DDL:
                    return
                main_statement_counter += 1
                continue
            if keyword_counter == 0 and \
                    t.ttype == sqlparse.tokens.Keyword:
                if t.value.lower() not in ['database', 'schema', 'table']:
                    return
                first_keyword = t.value.lower()
                keyword_counter += 1
                continue
            if entity_counter == 0 and \
                    t.__class__.__name__ == 'Identifier':
                # Remove all quotes from the entity idetifier.
                entity_identifier = str(t.value).translate(chars_to_remove)
                entity_counter += 1
                break

        # Query events are stored together with a 'schema' field in the
        # binlogs,
        # which holds the name of the schema that was the execution context of
        # the query.
        context_schema = self.schema.decode('utf-8').translate(
            chars_to_remove)

        if first_keyword in ['database', 'schema']:
            sql_use = ''
            self.ddl_schema = entity_identifier
        elif first_keyword == 'table':
            sql_use = "USE %s;" % context_schema
            if '.' in entity_identifier:
                self.ddl_schema, self.ddl_table = entity_identifier.split('.')
            else:
                self.ddl_table = entity_identifier
                self.ddl_schema = context_schema

        # Do we have a rule defined which tells us to ignore changes
        # to this entity?
        if self.ddl_schema in self.__sys_schemas:
            return
        if self.__only_tables is not None \
                and self.ddl_table not in self.__only_tables:
            return
        if self.__only_schemas is not None \
                and self.ddl_schema not in self.__only_schemas:
            return

        self.ddl_sql = sql_use + ' ' + sql

    def execute_ddl_statement(self):

        with self._ctl_connection.cursor() as cur:
            cur.execute(self.ddl_sql)
        self._ctl_connection.commit()

        return

    def _dump(self):
        super(QueryEvent, self)._dump()
        print("Schema: %s" % (self.schema))
        print("Execution time: %d" % (self.execution_time))
        print("Query: %s" % (self.query))


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
