# -*- coding: utf-8 -*-

from pymysqlreplication.tests import base
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.signals import signal


class TestBinLogSignal(base.PyMySQLReplicationTestCase):
    def test_signal(self):
        self.current_event = None

        def _event_receiver(event):
            self.current_event = event
        signal("binlog_event").connect(_event_receiver, weak=False)

        self.stream.close()
        self.stream = BinLogStreamReader(self.database, server_id=1024)
        query = "CREATE TABLE test (id INT NOT NULL AUTO_INCREMENT, data VARCHAR (50) NOT NULL, PRIMARY KEY (id))"
        self.execute(query)

        event = self.stream.fetchone()
        assert self.current_event == event
