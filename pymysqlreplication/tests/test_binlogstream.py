"""Stream regressions using synthetic packets and the real event decoders."""

import struct
from unittest.mock import Mock

import pytest
from pymysql.protocol import MysqlPacket

from pymysqlreplication import BinLogStreamReader, constants
from pymysqlreplication.constants import FIELD_TYPE
from pymysqlreplication.event import RotateEvent
from pymysqlreplication.row_event import UpdateRowsEvent


def _packet(event_type, body, timestamp=200, log_pos=100):
    header = struct.pack(
        "<cIBIIIH", b"\0", timestamp, event_type, 1, 19 + len(body), log_pos, 0
    )
    return MysqlPacket(header + body, "utf8")


def _rotate_packet(filename, timestamp=0):
    return _packet(
        constants.ROTATE_EVENT,
        struct.pack("<Q", 4) + filename.encode(),
        timestamp=timestamp,
        log_pos=0,
    )


def _table_map_packet(table, column_type, schema="test_db"):
    schema = schema.encode()
    table = table.encode()
    metadata = struct.pack("<H", 255) if column_type == FIELD_TYPE.VARCHAR else b""
    body = (
        (7).to_bytes(6, "little")
        + struct.pack("<H", 0)
        + bytes([len(schema)])
        + schema
        + b"\0"
        + bytes([len(table)])
        + table
        + b"\0\x01"
        + bytes([column_type, len(metadata)])
        + metadata
        + b"\0"
    )
    return _packet(constants.TABLE_MAP_EVENT, body)


def _update_packet(before, after):
    body = (
        (7).to_bytes(6, "little")
        + struct.pack("<HH", 0, 2)
        + b"\x01\x01\x01"  # One column, present in both row images.
        + b"\0"
        + before
        + b"\0"
        + after
    )
    return _packet(constants.UPDATE_ROWS_EVENT_V2, body)


@pytest.fixture
def make_stream():
    streams = []

    def make(packets, **kwargs):
        stream = BinLogStreamReader(
            {}, server_id=1, log_file="mysql-bin.000001", log_pos=4, **kwargs
        )
        # Replace only the network connections; fetchone and packet parsing are real.
        stream._stream_connection = Mock()
        stream._stream_connection._read_packet.side_effect = packets + [
            MysqlPacket(b"\xfe", "utf8")
        ]
        stream._ctl_connection = Mock(charset="utf8")
        stream._ctl_connection._get_dbms.return_value = "mysql"
        stream._BinLogStreamReader__connected_stream = True
        stream._BinLogStreamReader__connected_ctl = True
        streams.append(stream)
        return stream

    yield make
    for stream in streams:
        stream.close()


@pytest.mark.parametrize("timestamp", [0, 200])
def test_rotation_to_new_file_clears_table_map(make_stream, timestamp):
    stream = make_stream(
        [
            _table_map_packet("first_table", FIELD_TYPE.VARCHAR),
            _rotate_packet("mysql-bin.000002", timestamp),
        ],
        only_events=[RotateEvent],
    )

    assert isinstance(stream.fetchone(), RotateEvent)
    assert stream.log_file == "mysql-bin.000002"
    assert stream.log_pos == 4
    assert stream.table_map == {}


@pytest.mark.parametrize("freeze_schema", [False, True])
@pytest.mark.parametrize("skip_to_timestamp", [None, 100])
@pytest.mark.parametrize("timestamp", [0, 200])
def test_reused_table_id_decodes_new_table_after_rotation(
    make_stream, freeze_schema, skip_to_timestamp, timestamp
):
    stream = make_stream(
        [
            _table_map_packet("first_table", FIELD_TYPE.VARCHAR),
            _update_packet(b"\x01a", b"\x01b"),
            # A crash can omit the old file's timestamped terminating rotation.
            _rotate_packet("mysql-bin.000002", timestamp),
            _table_map_packet("second_table", FIELD_TYPE.LONG),
            _update_packet(struct.pack("<i", 42), struct.pack("<i", 43)),
        ],
        only_events=[UpdateRowsEvent],
        freeze_schema=freeze_schema,
        skip_to_timestamp=skip_to_timestamp,
    )

    old_event = stream.fetchone()
    assert old_event.table == "first_table"
    assert old_event.rows[0]["before_values"] == {"UNKNOWN_COL0": "a"}
    assert old_event.rows[0]["after_values"] == {"UNKNOWN_COL0": "b"}

    new_event = stream.fetchone()
    # Read rows first so stale VARCHAR metadata reproduces the decoding failure.
    assert new_event.rows[0]["before_values"] == {"UNKNOWN_COL0": 42}
    assert new_event.rows[0]["after_values"] == {"UNKNOWN_COL0": 43}
    assert new_event.schema == "test_db"
    assert new_event.table == "second_table"
    assert stream.log_file == "mysql-bin.000002"
    assert stream.fetchone() is None


@pytest.mark.parametrize("freeze_schema", [False, True])
def test_same_file_reconnect_preserves_table_map(make_stream, freeze_schema):
    stream = make_stream(
        [
            _table_map_packet("first_table", FIELD_TYPE.VARCHAR),
            _update_packet(b"\x01a", b"\x01b"),
            # Reconnecting within a row group need not resend its TableMapEvent.
            _rotate_packet("mysql-bin.000001"),
            _update_packet(b"\x01b", b"\x01c"),
        ],
        only_events=[UpdateRowsEvent],
        freeze_schema=freeze_schema,
    )

    first_event = stream.fetchone()
    assert first_event.rows[0]["after_values"] == {"UNKNOWN_COL0": "b"}
    cached_table = stream.table_map[7]
    resumed_event = stream.fetchone()
    assert resumed_event is not None
    assert resumed_event.rows[0]["before_values"] == {"UNKNOWN_COL0": "b"}
    assert resumed_event.rows[0]["after_values"] == {"UNKNOWN_COL0": "c"}
    assert stream.table_map[7] is cached_table


@pytest.mark.parametrize(
    "filters",
    [
        {"only_tables": ["first_table"]},
        {"ignored_tables": ["second_table"]},
        {"only_schemas": ["test_db"]},
        {"ignored_schemas": ["other_db"]},
    ],
)
def test_filtered_table_does_not_reuse_mapping_after_rotation(make_stream, filters):
    stream = make_stream(
        [
            _table_map_packet("first_table", FIELD_TYPE.VARCHAR),
            _update_packet(b"\x01a", b"\x01b"),
            _rotate_packet("mysql-bin.000002"),
            _table_map_packet("second_table", FIELD_TYPE.LONG, schema="other_db"),
            _update_packet(struct.pack("<i", 42), struct.pack("<i", 43)),
        ],
        only_events=[UpdateRowsEvent],
        freeze_schema=True,
        **filters,
    )

    assert stream.fetchone().table == "first_table"
    assert stream.fetchone() is None
    assert stream.table_map == {}
