import pymysql

from pymysqlreplication import BinLogStreamReader, gtid
from pymysqlreplication.event import GtidEvent, RotateEvent, MariadbGtidEvent, QueryEvent
from pymysqlreplication.row_event import WriteRowsEvent, UpdateRowsEvent, DeleteRowsEvent

MARIADB_SETTINGS = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "replication_user",
    "passwd": "secret123passwd",
}


class MariaDbGTID:
    def __init__(self, conn_config):
        self.connection = pymysql.connect(**conn_config)

    def query_single_value(self, sql: str):
        res = None

        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchone()
            res = str(row[0])

        return res

    def extract_gtid(self, gtid: str, server_id: str):
        if gtid is None or server_id is None:
            return None

        gtid_parts = gtid.split("-")

        if len(gtid_parts) != 3:
            return None

        if gtid_parts[1] == server_id:
            return gtid

        return None

    def query_gtid_current_pos(self, server_id: str):
        return self.extract_gtid(self.query_single_value("SELECT @@gtid_current_pos"), server_id)

    def query_server_id(self):
        return int(self.query_single_value("SELECT @@server_id"))


if __name__ == "__main__":
    db = MariaDbGTID(MARIADB_SETTINGS)

    server_id = db.query_server_id()
    print('Server ID: ', server_id)

    # gtid = db.query_gtid_current_pos(server_id)
    gtid = '0-1-1'  # initial pos

    stream = BinLogStreamReader(
        connection_settings=MARIADB_SETTINGS,
        server_id=server_id,
        blocking=False,
        only_events=[
            MariadbGtidEvent,
            RotateEvent,
            WriteRowsEvent,
            UpdateRowsEvent,
            DeleteRowsEvent
        ],
        auto_position=gtid,
        is_mariadb=True
    )

    print('Starting reading events from GTID ', gtid)
    for binlogevent in stream:
        binlogevent.dump()

        if isinstance(binlogevent, MariadbGtidEvent):
            gtid = binlogevent.gtid

    print('Last encountered GTID: ', gtid)

    stream.close()
