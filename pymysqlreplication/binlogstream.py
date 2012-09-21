import struct
from pymysql.util import byte2int, int2byte
from pymysql.constants.COMMAND import *
from constants.BINLOG import *
from event import *

class BinLogStreamReader(object):
    '''Connect to replication stream and read event'''
    
    def __init__(self, connection, resume_stream = False, blocking = False):
        '''
        resume_stream: Start for latest event of binlog or from older available event
        blocking: Read on stream is blocking
        '''
        self.__connection = connection
        self.__connected = False
        self.__resume_stream = resume_stream
        self.__blocking = blocking
        
        #Store table meta informations
        self.table_map = {}


    def __connect_to_stream(self):
        cur = self.__connection.cursor()
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
        if self.__resume_stream:
            prelude += struct.pack('<I', log_pos)            
        else:
            prelude += struct.pack('<I', 4)
        if self.__blocking:
            prelude += struct.pack('<h', 0)
        else:
            prelude += struct.pack('<h', 1)        
        prelude += struct.pack('<I', 3)
        self.__connection.wfile.write(prelude + log_file)
        self.__connection.wfile.flush()
        self.__connected = True
        
    def fetchone(self):
        if self.__connected == False:
            self.__connect_to_stream()
        pkt = self.__connection.read_packet()
        if not pkt.is_ok_packet():
            return None
        binlog_event = BinLogPacketWrapper(pkt, self.table_map)
        if binlog_event.event_type == TABLE_MAP_EVENT:
            self.table_map[binlog_event.event.table_id] = binlog_event.event
        return binlog_event

    def __iter__(self):
        return iter(self.fetchone, None)

class BinLogPacketWrapper(object):
    """
    Bin Log Packet Wrapper. It uses an existing packet object, and wraps
    around it, exposing useful variables while still providing access
    to the original packet objects variables and methods.
    """

    def __init__(self, from_packet, table_map):
        if not from_packet.is_ok_packet():
            raise ValueError('Cannot create ' + str(self.__class__.__name__)
                + ' object from invalid packet type')
        
        # Ok Value
        self.packet = from_packet
        self.packet.advance(1)
  
        # Header
        self.timestamp = struct.unpack('<I', self.packet.read(4))[0]
        self.event_type = byte2int(self.packet.read(1))
        self.server_id = struct.unpack('<I', self.packet.read(4))[0]
        self.event_size = struct.unpack('<I', self.packet.read(4))[0]
        # position of the next event
        self.log_pos = struct.unpack('<I', self.packet.read(4))[0]
        self.flags = struct.unpack('<H', self.packet.read(2))[0]
        

        event_size_without_header = self.event_size - 19
        if self.event_type == QUERY_EVENT:
            self.event = QueryEvent(self.packet, event_size_without_header, table_map)
        elif self.event_type == UPDATE_ROWS_EVENT:
            self.event = UpdateRowsEvent(self.packet, event_size_without_header, table_map)
        elif self.event_type == WRITE_ROWS_EVENT:
            self.event = WriteRowsEvent(self.packet, event_size_without_header, table_map)
        elif self.event_type == DELETE_ROWS_EVENT:
            self.event = DeleteRowsEvent(self.packet, event_size_without_header, table_map)
        elif self.event_type == TABLE_MAP_EVENT:
            self.event = TableMapEvent(self.packet, event_size_without_header, table_map)
        else:
            self.event = None

    def __getattr__(self, key):
        if hasattr(self.packet, key):
            return getattr(self.packet, key)
        
        raise AttributeError(str(self.__class__)
            + " instance has no attribute '" + key + "'")

