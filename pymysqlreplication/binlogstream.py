import struct
import copy
import pymysql
import pymysql.cursors
from pymysql.constants.COMMAND import *
from pymysql.util import byte2int, int2byte
from .packet import BinLogPacketWrapper
from .constants.BINLOG import TABLE_MAP_EVENT


class BinLogStreamReader(object):
    '''Connect to replication stream and read event'''

    def __init__(self, connection_settings = {}, resume_stream = False, blocking = False, only_events = None, server_id = 255):
        '''
        resume_stream: Start for latest event of binlog or from older available event
        blocking: Read on stream is blocking
        only_events: Array of allowed events
        '''
        self.__connection_settings = connection_settings
        self.__connection_settings['charset'] = 'utf8'
        ctl_connection_settings = copy.copy(self.__connection_settings)
        ctl_connection_settings['db'] = 'information_schema'
        ctl_connection_settings['cursorclass'] = pymysql.cursors.DictCursor
        self.__ctl_connection = pymysql.connect(**ctl_connection_settings)
        self.__connected = False
        self.__resume_stream = resume_stream
        self.__blocking = blocking
        self.__only_events = only_events
        self.__server_id = server_id
        self.__log_pos = None

        #Store table meta informations
        self.table_map = {}

    def close(self):
        if self.__connected:
            self._stream_connection.close()
            self.__connected = False
        self.__ctl_connection.close()

    def __connect_to_stream(self):
        self._stream_connection = pymysql.connect(**self.__connection_settings)
        cur = self._stream_connection.cursor()
        cur.execute("SHOW MASTER STATUS")
        (log_file, log_pos) = cur.fetchone()[:2]
        cur.close()


        # binlog_pos (4) -- position in the binlog-file to start the stream with
        # flags (2) BINLOG_DUMP_NON_BLOCK (0 or 1)
        # server_id (4) -- server id of this slave
        # binlog-filename (string.EOF) -- filename of the binlog on the master
        command = COM_BINLOG_DUMP
        prelude = struct.pack('<i', len(log_file) + 11) \
                + int2byte(command)
        if self.__log_pos is None:
            if self.__resume_stream:
                prelude += struct.pack('<I', log_pos)
            else:
                prelude += struct.pack('<I', 4)
        else:
            prelude += struct.pack('<I', self.__log_pos)
        if self.__blocking:
            prelude += struct.pack('<h', 0)
        else:
            prelude += struct.pack('<h', 1)
        prelude += struct.pack('<I', self.__server_id)
        self._stream_connection.wfile.write(prelude + log_file.encode())
        self._stream_connection.wfile.flush()
        self.__connected = True

    def fetchone(self):
        while True:
            if self.__connected == False:
                self.__connect_to_stream()
            pkt = None
            try:
                pkt = self._stream_connection.read_packet()
            except pymysql.OperationalError as (code, message):
                if code == 2013: #2013: Connection Lost
                    self.__connected = False
                    continue
            if not pkt.is_ok_packet():
                return None
            binlog_event = BinLogPacketWrapper(pkt, self.table_map, self.__ctl_connection)
            if binlog_event.event_type == TABLE_MAP_EVENT:
                self.table_map[binlog_event.event.table_id] = binlog_event.event
            if self.__filter_event(binlog_event.event):
                continue
            self.__log_pos = binlog_event.log_pos
            return binlog_event.event

    def __filter_event(self, event):
        if self.__only_events is not None:
            for allowed_event in self.__only_events:
                if isinstance(event, allowed_event):
                    return False
            return True
        return False

    def __iter__(self):
        return iter(self.fetchone, None)


