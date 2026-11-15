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
from pymysqlreplication.event import GtidEvent, XidEvent, QueryEvent, XAPrepareEvent
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


def query_event(text):
    event = QueryEvent.__new__(QueryEvent)
    event.query = text
    return event


class GtidBoundaryTest(unittest.TestCase):
    """A GTID is executed only at the real end of its transaction."""

    def tracked(self, events):
        reader = BinLogStreamReader(
            connection_settings={},
            server_id=100,
            auto_position=f"{SID_TEXT}:1-5",
        )
        for event in events:
            reader._track_executed_gtid(event)
        return reader._executed_gtids

    def executed(self, events):
        gtids = self.tracked(events)
        return None if gtids is None else str(gtids)

    def test_statement_insert_inside_begin_is_not_a_boundary(self):
        events = [gtid_event(6), query_event("BEGIN"), query_event("INSERT INTO t VALUES (1)")]
        self.assertIsNone(self.tracked(events))
        events.append(query_event("INSERT INTO t VALUES (2)"))
        self.assertIsNone(self.tracked(events))
        events.append(XidEvent.__new__(XidEvent))
        self.assertEqual(self.executed(events), f"{SID_TEXT}:1-6")

    def test_commit_and_rollback_queries_are_boundaries(self):
        for end in ("COMMIT", "ROLLBACK"):
            events = [gtid_event(6), query_event("BEGIN"), query_event(end)]
            self.assertEqual(self.executed(events), f"{SID_TEXT}:1-6", end)

    def test_rollback_to_savepoint_is_not_a_boundary(self):
        events = [gtid_event(6), query_event("BEGIN"), query_event("ROLLBACK TO SAVEPOINT a")]
        self.assertIsNone(self.tracked(events))

    def test_ddl_without_begin_is_a_boundary(self):
        events = [gtid_event(6), query_event("CREATE TABLE t (id int)")]
        self.assertEqual(self.executed(events), f"{SID_TEXT}:1-6")

    def test_xa_start_and_xa_end_are_not_boundaries(self):
        events = [
            gtid_event(6),
            query_event("XA START 0x78,0x,1"),
            query_event("XA END 0x78,0x,1"),
        ]
        self.assertIsNone(self.tracked(events))

    def test_xa_prepare_is_a_boundary(self):
        events = [
            gtid_event(6),
            query_event("XA START 0x78,0x,1"),
            query_event("XA END 0x78,0x,1"),
            XAPrepareEvent.__new__(XAPrepareEvent),
        ]
        self.assertEqual(self.executed(events), f"{SID_TEXT}:1-6")

    def test_xa_commit_and_xa_rollback_are_boundaries(self):
        for end in ("XA COMMIT 0x78,0x,1", "XA ROLLBACK 0x78,0x,1"):
            events = [gtid_event(7), query_event(end)]
            self.assertEqual(self.executed(events), f"{SID_TEXT}:1-5:7", end)


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
