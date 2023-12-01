from pymysqlreplication.tests.base import PyMySQLReplicationTestCase
from pymysqlreplication import BinLogStreamReader
import json


class BinLogEventTestCase(PyMySQLReplicationTestCase):
    def setUp(self):
        super(BinLogEventTestCase, self).setUp()
        self.execute("SET SESSION binlog_rows_query_log_events=1")

    def tearDown(self):
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
