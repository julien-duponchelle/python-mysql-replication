import json
import struct
import unittest

from pymysql.protocol import MysqlPacket

from pymysqlreplication import BinLogStreamReader
from pymysqlreplication import constants
from pymysqlreplication.event import FormatDescriptionEvent, QueryEvent
from pymysqlreplication.exceptions import MalformedBinLogEvent
from pymysqlreplication.packet import BinLogPacketWrapper
from pymysqlreplication.tests.base import PyMySQLReplicationTestCase


class _CtlConnection:
    charset = "utf8"

    def _get_dbms(self):
        return "mysql"


def _packet(event_type, body, log_pos=4, checksum=b""):
    event_size = 19 + len(body) + len(checksum)
    header = struct.pack("<cIBIIIH", b"\0", 0, event_type, 1, event_size, log_pos, 0)
    return MysqlPacket(header + body + checksum, 0)


def _wrapper(
    event_type,
    body,
    event_class,
    post_header_lengths=None,
    use_checksum=False,
    checksum=b"",
):
    return BinLogPacketWrapper(
        _packet(event_type, body, checksum=checksum),
        {},
        _CtlConnection(),
        (8, 0, 0),
        use_checksum,
        frozenset([event_class]),
        None,
        None,
        None,
        None,
        False,
        False,
        False,
        False,
        False,
        False,
        post_header_lengths,
    )


class BinLogProtocolEventTestCase(unittest.TestCase):
    def test_format_description_event_reads_full_post_header_lengths(self):
        post_header_lengths = bytearray(41)
        post_header_lengths[constants.QUERY_EVENT - 1] = 13
        post_header_lengths[constants.FORMAT_DESCRIPTION_EVENT - 1] = 98
        post_header_lengths[constants.TABLE_MAP_EVENT - 1] = 8
        post_header_lengths[constants.WRITE_ROWS_EVENT_V2 - 1] = 10
        post_header_lengths[constants.UPDATE_ROWS_EVENT_V2 - 1] = 10
        post_header_lengths[constants.DELETE_ROWS_EVENT_V2 - 1] = 10

        body = (
            struct.pack("<H", 4)
            + b"8.0.46".ljust(50, b"\0")
            + struct.pack("<I", 0)
            + b"\x13"
            + bytes(post_header_lengths)
            + b"\x01"
        )

        event = _wrapper(
            constants.FORMAT_DESCRIPTION_EVENT,
            body,
            FormatDescriptionEvent,
            use_checksum=True,
            checksum=b"\0\0\0\0",
        ).event

        self.assertEqual(event.common_header_len, 19)
        self.assertEqual(event.number_of_event_types, 41)
        self.assertEqual(event.post_header_len[constants.QUERY_EVENT - 1], 13)
        self.assertEqual(event.post_header_len[constants.TABLE_MAP_EVENT - 1], 8)
        self.assertEqual(event.post_header_len[constants.WRITE_ROWS_EVENT_V2 - 1], 10)
        self.assertEqual(event.checksum_algorithm, 1)

    def test_query_event_skips_fde_declared_extra_post_header_bytes(self):
        post_header_lengths = [0] * 41
        post_header_lengths[constants.QUERY_EVENT - 1] = 15
        body = (
            struct.pack("<IIBHH", 10, 0, 2, 0, 0)
            + b"xy"
            + b"d1"
            + b"\0"
            + b"CREATE TABLE t1 (id INT)"
        )

        event = _wrapper(
            constants.QUERY_EVENT,
            body,
            QueryEvent,
            post_header_lengths=tuple(post_header_lengths),
        ).event

        self.assertEqual(event.schema, b"d1")
        self.assertEqual(event.query, "CREATE TABLE t1 (id INT)")

    def test_query_event_rejects_short_declared_post_header(self):
        post_header_lengths = [0] * 41
        post_header_lengths[constants.QUERY_EVENT - 1] = 12
        body = struct.pack("<IIBHH", 10, 0, 0, 0, 0)

        with self.assertRaises(MalformedBinLogEvent):
            _wrapper(
                constants.QUERY_EVENT,
                body,
                QueryEvent,
                post_header_lengths=tuple(post_header_lengths),
            )


class BinLogEventTestCase(PyMySQLReplicationTestCase):
    def setUp(self):
        super(BinLogEventTestCase, self).setUp()
        if not self.isMariaDB():
            self.execute("SET SESSION binlog_rows_query_log_events=1")

    def tearDown(self):
        if not self.isMariaDB():
            self.execute("SET SESSION binlog_rows_query_log_events=0")
        super(BinLogEventTestCase, self).tearDown()

    target_fields = ["timestamp", "log_pos", "event_size", "read_bytes"]

    def test_to_dict(self):
        self.stream = BinLogStreamReader(self.database, server_id=1024)
        query = "CREATE TABLE test (id INT NOT NULL AUTO_INCREMENT, data VARCHAR (50) NOT NULL, PRIMARY KEY (id))"
        self.execute(query)
        self.execute("COMMIT")

        event = self.stream.fetchone()

        event_dict = event.to_dict()

        self.assertEqual(set(event_dict.keys()), set(self.target_fields))
        self.assertEqual(event_dict["timestamp"], event.formatted_timestamp)
        self.assertEqual(event_dict["log_pos"], event.packet.log_pos)
        self.assertEqual(event_dict["read_bytes"], event.packet.read_bytes)
        self.assertEqual(event_dict["event_size"], event.event_size)

    def test_to_json(self):
        self.stream = BinLogStreamReader(self.database, server_id=1024)
        query = "CREATE TABLE test (id INT NOT NULL AUTO_INCREMENT, data VARCHAR (50) NOT NULL, PRIMARY KEY (id))"
        self.execute(query)
        self.execute("COMMIT")

        event = self.stream.fetchone()

        assert event.to_json() == json.dumps(event.to_dict())
