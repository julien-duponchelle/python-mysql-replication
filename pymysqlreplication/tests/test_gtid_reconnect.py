"""Unit tests (no MySQL server needed) for resuming from the right GTID set
after the stream connection is lost with ``auto_position``."""

import unittest
from unittest import mock

import pymysql

from pymysqlreplication import BinLogStreamReader
from pymysqlreplication import binlogstream
from pymysqlreplication.constants.BINLOG import (
    GTID_LOG_EVENT,
    XID_EVENT,
    WRITE_ROWS_EVENT_V2,
)
from pymysqlreplication.event import GtidEvent, XidEvent, QueryEvent
from pymysqlreplication.row_event import WriteRowsEvent

SID = bytes.fromhex("11111111222233334444555555555555")
SID_TEXT = "11111111-2222-3333-4444-555555555555"


def gtid_event(gno):
    event = GtidEvent.__new__(GtidEvent)
    event.sid, event.gno = SID, gno
    return event


def wrapper(event, event_type):
    return mock.Mock(event=event, event_type=event_type, timestamp=1, log_pos=0)


def begin_event():
    event = QueryEvent.__new__(QueryEvent)
    event.query = "BEGIN"
    return event


class GtidReconnectTest(unittest.TestCase):
    def run_stream(self, script, **kwargs):
        """Feed ``script`` (events or an exception) to a reader and return the
        auto_position used by each connection attempt."""
        reader = BinLogStreamReader(
            connection_settings={},
            server_id=100,
            auto_position=f"{SID_TEXT}:1-5",
            only_events=[WriteRowsEvent],
            **kwargs,
        )
        used = []
        steps = iter(script)

        def connect():
            used.append(reader.auto_position)
            reader._BinLogStreamReader__connected_stream = True

        def read_packet():
            step = next(steps)
            if isinstance(step, Exception):
                raise step
            return mock.Mock(
                **{"is_eof_packet.return_value": False, "is_ok_packet.return_value": True}
            )

        reader._BinLogStreamReader__connect_to_stream = connect
        reader._BinLogStreamReader__connect_to_ctl = lambda: None
        reader._BinLogStreamReader__connected_ctl = True
        reader._ctl_connection = mock.Mock()
        reader._stream_connection = mock.Mock(_read_packet=read_packet)
        reader._stream_connection.read_packet = read_packet
        return reader, used

    def drain(self, reader, wrappers, expected_rows):
        it = iter(wrappers)
        with mock.patch.object(
            binlogstream, "BinLogPacketWrapper", side_effect=lambda *a, **k: next(it)
        ):
            for _ in range(expected_rows):
                reader.fetchone()

    def test_resume_after_last_committed_transaction(self):
        row = mock.Mock(spec=WriteRowsEvent)
        row.__class__ = WriteRowsEvent
        wrappers = [
            wrapper(gtid_event(6), GTID_LOG_EVENT),
            wrapper(begin_event(), 2),
            wrapper(row, WRITE_ROWS_EVENT_V2),
            wrapper(XidEvent.__new__(XidEvent), XID_EVENT),
            wrapper(gtid_event(7), GTID_LOG_EVENT),  # never committed
            wrapper(row, WRITE_ROWS_EVENT_V2),
            wrapper(row, WRITE_ROWS_EVENT_V2),
        ]
        script = [None] * 6 + [pymysql.OperationalError(2013, "lost")] + [None]
        reader, used = self.run_stream(script)
        self.drain(reader, wrappers, expected_rows=3)
        self.assertEqual(used, [f"{SID_TEXT}:1-5", f"{SID_TEXT}:1-6"])

    def test_gtid_events_parsed_even_when_filtered_out(self):
        reader, _ = self.run_stream([])
        in_packet = reader._BinLogStreamReader__allowed_events_in_packet
        for cls in (GtidEvent, XidEvent, QueryEvent):
            self.assertIn(cls, in_packet)


if __name__ == "__main__":
    unittest.main()
